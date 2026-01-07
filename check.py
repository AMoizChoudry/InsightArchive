import lancedb
from pathlib import Path

# Get the absolute path to the .lancedb folder
ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / ".lancedb"

print(f"Checking database at: {DB_PATH}")

if not DB_PATH.exists():
    print("❌ ERROR: .lancedb folder does not exist in this directory.")
else:
    db = lancedb.connect(str(DB_PATH))
    table_names = db.table_names()
    print(f"Tables found: {table_names}")

    if "pdf_search" in table_names:
        table = db.open_table("pdf_search")
        print(f"✅ SUCCESS: Total rows in 'pdf_search': {len(table)}")
        if len(table) > 0:
            print(f"Sample data: {table.to_list()[0]['text'][:100]}...")
    else:
        print("❌ ERROR: The table 'pdf_search' was not found.")