import subprocess
import time
import sys

def start_app():
    print("🚀 Starting PDF Intel Agent...")
    # Start Backend
    backend = subprocess.Popen([sys.executable, "-m", "app.main"])
    time.sleep(2) # Give the backend a moment to breathe
    
    # Start Frontend
    try:
        subprocess.run(["streamlit", "run", "frontend.py"])
    finally:
        backend.terminate()

if __name__ == "__main__":
    start_app()