# import sys
# import os

# # Get the current working directory
# current_dir = os.getcwd()  # Get the current working directory
# # Add the project root directory to the system path
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "utils")))
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "models")))
#  # Append current directory to the path

# import streamlit as st
# from utils import document_processing
# from utils.document_processing import extract_text_from_file, process_audio, process_video
# from utils.embeddings import embed_text
# from utils.retrieval import retrieve_relevant_content
# from models.llm_integration import get_llm_response

# # Setting up the Streamlit app
# st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")

# # Customizing the UI
# st.title("🤖 Chat Assistant")
# st.markdown("### Choose your chat mode:")
# tab1, tab2 = st.tabs(["🗂️ RAG System", "💬 Direct LLM Chat"])

# # RAG System Tab
# with tab1:
#     st.header("RAG System Chat")
    
#     # File upload section with icons
#     uploaded_files = st.file_uploader(
#         "Upload your documents (PDF, Word, TXT, Audio, Video, or URLs)", 
#         type=["pdf", "docx", "txt", "mp3", "wav", "mp4", "avi"], 
#         accept_multiple_files=True,
#         help="You can upload multiple files at once."
#     )

#     # Query input
#     user_query = st.text_input("🔍 Enter your query:")

#     # Submit button with an icon
#     if st.button("🚀 Submit"):
#         if uploaded_files and user_query:
#             texts = []
#             for file in uploaded_files:
#                 text = extract_text_from_file(file)
#                 if text:
#                     texts.append(text)

#             if not texts:
#                 st.warning("⚠️ No text could be extracted from the uploaded files.")
#             else:
#                 # Embed text and retrieve relevant content
#                 embeddings = embed_text(texts)
#                 user_query_embedding = embed_text([user_query])
#                 relevant_content_indices = retrieve_relevant_content(embeddings, user_query_embedding)

#                 # Prepare and display relevant content
#                 relevant_texts = [texts[i] for i in relevant_content_indices[0]]  # Assuming 1st list returns indices
#                 response = get_llm_response(" ".join(relevant_texts) + " " + user_query)

#                 # Display response with emphasis
#                 st.success("**Response:** " + response)
#         else:
#             st.warning("⚠️ Please upload a document and enter a query.")

# # Direct LLM Chat Tab
# with tab2:
#     st.header("Direct LLM Chat")
    
#     user_message = st.text_input("💬 Say something:")
    
#     if st.button("✉️ Send"):
#         if user_message:
#             response = get_llm_response(user_message)
#             st.text_area("LLM Response:", value=response, height=150)
#         else:
#             st.warning("⚠️ Please enter a message.")






















# import sys
# import os
# import yt_dlp
# import streamlit as st
# import requests
# import numpy as np
# from utils import document_processing
# from utils.document_processing import extract_text_from_file, process_audio, process_video
# from utils.embeddings import embed_text
# from utils.retrieval import retrieve_relevant_content
# from models.llm_integration import get_llm_response

# # Additional imports for URL processing and YouTube
# from bs4 import BeautifulSoup
# import youtube_dl  # Install with: pip install youtube_dl

# # Setting up the Streamlit app
# st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")

# # Customizing the UI
# st.title("🤖 Chat Assistant")
# st.markdown("### Choose your chat mode:")
# tab1, tab2 = st.tabs(["🗂️ RAG System", "💬 Direct LLM Chat"])

# # Helper function to extract text from a general URL
# def extract_text_from_url(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = [p.text for p in soup.find_all('p')]
#         return ' '.join(paragraphs)
#     except Exception as e:
#         return f"Error: Could not extract text from URL - {e}"

# # Helper function to extract text or description from a YouTube video URL
# def extract_text_from_youtube(url):
#     try:
#         with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             description = info_dict.get("description", "No description available.")
#             return description
#     except Exception as e:
#         return f"Error: Could not extract audio from YouTube URL - {e}"

# # RAG System Tab
# with tab1:
#     st.header("RAG System Chat")

#     # Choose file type
#     file_type = st.selectbox(
#         "Select file type:",
#         options=["PDF", "Word (DOCX)", "TXT", "Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)", "URL"],
#     )

#     # Initialize variables
#     uploaded_file = None
#     url = ""
#     user_query = ""
#     processing_choice = None  # For audio/video options

