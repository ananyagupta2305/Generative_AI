import os
import yt_dlp
import streamlit as st
import requests
import numpy as np
import speech_recognition as sr
import moviepy.editor as mp
from bs4 import BeautifulSoup
from utils import document_processing
from utils.document_processing import extract_text_from_file
from utils.embeddings import embed_text
from utils.retrieval import retrieve_relevant_content
from models.llm_integration import get_llm_response

# Set up the Streamlit app
st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f0f0f5;
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
    }
    .stButton>button:hover {
        background-color: #303f9f;
    }
    .stTextInput {
        border-radius: 5px;
        border: 1px solid #3f51b5;
    }
    .response-buttons {
        display: flex;
        align-items: center;
        margin-top: 10px;
    }
    .icon-button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        font-size: 24px;
        margin-right: 20px; /* Space between buttons */
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Chat Assistant")
st.markdown("### Welcome to the AI Chat Assistant!")

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_mode = st.sidebar.radio("Choose your mode:", ("RAG System", "Direct LLM Chat"))

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

# Function to process video and extract audio for transcription
def process_video(video_file):
    try:
        video = mp.VideoFileClip(video_file.name)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path)
        
        # Transcribe the extracted audio
        text = transcribe_audio(audio_path)
        os.remove(audio_path)  # Clean up the temporary audio file
        return text
    except Exception as e:
        return f"Error in video processing: {e}"

# RAG System Tab
if selected_mode == "RAG System":
    st.header("🗂️ RAG System Chat")

    # Select file type
    file_type = st.selectbox(
        "Select file type:",
        options=["PDF", "Word (DOCX)", "TXT", "Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)", "URL"],
    )

    # Initialize variables
    uploaded_file = None
    url = ""
    user_query = ""
    processing_choice = None  # For audio/video options

    # Show relevant input based on selected file type
    if file_type in ["PDF", "Word (DOCX)", "TXT"]:
        uploaded_file = st.file_uploader("Upload your document:", type=["pdf", "docx", "txt"])
        user_query = st.text_input("🔍 Enter your query:")

    elif file_type == "URL":
        url = st.text_input("🌐 Enter URL (YouTube or general website):")
        user_query = st.text_input("🔍 Enter your query:")

    elif file_type in ["Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)"]:
        uploaded_file = st.file_uploader("Upload your audio/video file:", type=["mp3", "wav", "mp4", "avi"])
        processing_choice = st.radio("Select processing option:", ["Transcription", "Query based on content"])
        if processing_choice == "Query based on content":
            user_query = st.text_input("🔍 Enter your query:")

    # Submit button with an icon
    if st.button("🚀 Submit"):
        texts = []
        st.spinner("Processing...")  # Add a loading spinner

        # Document Processing
        if uploaded_file:
            if file_type in ["PDF", "Word (DOCX)", "TXT"]:
                text = extract_text_from_file(uploaded_file)
                if text:
                    texts.append(text)

            elif file_type == "Audio (MP3, WAV)":
                text = transcribe_audio(uploaded_file)
                if text:
                    texts.append(text)
                else:
                    st.warning("⚠️ No text could be extracted from the uploaded audio.")

            elif file_type == "Video (MP4, AVI, MPEG4)":
                text = process_video(uploaded_file)
                if text:
                    texts.append(text)

        # URL Processing
        elif url:
            if "youtube.com" in url or "youtu.be" in url:
                youtube_text = extract_text_from_youtube(url)
                texts.append(youtube_text + " " + user_query if user_query else youtube_text)
            else:
                webpage_text = extract_text_from_url(url)
                texts.append(webpage_text + " " + user_query if user_query else webpage_text)

        # Check if texts are extracted
        if not texts:
            st.warning("⚠️ No text could be extracted from the uploaded files or URL.")
        else:
            # Ensure user query is valid
            if user_query:
                user_query_embedding = embed_text([user_query])
            else:
                st.warning("⚠️ Please enter a valid query.")
                user_query_embedding = None
            
            # If the user query is valid, process it
            if user_query_embedding is not None:
                # Limit the length of the combined text for LLM
                combined_text = " ".join(texts)
                if len(combined_text) > 3000:  # Adjust this limit if needed
                    combined_text = combined_text[:3000] + "..."  # Truncate text
                
                embeddings = embed_text([combined_text])
                relevant_content_indices_raw = retrieve_relevant_content(embeddings, user_query_embedding)

                # Flatten array if needed and convert to list of integers
                if isinstance(relevant_content_indices_raw, np.ndarray):
                    relevant_content_indices = [int(i) for i in relevant_content_indices_raw.ravel()]
                elif isinstance(relevant_content_indices_raw, list):
                    relevant_content_indices = [int(i) for sublist in relevant_content_indices_raw for i in (sublist if isinstance(sublist, list) else [sublist])]
                else:
                    relevant_content_indices = [int(relevant_content_indices_raw)]
                
                # Retrieve relevant texts
                relevant_texts = [texts[i] for i in relevant_content_indices]

                # Ensure there's relevant text to query
                if relevant_texts:
                    response = get_llm_response(" ".join(relevant_texts))
                    st.success("**Response:** " + response)

                    # Add buttons for audio and copy functionalities
                    st.markdown("""
                        <div class="response-buttons">
                            <button class="icon-button" id="playAudio">🔊</button>
                            <button class="icon-button" id="copyToClipboard">📋</button>
                        </div>
                    """, unsafe_allow_html=True)

                    # Adding JS for audio and copy functionality
                    st.markdown(f"""
                        <script>
                        document.getElementById('playAudio').onclick = function() {{
                            const response = `{response}`;
                            const utterance = new SpeechSynthesisUtterance(response);
                            speechSynthesis.speak(utterance);
                        }};
                        
                        document.getElementById('copyToClipboard').onclick = function() {{
                            navigator.clipboard.writeText(`{response}`).then(() => {{
                                alert('Response copied to clipboard!');
                            }});
                        }};
                        </script>
                    """, unsafe_allow_html=True)

                else:
                    st.warning("⚠️ No relevant texts found for the query.")
            else:
                st.warning("⚠️ Please enter a valid query.")

# Direct LLM Chat Tab
else:
    st.header("💬 Direct LLM Chat")

    user_message = st.text_input("💬 Type your message:")
    if st.button("📬 Send"):
        if user_message:
            response = get_llm_response(user_message)
            st.success("**Response:** " + response)

            # Add buttons for audio and copy functionalities
            st.markdown("""
                <div class="response-buttons">
                    <button class="icon-button" id="playAudio">🔊</button>
                    <button class="icon-button" id="copyToClipboard">📋</button>
                </div>
            """, unsafe_allow_html=True)

            # Adding JS for audio and copy functionality
            st.markdown(f"""
                <script>
                document.getElementById('playAudio').onclick = function() {{
                    const response = `{response}`;
                    const utterance = new SpeechSynthesisUtterance(response);
                    speechSynthesis.speak(utterance);
                }};
                
                document.getElementById('copyToClipboard').onclick = function() {{
                    navigator.clipboard.writeText(`{response}`).then(() => {{
                        alert('Response copied to clipboard!');
                    }});
                }};
                </script>
            """, unsafe_allow_html=True)

        else:
            st.warning("⚠️ Please enter a message to send.")
