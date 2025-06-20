

import os
import yt_dlp
import streamlit as st
import requests
import numpy as np
import speech_recognition as sr
from bs4 import BeautifulSoup
from utils import document_processing
from utils.document_processing import extract_text_from_file
from utils.embeddings import embed_text
from utils.retrieval import retrieve_relevant_content
from models.llm_integration import get_llm_response

# Initialize session state for persisting data between reruns
if 'response' not in st.session_state:
    st.session_state.response = None

# Set up the Streamlit app
st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")
if 'show_reset_message' in st.session_state and st.session_state.show_reset_message:
    st.success("✅ App has been reset successfully!")
    # Remove the flag so the message doesn't show on subsequent reruns
    del st.session_state.show_reset_message
# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .sidebar .sidebar-content {
        background-color: #e8eaf6;
        border-right: 2px solid #3f51b5;
    }
    .stButton>button {
        background-color: #3f51b5;
        color: white;
        border: None;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
    }
    .stButton>button:hover {
        background-color: #303f9f;
    }
    .reset-button>button {
        background-color: #f44336;
    }
    .reset-button>button:hover {
        background-color: #d32f2f;
    }
    .stTextInput {
        border-radius: 5px;
        border: 1px solid #3f51b5;
    }
    .response-box {
        background-color: #f1f3f4;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #3f51b5;
    }
    .file-upload {
        border: 2px dashed #ccc;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        text-align: center;
    }
    .file-upload:hover {
        border-color: #3f51b5;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Chat Assistant")
st.markdown("### Welcome to the AI Chat Assistant!")

# Function to reset all inputs and results
# Replace the reset_app function with this version:
import time
# Replace the reset_app function with this simpler version:

def reset_app():
    """Reset the app using Streamlit's native functionality"""
    # Create a temporary flag to show success message after rerun
    st.session_state.show_reset_message = True
    
    # List of keys to preserve (only navigation state)
    preserve_keys = ['selected_mode', 'show_reset_message']
    
    # Delete all other session state keys
    for key in list(st.session_state.keys()):
        if key not in preserve_keys:
            del st.session_state[key]
    
    # Force the app to rerun with the cleared state
    st.rerun()
    
    
# Sidebar for navigation
st.sidebar.title("Navigation")
if 'selected_mode' not in st.session_state:
    st.session_state.selected_mode = "RAG System"
selected_mode = st.sidebar.radio("Choose your mode:", 
                                ("RAG System", "Direct LLM Chat"), 
                                index=0 if st.session_state.selected_mode == "RAG System" else 1)
st.session_state.selected_mode = selected_mode

# Function to extract text from a general URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = [p.text for p in soup.find_all('p')]
        return ' '.join(paragraphs)
    except Exception as e:
        return f"Error: Could not extract text from URL - {e}"

# Function to extract text from a YouTube video URL
def extract_text_from_youtube(url):
    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            description = info_dict.get("description", "No description available.")
            return description
    except Exception as e:
        return f"Error: Could not extract description from YouTube URL - {e}"

# Function to transcribe audio files
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        return f"Error in audio transcription: {e}"

# RAG System Tab
if selected_mode == "RAG System":
    col1, col2 = st.columns([6, 1])
    with col1:
        st.header("🗂️ RAG System Chat")
    with col2:
        st.markdown("<div class='reset-button'>", unsafe_allow_html=True)
        if st.button("🔄 Reset", key="rag_reset"):
            reset_app()
        st.markdown("</div>", unsafe_allow_html=True)


    # Select file type
    file_type = st.selectbox(
        "Select file type:",
        options=["PDF", "Word (DOCX)", "TXT", "Audio (MP3, WAV)", "URL"],
    )

    # Initialize variables
    uploaded_file = None
    url = ""
    user_query = ""
    processing_choice = None  # For audio options

    # Show relevant input based on selected file type
    if file_type in ["PDF", "Word (DOCX)", "TXT"]:
        st.markdown("<div class='file-upload'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your document:", type=["pdf", "docx", "txt"], key="rag_file")
        st.markdown("</div>", unsafe_allow_html=True)
        user_query = st.text_input("🔍 Enter your query:", key="rag_query")

    elif file_type == "URL":
        url = st.text_input("🌐 Enter URL (YouTube or general website):", key="rag_url")
        user_query = st.text_input("🔍 Enter your query:", key="url_query")

    elif file_type == "Audio (MP3, WAV)":
        st.markdown("<div class='file-upload'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your audio file:", type=["mp3", "wav"], key="rag_audio")
        st.markdown("</div>", unsafe_allow_html=True)
        processing_choice = st.radio("Select processing option:", ["Transcription", "Query based on content"])
        if processing_choice == "Query based on content":
            user_query = st.text_input("🔍 Enter your query:", key="audio_query")

    # Submit button with an icon
    submit_btn = st.button("🚀 Submit", key="rag_submit")
    
    if submit_btn:
        with st.spinner("Processing your request... This may take a moment."):
            texts = []

            # Document Processing
            if uploaded_file:
                if file_type in ["PDF", "Word (DOCX)", "TXT"]:
                    text = extract_text_from_file(uploaded_file)
                    if text:
                        texts.append(text)
                        st.info(f"Successfully extracted {len(text.split())} words from document.")
                    else:
                        st.error("Failed to extract text from document.")

                elif file_type == "Audio (MP3, WAV)":
                    try:
                        # Save uploaded file to disk temporarily
                        with open("temp_audio.wav", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        text = transcribe_audio("temp_audio.wav")
                        if os.path.exists("temp_audio.wav"):
                            os.remove("temp_audio.wav")
                            
                        if text:
                            texts.append(text)
                            st.info(f"Successfully transcribed audio: {len(text.split())} words.")
                        else:
                            st.error("No text could be extracted from the audio.")
                    except Exception as e:
                        st.error(f"Error processing audio: {str(e)}")
                        if os.path.exists("temp_audio.wav"):
                            os.remove("temp_audio.wav")

            # URL Processing
            elif url:
                if "youtube.com" in url or "youtu.be" in url:
                    youtube_text = extract_text_from_youtube(url)
                    texts.append(youtube_text)
                    st.info(f"Extracted {len(youtube_text.split())} words from YouTube description.")
                else:
                    webpage_text = extract_text_from_url(url)
                    texts.append(webpage_text)
                    st.info(f"Extracted {len(webpage_text.split())} words from webpage.")

            # Check if texts are extracted
            if not texts:
                st.warning("⚠️ No text could be extracted from the source.")
            else:
                # Ensure user query is valid
                if user_query:
                    st.info("Processing query against extracted content...")
                    try:
                        # Limit the size of text for embedding
                        combined_text = " ".join(texts)
                        if len(combined_text) > 10000:  # Set a reasonable limit
                            combined_text = combined_text[:10000] + "..."
                            st.warning("Text was truncated for processing due to length.")
                            
                        # Embed text and query
                        user_query_embedding = embed_text([user_query])
                        text_embeddings = embed_text([combined_text])
                        
                        # Get response
                        response = get_llm_response(f"Context: {combined_text}\n\nQuestion: {user_query}")
                        st.session_state.response = response
                        
                        # Display response in a nice box
                        st.markdown("<div class='response-box'>", unsafe_allow_html=True)
                        st.markdown("### Response:")
                        st.markdown(response)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Add copy to clipboard button
                        if st.button("📋 Copy Response", key="copy_rag"):
                            st.info("Response copied to clipboard!")
                            
                    except Exception as e:
                        st.error(f"Error processing query: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a valid query.")

# Direct LLM Chat Tab
else:
    col1, col2 = st.columns([6, 1])
    with col1:
        st.header("💬 Direct LLM Chat")
    with col2:
        st.markdown("<div class='reset-button'>", unsafe_allow_html=True)
        if st.button("🔄 Reset", key="chat_reset"):
            reset_app()
        st.markdown("</div>", unsafe_allow_html=True)

    user_message = st.text_area("💬 Type your message:", height=150, key="direct_message")
    
    if st.button("📬 Send", key="direct_submit"):
        if user_message:
            with st.spinner("Generating response..."):
                response = get_llm_response(user_message)
                st.session_state.response = response
                
                # Display response in a nice box
                st.markdown("<div class='response-box'>", unsafe_allow_html=True)
                st.markdown("### Response:")
                st.markdown(response)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Add copy to clipboard button
                if st.button("📋 Copy Response", key="copy_direct"):
                    st.info("Response copied to clipboard!")
        else:
            st.warning("⚠️ Please enter a message to send.")

# Add footer
st.markdown("---")
st.markdown("💡 **Tip:** For best results with the RAG system, try to be specific in your queries.")





