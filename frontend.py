import streamlit as st
import requests
import time

st.set_page_config(page_title="PDF Chat Pro", layout="wide")

# Custom CSS for better looks
# Custom CSS for better looks
# Custom CSS for better looks
st.markdown("""
    <style>
    /* Change the sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E; /* Dark grey to match VS Code */
        color: white;
    }
    
    /* Optional: Change sidebar text and headers to white */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: white !important;
    }

    /* Style the chat messages */
    .stChatMessage { 
        border-radius: 10px; 
        margin-bottom: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)
st.title("📚 PDF Intel Agent")

with st.sidebar:
    st.header("🛠️ Control Panel")
    
    # Upload Section
    uploaded_file = st.file_uploader("Add Document", type="pdf")
    if st.button("🚀 Index Document", use_container_width=True):
        if uploaded_file:
            with st.status("Reading PDF...", expanded=True) as status:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                res = requests.post("http://127.0.0.1:8000/upload", files=files)
                if res.status_code == 200:
                    status.update(label="✅ Indexing Complete!", state="complete", expanded=False)
                    st.toast(f"Added {uploaded_file.name}")
                else:
                    status.update(label="❌ Upload Failed", state="error")
        else:
            st.error("Select a PDF first.")

    st.divider()
    
 # Remove variant="danger" as it is causing the error
    if st.button("🗑️ Wipe Database", use_container_width=True):
        res = requests.delete("http://127.0.0.1:8000/clear")
        if res.status_code == 200:
            st.session_state.messages = []
            st.rerun()

# --- Chat Window ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I'm ready. Upload a PDF and ask me anything!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your data..."):
    # 1. Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Setup Assistant container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 3. Single API call with Spinner
            with st.spinner("Thinking..."):
                res = requests.post("http://127.0.0.1:8000/chat", json={"message": prompt})
                data = res.json()
                
                # Extract data safely
                answer = data.get("response", "Error: No response.")
                metrics = data.get("metrics", {"db_time": 0, "llm_time": 0})
            
            # 4. Simulate streaming for better UX
            for chunk in answer.split():
                full_response += chunk + " "
                time.sleep(0.04) # Slightly faster for smoother feel
                message_placeholder.markdown(full_response + "▌")
            
            # 5. Finalize text and add Metrics
            message_placeholder.markdown(full_response)
            st.caption(f"⏱️ DB Search: {metrics['db_time']}s | LLM Generation: {metrics['llm_time']}s")
            
            # 6. Save to session history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Backend Connection Error: {e}")