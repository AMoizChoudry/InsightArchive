import subprocess
import time
import sys
import os

def start_app():
    print("🚀 Starting PDF Intel Agent...")
    
    # 1. Start Backend on port 8000 (Internal communication only)
    # We use sys.executable to ensure we use the same python interpreter
    backend = subprocess.Popen([sys.executable, "-m", "app.main"])
    time.sleep(3) # Give it a moment to boot
    
    # 2. Start Frontend on port 7860 (Hugging Face Requirement)
    # Streamlit needs to listen on 0.0.0.0 to be accessible externally
    try:
        subprocess.run([
            "streamlit", "run", "frontend.py",
            "--server.port=7860", 
            "--server.address=0.0.0.0" 
        ])
    finally:
        backend.terminate()

if __name__ == "__main__":
    start_app()