#     # Show relevant input based on the selected file type
#     if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#         uploaded_file = st.file_uploader("Upload your document:", type=["pdf", "docx", "txt"])
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type == "URL":
#         url = st.text_input("🌐 Enter URL (YouTube or general website):")
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type in ["Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)"]:
#         uploaded_file = st.file_uploader("Upload your audio/video file:", type=["mp3", "wav", "mp4", "avi"])
#         processing_choice = st.radio("Select processing option:", ["Transcription", "Query based on audio/video content"])
#         if processing_choice == "Query based on audio/video content":
#             user_query = st.text_input("🔍 Enter your query:")

#     # Submit button with an icon
#     if st.button("🚀 Submit"):
#         texts = []
        
#         # Document Processing
#         if uploaded_file:
#             if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#                 text = extract_text_from_file(uploaded_file)
#                 if text:
#                     texts.append(text)

#             elif file_type in ["Audio (MP3, WAV)"]:
#                 if processing_choice == "Transcription":
#                     text = process_audio(uploaded_file)
#                     if text:
#                         texts.append(text)
#                 else:
#                     text = process_audio(uploaded_file)
#                     if text:
#                         texts.append(text + " " + user_query)

#             elif file_type in ["Video (MP4, AVI, MPEG4)"]:
#                 if processing_choice == "Transcription":
#                     text = process_video(uploaded_file, transcribe=True)
#                     if text:
#                         texts.append(text)
#                 else:
#                     text = process_video(uploaded_file)
#                     if text:
#                         texts.append(text + " " + user_query)

#         # URL Processing
#         elif url:
#             if "youtube.com" in url or "youtu.be" in url:
#                 youtube_text = extract_text_from_youtube(url)
#                 texts.append(youtube_text + " " + user_query if user_query else youtube_text)
#             else:
#                 webpage_text = extract_text_from_url(url)
#                 texts.append(webpage_text + " " + user_query if user_query else webpage_text)

#         # Process extracted texts with LLM
#         if not texts:
#             st.warning("⚠️ No text could be extracted from the uploaded files or URL.")
#         else:
#             # Embed text and retrieve relevant content
#             embeddings = embed_text(texts)
#             user_query_embedding = embed_text([user_query]) if user_query else None
#             # Ensure relevant_content_indices is a list of integers
#             relevant_content_indices_raw = retrieve_relevant_content(embeddings, user_query_embedding)
#             # Flatten array if needed and convert to list of integers
#             if isinstance(relevant_content_indices_raw, np.ndarray):
#                 relevant_content_indices = [int(i) for i in relevant_content_indices_raw.ravel()]
#             elif isinstance(relevant_content_indices_raw, list):
#                 # Check if nested lists exist and flatten accordingly
#                 relevant_content_indices = [int(i) for sublist in relevant_content_indices_raw for i in (sublist if isinstance(sublist, list) else [sublist])]
#             else:
#                 # In case of a single integer or unexpected format
#                 relevant_content_indices = [int(relevant_content_indices_raw)]
    
    
#             relevant_texts = [texts[i] for i in relevant_content_indices]

#             response = get_llm_response(" ".join(relevant_texts))

#             # Display response with emphasis
#             st.success("**Response:** " + response)

# # Direct LLM Chat Tab
# with tab2:
#     st.header("Direct LLM Chat")
    
#     user_message = st.text_input("💬 Say something:")
    
#     if st.button("📬 Send"):
#         if user_message:
#             response = get_llm_response(user_message)
#             st.text_area("LLM Response:", value=response, height=150)
#         else:
#             st.warning("⚠️ Please enter a message.")

















# import sys
# import os
# import yt_dlp
# import streamlit as st
# import requests
# import numpy as np
# from utils import document_processing
# from utils.document_processing import extract_text_from_file, process_audio, process_video
# from utils.embeddings import embed_text
# from utils.retrieval import retrieve_relevant_content
# from models.llm_integration import get_llm_response

# # Additional imports for URL processing and YouTube
# from bs4 import BeautifulSoup
# import youtube_dl  # Install with: pip install youtube_dl

# # Setting up the Streamlit app
# st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")

# # Customizing the UI
# st.title("🤖 Chat Assistant")
# st.markdown("### Choose your chat mode:")
# tab1, tab2 = st.tabs(["🗂️ RAG System", "💬 Direct LLM Chat"])

