import os
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
import pypdf
from pathlib import Path
from dotenv import load_dotenv
# Force the database to be in the root project folder
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / ".lancedb"
env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

if not os.getenv("OPENAI_API_KEY"):
    print("❌ ERROR: OPENAI_API_KEY not found. Check your .env file.")
# Setup Embedding Model
registry = get_registry().get("openai")
model = registry.create(name="text-embedding-3-small")

class Documents(LanceModel):
    text: str = model.SourceField()
    vector: Vector(model.ndims()) = model.VectorField()

def ingest_pdf(pdf_path: str):
    """Parses PDF and stores it with Hybrid Search (Vector + Keyword) support."""
    print(f"--- Starting Ingestion for {pdf_path} ---")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Could not find {pdf_path}")
        return

    db = lancedb.connect(str(DB_PATH))
    
    reader = pypdf.PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    if not full_text.strip():
        print("❌ Error: No text could be extracted.")
        return

    # Chunking
    chunks = [full_text[i:i+1000] for i in range(0, len(full_text), 1000)]
    data = [{"text": chunk} for chunk in chunks]
    
    # Create Table
    table = db.create_table("pdf_search", data=data, schema=Documents, mode="overwrite")
    
    # NEW: Enable Full-Text Search (Keyword Indexing)
    table.create_fts_index("text", replace=True)
    
    print(f"✅ SUCCESS: Indexed {len(chunks)} chunks with Hybrid Search support.")

def search_docs(query: str, limit: int = 5):
    """Performs Hybrid Search using Vector similarity + Keyword matching."""
    if not os.path.exists(DB_PATH):
        return "Database folder (.lancedb) not found."
        
    db = lancedb.connect(str(DB_PATH))
    if "pdf_search" not in db.table_names():
        return "Table 'pdf_search' not found in database."
        
    table = db.open_table("pdf_search")
    
    # Hybrid Search: Automatically combines vector and keyword results
    results = table.search(query).limit(limit).to_list()
    
    if not results:
        return "No relevant information found."
        
    return "\n".join([r["text"] for r in results])