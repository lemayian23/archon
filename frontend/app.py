import streamlit as st
import requests
import pandas as pd
import json
import time

st.set_page_config(page_title="Archon - Data Analysis Copilot", layout="wide")
st.title("🧠 Archon - Data Analysis Copilot")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Your Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Upload file to backend
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response = requests.post("http://localhost:8000/api/v1/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.session_id = data["session_id"]
            st.session_state.file_uploaded = True
            st.success(f"✅ File uploaded successfully!")
            st.write(f"**Filename:** {data['filename']}")
            st.write(f"**Columns:** {', '.join(data['columns'])}")
            st.write(f"**Rows:** {data['row_count']}")
        else:
            st.error("File upload failed")

# Main chat interface
st.header("Ask Questions About Your Data")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if st.session_state.file_uploaded:
    if prompt := st.chat_input("What would you like to know about your data?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Call the backend API
            response = requests.post(
                "http://localhost:8000/api/v1/chat",
                json={
                    "query": prompt,
                    "session_id": st.session_state.session_id
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                full_response = "## Analysis Results\\n\\n"
                
                # Display each agent's work
                for step in data["steps"]:
                    agent = step.get("agent", "")
                    status = step.get("status", "")
                    message = step.get("message", "")
                    output = step.get("output", "")
                    
                    if status == "started":
                        full_response += f"**{agent.upper()}**: {message}\\n"
                    elif status == "completed" and output:
                        full_response += f"✅ **{agent.upper()}**: Completed\\n"
                        if agent == "executor" and step.get("output", {}).get("results"):
                            results = step["output"]["results"]
                            full_response += f"\\n**Results**:\\n```json\\n{json.dumps(results, indent=2)}\\n```\\n"
                        elif output and len(output) < 1000:  # Don't show huge code blocks
                            full_response += f"```\\n{output}\\n```\\n"
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Failed to get response from AI")
else:
    st.info("👆 Please upload a CSV file in the sidebar to get started")