# # Helper function to extract text from a general URL
# def extract_text_from_url(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = [p.text for p in soup.find_all('p')]
#         return ' '.join(paragraphs)
#     except Exception as e:
#         return f"Error: Could not extract text from URL - {e}"

# # Helper function to extract text or description from a YouTube video URL
# def extract_text_from_youtube(url):
#     try:
#         with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             description = info_dict.get("description", "No description available.")
#             return description
#     except Exception as e:
#         return f"Error: Could not extract audio from YouTube URL - {e}"

# # RAG System Tab
# with tab1:
#     st.header("RAG System Chat")

#     # Choose file type
#     file_type = st.selectbox(
#         "Select file type:",
#         options=["PDF", "Word (DOCX)", "TXT", "Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)", "URL"],
#     )

#     # Initialize variables
#     uploaded_file = None
#     url = ""
#     user_query = ""
#     processing_choice = None  # For audio/video options

#     # Show relevant input based on the selected file type
#     if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#         uploaded_file = st.file_uploader("Upload your document:", type=["pdf", "docx", "txt"])
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type == "URL":
#         url = st.text_input("🌐 Enter URL (YouTube or general website):")
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type in ["Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)"]:
#         uploaded_file = st.file_uploader("Upload your audio/video file:", type=["mp3", "wav", "mp4", "avi"])
#         processing_choice = st.radio("Select processing option:", ["Transcription", "Query based on audio/video content"])
#         if processing_choice == "Query based on audio/video content":
#             user_query = st.text_input("🔍 Enter your query:")

#     # Submit button with an icon
#     if st.button("🚀 Submit"):
#         texts = []
        
#         # Document Processing
#         if uploaded_file:
#             if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#                 text = extract_text_from_file(uploaded_file)
#                 if text:
#                     texts.append(text)

#             elif file_type in ["Audio (MP3, WAV)"]:
#                 if processing_choice == "Transcription":
#                     if user_query:  # Ensure a valid query is provided
#                         text = process_audio(uploaded_file)
#                         if text:
#                             texts.append(text)
#                     else:
#                         st.warning("⚠️ Please enter a valid query for transcription.")

#                 else:
#                     text = process_audio(uploaded_file)
#                     if text:
#                         texts.append(text + " " + user_query)

#             elif file_type in ["Video (MP4, AVI, MPEG4)"]:
#                 if processing_choice == "Transcription":
#                     text = process_video(uploaded_file, transcribe=True)
#                     if text:
#                         texts.append(text)
#                 else:
#                     text = process_video(uploaded_file)
#                     if text:
#                         texts.append(text + " " + user_query)

#         # URL Processing
#         elif url:
#             if "youtube.com" in url or "youtu.be" in url:
#                 youtube_text = extract_text_from_youtube(url)
#                 texts.append(youtube_text + " " + user_query if user_query else youtube_text)
#             else:
#                 webpage_text = extract_text_from_url(url)
#                 texts.append(webpage_text + " " + user_query if user_query else webpage_text)

#         # Process extracted texts with LLM
#         if not texts:
#             st.warning("⚠️ No text could be extracted from the uploaded files or URL.")
#         else:
#             # Embed text and retrieve relevant content
#             embeddings = embed_text(texts)
#             user_query_embedding = embed_text([user_query]) if user_query else None
            
#             # Ensure user_query_embedding is not None
#             if user_query_embedding is not None:
#                 relevant_content_indices_raw = retrieve_relevant_content(embeddings, user_query_embedding)

#                 # Flatten array if needed and convert to list of integers
#                 if isinstance(relevant_content_indices_raw, np.ndarray):
#                     relevant_content_indices = [int(i) for i in relevant_content_indices_raw.ravel()]
#                 elif isinstance(relevant_content_indices_raw, list):
#                     relevant_content_indices = [int(i) for sublist in relevant_content_indices_raw for i in (sublist if isinstance(sublist, list) else [sublist])]
#                 else:
#                     relevant_content_indices = [int(relevant_content_indices_raw)]
                
#                 # Retrieve relevant texts
#                 relevant_texts = [texts[i] for i in relevant_content_indices]

#                 response = get_llm_response(" ".join(relevant_texts))

#                 # Display response with emphasis
#                 st.success("**Response:** " + response)
#             else:
#                 st.warning("⚠️ Please enter a valid query.")

# # Direct LLM Chat Tab
# with tab2:
#     st.header("Direct LLM Chat")
    
#     user_message = st.text_input("💬 Say something:")
    
#     if st.button("✉️ Send"):
#         if user_message:
#             response = get_llm_response(user_message)
#             st.text_area("LLM Response:", value=response, height=150)
#         else:
#             st.warning("⚠️ Please enter a message.")


















































# import sys
# import os
# import yt_dlp
# import streamlit as st
# import requests
# import numpy as np
# from utils import document_processing
# from utils.document_processing import extract_text_from_file, process_audio, process_video
# from utils.embeddings import embed_text
# from utils.retrieval import retrieve_relevant_content
# from models.llm_integration import get_llm_response

# # Additional imports for URL processing and YouTube
# from bs4 import BeautifulSoup
# import speech_recognition as sr  # Install with: pip install SpeechRecognition

# # Setting up the Streamlit app
# st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")

# # Customizing the UI
# st.title("🤖 Chat Assistant")
# st.markdown("### Choose your chat mode:")
# tab1, tab2 = st.tabs(["🗂️ RAG System", "💬 Direct LLM Chat"])

# # Helper function to extract text from a general URL
# def extract_text_from_url(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = [p.text for p in soup.find_all('p')]
#         return ' '.join(paragraphs)
#     except Exception as e:
#         return f"Error: Could not extract text from URL - {e}"

# # Helper function to extract text or description from a YouTube video URL
# def extract_text_from_youtube(url):
#     try:
#         with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             description = info_dict.get("description", "No description available.")
#             return description
#     except Exception as e:
#         return f"Error: Could not extract audio from YouTube URL - {e}"

# # Audio processing without FFmpeg
# def process_audio_no_ffmpeg(audio_file):
#     recognizer = sr.Recognizer()
#     try:
#         with sr.AudioFile(audio_file) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data)
#             return text
#     except Exception as e:
#         return f"Error in audio processing: {e}"

# # RAG System Tab
# with tab1:
#     st.header("RAG System Chat")

#     # Choose file type
#     file_type = st.selectbox(
#         "Select file type:",
#         options=["PDF", "Word (DOCX)", "TXT", "Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)", "URL"],
#     )

#     # Initialize variables
#     uploaded_file = None
#     url = ""
#     user_query = ""
#     processing_choice = None  # For audio/video options

#     # Show relevant input based on the selected file type
#     if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#         uploaded_file = st.file_uploader("Upload your document:", type=["pdf", "docx", "txt"])
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type == "URL":
#         url = st.text_input("🌐 Enter URL (YouTube or general website):")
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type in ["Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)"]:
#         uploaded_file = st.file_uploader("Upload your audio/video file:", type=["mp3", "wav", "mp4", "avi"])
#         processing_choice = st.radio("Select processing option:", ["Transcription", "Query based on audio/video content"])
#         if processing_choice == "Query based on audio/video content":
#             user_query = st.text_input("🔍 Enter your query:")

#     # Submit button with an icon
#     if st.button("🚀 Submit"):
#         texts = []
        
#         # Document Processing
#         if uploaded_file:
#             if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#                 text = extract_text_from_file(uploaded_file)
#                 if text:
#                     texts.append(text)

#             elif file_type == "Audio (MP3, WAV)":
#                 if processing_choice == "Transcription":
#                     text = process_audio_no_ffmpeg(uploaded_file)
#                     if text:
#                         texts.append(text)
#                     else:
#                         st.warning("⚠️ No text could be extracted from the uploaded audio.")

#             elif file_type in ["Video (MP4, AVI, MPEG4)"]:
#                 if processing_choice == "Transcription":
#                     text = process_video(uploaded_file, transcribe=True)
#                     if text:
#                         texts.append(text)
#                 elif processing_choice == "Query based on audio/video content":
#                     text = process_video(uploaded_file)
#                     if text:
#                         texts.append(text + " " + user_query)

#         # URL Processing
#         elif url:
#             if "youtube.com" in url or "youtu.be" in url:
#                 youtube_text = extract_text_from_youtube(url)
#                 texts.append(youtube_text + " " + user_query if user_query else youtube_text)
#             else:
#                 webpage_text = extract_text_from_url(url)
#                 texts.append(webpage_text + " " + user_query if user_query else webpage_text)

#         # Process extracted texts with LLM
#         if not texts:
#             st.warning("⚠️ No text could be extracted from the uploaded files or URL.")
#         else:
#             # Embed text and retrieve relevant content
#             embeddings = embed_text(texts)
#             user_query_embedding = embed_text([user_query]) if user_query else None
            
#             # Ensure user_query_embedding is not None
#             if user_query_embedding is not None:
#                 relevant_content_indices_raw = retrieve_relevant_content(embeddings, user_query_embedding)

#                 # Flatten array if needed and convert to list of integers
#                 if isinstance(relevant_content_indices_raw, np.ndarray):
#                     relevant_content_indices = [int(i) for i in relevant_content_indices_raw.ravel()]
#                 elif isinstance(relevant_content_indices_raw, list):
#                     relevant_content_indices = [int(i) for sublist in relevant_content_indices_raw for i in (sublist if isinstance(sublist, list) else [sublist])]
#                 else:
#                     relevant_content_indices = [int(relevant_content_indices_raw)]
                
#                 # Retrieve relevant texts
#                 relevant_texts = [texts[i] for i in relevant_content_indices]

#                 response = get_llm_response(" ".join(relevant_texts))

#                 # Display response with emphasis
#                 st.success("**Response:** " + response)
#             else:
#                 st.warning("⚠️ Please enter a valid query.")

# # Direct LLM Chat Tab
# with tab2:
#     st.header("Direct LLM Chat")
    
#     user_message = st.text_input("💬 Say something:")
    
#     if st.button("✉️ Send"):
#         if user_message:
#             response = get_llm_response(user_message)
#             st.text_area("LLM Response:", value=response, height=150)
#         else:
#             st.warning("⚠️ Please enter a message.")




















































# import sys
# import os
# import yt_dlp
# import streamlit as st
# import requests
# import numpy as np
# import speech_recognition as sr  # Install with: pip install SpeechRecognition
# from bs4 import BeautifulSoup
# from utils import document_processing
# from utils.document_processing import extract_text_from_file, process_audio, process_video
# from utils.embeddings import embed_text
# from utils.retrieval import retrieve_relevant_content
# from models.llm_integration import get_llm_response

# # Setting up the Streamlit app
# st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")

# # Customizing the UI
# st.title("🤖 Chat Assistant")
# st.markdown("### Choose your chat mode:")
# tab1, tab2 = st.tabs(["🗂️ RAG System", "💬 Direct LLM Chat"])

# # Helper function to extract text from a general URL
# def extract_text_from_url(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = [p.text for p in soup.find_all('p')]
#         return ' '.join(paragraphs)
#     except Exception as e:
#         return f"Error: Could not extract text from URL - {e}"

# # Helper function to extract text or description from a YouTube video URL
# def extract_text_from_youtube(url):
#     try:
#         with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             description = info_dict.get("description", "No description available.")
#             return description
#     except Exception as e:
#         return f"Error: Could not extract audio from YouTube URL - {e}"

# # Audio processing without FFmpeg
# def process_audio_no_ffmpeg(audio_file):
#     recognizer = sr.Recognizer()
#     try:
#         with sr.AudioFile(audio_file) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data)
#             return text
#     except Exception as e:
#         return f"Error in audio processing: {e}"

# # RAG System Tab
# with tab1:
#     st.header("RAG System Chat")

#     # Choose file type
#     file_type = st.selectbox(
#         "Select file type:",
#         options=["PDF", "Word (DOCX)", "TXT", "Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)", "URL"],
#     )

#     # Initialize variables
#     uploaded_file = None
#     url = ""
#     user_query = ""
#     processing_choice = None  # For audio/video options

#     # Show relevant input based on the selected file type
#     if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#         uploaded_file = st.file_uploader("Upload your document:", type=["pdf", "docx", "txt"])
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type == "URL":
#         url = st.text_input("🌐 Enter URL (YouTube or general website):")
#         user_query = st.text_input("🔍 Enter your query:")

#     elif file_type in ["Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)"]:
#         uploaded_file = st.file_uploader("Upload your audio/video file:", type=["mp3", "wav", "mp4", "avi"])
#         processing_choice = st.radio("Select processing option:", ["Transcription", "Query based on audio/video content"])
#         if processing_choice == "Query based on audio/video content":
#             user_query = st.text_input("🔍 Enter your query:")

#     # Submit button with an icon
#     if st.button("🚀 Submit"):
#         texts = []
        
#         # Document Processing
#         if uploaded_file:
#             if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#                 text = extract_text_from_file(uploaded_file)
#                 if text:
#                     texts.append(text)

#             elif file_type == "Audio (MP3, WAV)":
#                 if processing_choice == "Transcription":
#                     text = process_audio_no_ffmpeg(uploaded_file)
#                     if text:
#                         texts.append(text)
#                     else:
#                         st.warning("⚠️ No text could be extracted from the uploaded audio.")

#             elif file_type in ["Video (MP4, AVI, MPEG4)"]:
#                 if processing_choice == "Transcription":
#                     text = process_video(uploaded_file, transcribe=True)
#                     if text:
#                         texts.append(text)
#                 elif processing_choice == "Query based on audio/video content":
#                     text = process_video(uploaded_file)
#                     if text:
#                         texts.append(text + " " + user_query)

#         # URL Processing
#         elif url:
#             if "youtube.com" in url or "youtu.be" in url:
#                 youtube_text = extract_text_from_youtube(url)
#                 texts.append(youtube_text + " " + user_query if user_query else youtube_text)
#             else:
#                 webpage_text = extract_text_from_url(url)
#                 texts.append(webpage_text + " " + user_query if user_query else webpage_text)

#         # Process extracted texts with LLM
#         if not texts:
#             st.warning("⚠️ No text could be extracted from the uploaded files or URL.")
#         else:
#             # Embed text and retrieve relevant content
#             embeddings = embed_text(texts)
#             user_query_embedding = embed_text([user_query]) if user_query else None
            
#             # Ensure user_query_embedding is not None
#             if user_query_embedding is not None:
#                 relevant_content_indices_raw = retrieve_relevant_content(embeddings, user_query_embedding)

#                 # Flatten array if needed and convert to list of integers
#                 if isinstance(relevant_content_indices_raw, np.ndarray):
#                     relevant_content_indices = [int(i) for i in relevant_content_indices_raw.ravel()]
#                 elif isinstance(relevant_content_indices_raw, list):
#                     relevant_content_indices = [int(i) for sublist in relevant_content_indices_raw for i in (sublist if isinstance(sublist, list) else [sublist])]
#                 else:
#                     relevant_content_indices = [int(relevant_content_indices_raw)]
                
#                 # Retrieve relevant texts
#                 relevant_texts = [texts[i] for i in relevant_content_indices]

#                 response = get_llm_response(" ".join(relevant_texts))

#                 # Display response with emphasis
#                 st.success("**Response:** " + response)
#             else:
#                 st.warning("⚠️ Please enter a valid query.")

# # Direct LLM Chat Tab
# with tab2:
#     st.header("Direct LLM Chat")
    
#     user_message = st.text_input("💬 Say something:")
    
#     if st.button("✉️ Send"):
#         if user_message:
#             response = get_llm_response(user_message)
#             st.text_area("LLM Response:", value=response, height=150)
#         else:
#             st.warning("⚠️ Please enter a message.")



































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

















































# import os
# import yt_dlp
# import streamlit as st
# import requests
# import numpy as np
# import speech_recognition as sr
# import moviepy.editor as mp
# from bs4 import BeautifulSoup
# import tempfile
# from utils.document_processing import extract_text_from_file
# from utils.embeddings import embed_text
# from utils.retrieval import retrieve_relevant_content
# from models.llm_integration import get_llm_response

# # Set up the Streamlit app
# st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="wide")

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .main {
#         background-color: #f0f0f5;
#     }
#     .sidebar .sidebar-content {
#         background-color: #e8eaf6;
#         border-right: 2px solid #3f51b5;
#     }
#     .stButton>button {
#         background-color: #3f51b5;
#         color: white;
#         border: None;
#         border-radius: 5px;
#         margin: 5px;
#     }
#     .stButton>button:hover {
#         background-color: #303f9f;
#     }
#     .stTextInput {
#         border-radius: 5px;
#         border: 1px solid #3f51b5;
#     }
#     .response-container {
#         margin: 10px 0;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #f8f9fa;
#         border: 1px solid #dee2e6;
#     }
#     .custom-button {
#         padding: 5px 10px;
#         margin: 5px;
#         border: none;
#         border-radius: 5px;
#         background-color: #3f51b5;
#         color: white;
#         cursor: pointer;
#     }
#     .custom-button:hover {
#         background-color: #303f9f;
#     }
#     /* Hide default Streamlit buttons when needed */
#     .stHidden {
#         display: none;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# def create_response_buttons(response, index):
#     """Create custom buttons with JavaScript functionality"""
#     # Generate unique IDs for buttons to avoid conflicts
#     play_btn_id = f"play_btn_{index}"
#     copy_btn_id = f"copy_btn_{index}"
    
#     button_html = f"""
#         <div class="button-container">
#             <button id="{play_btn_id}" class="custom-button" onclick="playResponse('{index}')">
#                 🔊 Play Response
#             </button>
#             <button id="{copy_btn_id}" class="custom-button" onclick="copyResponse('{index}')">
#                 📋 Copy Response
#             </button>
#         </div>
#         <div id="response_{index}" style="display: none;">{response}</div>
#         <script>
#             function playResponse(index) {{
#                 const text = document.getElementById('response_' + index).textContent;
#                 const utterance = new SpeechSynthesisUtterance(text);
#                 window.speechSynthesis.cancel(); // Stop any current speech
#                 window.speechSynthesis.speak(utterance);
#             }}
            
#             function copyResponse(index) {{
#                 const text = document.getElementById('response_' + index).textContent;
#                 navigator.clipboard.writeText(text)
#                     .then(() => {{
#                         // Show temporary success message
#                         const btn = document.getElementById('copy_btn_' + index);
#                         const originalText = btn.innerHTML;
#                         btn.innerHTML = '✓ Copied!';
#                         setTimeout(() => {{
#                             btn.innerHTML = originalText;
#                         }}, 2000);
#                     }})
#                     .catch(err => {{
#                         console.error('Failed to copy text:', err);
#                         alert('Failed to copy text to clipboard');
#                     }});
#             }}
#         </script>
#     """
#     st.markdown(button_html, unsafe_allow_html=True)

# def display_response(response, index):
#     """Display response with interactive buttons"""
#     if response:
#         with st.container():
#             st.markdown(f"**Response:**")
#             st.markdown(response)
#             create_response_buttons(response, index)


# def extract_text_from_url(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = [p.text for p in soup.find_all('p')]
#         return ' '.join(paragraphs)
#     except Exception as e:
#         return f"Error: Could not extract text from URL - {e}"

# def extract_text_from_youtube(url):
#     try:
#         with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             description = info_dict.get("description", "No description available.")
#             return description
#     except Exception as e:
#         return f"Error: Could not extract description from YouTube URL - {e}"

# def transcribe_audio(file_path):
#     recognizer = sr.Recognizer()
#     try:
#         with sr.AudioFile(file_path) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data)
#             return text
#     except Exception as e:
#         return f"Error in audio transcription: {e}"

# def handle_audio_file(uploaded_file):
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
#             tmp_file.write(uploaded_file.getbuffer())
#             tmp_path = tmp_file.name

#         text = transcribe_audio(tmp_path)
#         os.unlink(tmp_path)
#         return text
#     except Exception as e:
#         st.error(f"Error processing audio file: {str(e)}")
#         return None

# def handle_video_file(uploaded_file):
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
#             tmp_file.write(uploaded_file.getbuffer())
#             tmp_path = tmp_file.name

#         video = mp.VideoFileClip(tmp_path)
#         audio_path = tempfile.mktemp(suffix='.wav')
#         video.audio.write_audiofile(audio_path)
        
#         text = transcribe_audio(audio_path)
        
#         video.close()
#         os.unlink(tmp_path)
#         os.unlink(audio_path)
#         return text
#     except Exception as e:
#         st.error(f"Error processing video file: {str(e)}")
#         return None

# # Main app interface
# st.title("🤖 Chat Assistant")
# st.markdown("### Welcome to the AI Chat Assistant!")

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# selected_mode = st.sidebar.radio("Choose your mode:", ("RAG System", "Direct LLM Chat"))

# # RAG System Tab
# if selected_mode == "RAG System":
#     st.header("🗂️ RAG System Chat")

#     file_type = st.selectbox(
#         "Select file type:",
#         options=["PDF", "Word (DOCX)", "TXT", "Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)", "URL"],
#     )

#     uploaded_file = None
#     url = ""
#     user_query = ""
#     processing_choice = None

#     if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#         uploaded_file = st.file_uploader("Upload your document:", type=["pdf", "docx", "txt"])
#         user_query = st.text_input("🔍 Enter your query:", key="rag_query")

#     elif file_type == "URL":
#         url = st.text_input("🌐 Enter URL (YouTube or general website):")
#         user_query = st.text_input("🔍 Enter your query:", key="url_query")

#     elif file_type in ["Audio (MP3, WAV)", "Video (MP4, AVI, MPEG4)"]:
#         file_types = ["mp3", "wav"] if file_type == "Audio (MP3, WAV)" else ["mp4", "avi", "mpeg4"]
#         uploaded_file = st.file_uploader(f"Upload your {file_type.lower()} file:", type=file_types)
#         processing_choice = st.radio("Select processing option:", ["Transcription", "Query based on content"])
#         if processing_choice == "Query based on content":
#             user_query = st.text_input("🔍 Enter your query:", key="media_query")

#     if st.button("🚀 Submit", key="rag_submit"):
#         with st.spinner("Processing..."):
#             texts = []

#             if uploaded_file:
#                 if file_type in ["PDF", "Word (DOCX)", "TXT"]:
#                     text = extract_text_from_file(uploaded_file)
#                     if text:
#                         texts.append(text)

#                 elif file_type == "Audio (MP3, WAV)":
#                     text = handle_audio_file(uploaded_file)
#                     if text:
#                         texts.append(text)
#                     else:
#                         st.warning("⚠️ No text could be extracted from the uploaded audio.")

#                 elif file_type == "Video (MP4, AVI, MPEG4)":
#                     text = handle_video_file(uploaded_file)
#                     if text:
#                         texts.append(text)
#                     else:
#                         st.warning("⚠️ No text could be extracted from the uploaded video.")

#             elif url:
#                 if "youtube.com" in url or "youtu.be" in url:
#                     youtube_text = extract_text_from_youtube(url)
#                     texts.append(youtube_text)
#                 else:
#                     webpage_text = extract_text_from_url(url)
#                     texts.append(webpage_text)

#             if not texts:
#                 st.warning("⚠️ No text could be extracted from the source.")
#             else:
#                 if processing_choice == "Transcription":
#                     st.subheader("Transcription Result:")
#                     display_response(texts[0], "transcription")
#                 elif user_query:
#                     user_query_embedding = embed_text([user_query])
#                     embeddings = embed_text(texts)
#                     relevant_indices = retrieve_relevant_content(embeddings, user_query_embedding)
                    
#                     if isinstance(relevant_indices, np.ndarray):
#                         relevant_indices = relevant_indices.tolist()
#                     if not isinstance(relevant_indices, list):
#                         relevant_indices = [relevant_indices]
                    
#                     relevant_texts = [texts[i] for i in relevant_indices if i < len(texts)]
                    
#                     if relevant_texts:
#                         response = get_llm_response(" ".join(relevant_texts))
#                         st.session_state.current_response = response
#                         display_response(response, "rag")
#                     else:
#                         st.warning("⚠️ No relevant content found for the query.")
#                 else:
#                     st.warning("⚠️ Please enter a query.")
# # Direct LLM Chat Tab
# else:
#     st.header("💬 Direct LLM Chat")
    
#     # Display chat history
#     for role, message in st.session_state.chat_history:
#         with st.container():
#             if role == "user":
#                 st.markdown(f"**You:** {message}")
#             else:
#                 st.markdown(f"**Assistant:** {message}")
#                 if st.button("🔊 Play", key=f"play_hist_{message}"):
#                     play_text(message)

#     user_message = st.text_input("💬 Type your message:", key="direct_message")
#     if st.button("📬 Send", key="direct_submit"):
#         if user_message:
#             # Add user message to chat history
#             st.session_state.chat_history.append(("user", user_message))
            
#             # Get response
#             response = get_llm_response(user_message)
            
#             # Add response to chat history
#             st.session_state.chat_history.append(("assistant", response))
#             st.session_state.current_response = response
#         else:
#             st.warning("⚠️ Please enter a message to send.")
















