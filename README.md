# **Multi-File RAG & LLM Chat System with Streamlit**

This project implements a Retrieval-Augmented Generation (RAG) system with support for multi-file interaction and a simple LLM (Large Language Model) chat interface
using Streamlit. The system allows users to upload various types of files (PDF, DOCX, TXT, MP3, MP4) for retrieval-augmented responses and enables a
simple conversational interface using an LLM (LLaMA 8B via the Groq API) for natural language queries.<br>

#### The application is designed with two core components:<br>
1. RAG (Multi-file Interaction): Retrieve relevant content from multiple uploaded files to provide context-based responses.<br>
2. LLM Chat: Enable users to have a direct conversation with an LLM (LLaMA 8B) for simple queries and interactions.<br><br>
<hr>

### **Features**
1. File Upload & Extraction: Upload and process files (PDF, DOCX, TXT, MP3, MP4).
2. Retrieval-Augmented Generation: Uses LLM and document retrieval for answering queries based on the content of multiple files.
3. Simple LLM Chat: Conversational interface with LLaMA 8B for chatting.
4. Multi-file Support: Handles various file types for retrieval (PDF, DOCX, TXT, MP3, MP4).
5. Groq API Integration: Uses LLaMA 8B model via the Groq API for fast, efficient inference.
6. Streamlit UI: A user-friendly interface for uploading files and interacting with the system.

# **Technologies Used**
1. Streamlit: Framework for building the frontend user interface.
2. LLaMA 8B: Large Language Model via Groq API for handling complex conversational queries.
3. PyPDF2: For text extraction from PDF files.
4. python-docx: For reading DOCX files.
5. moviepy: For transcribing MP4 video files.
6. FAISS: For document retrieval based on file content.

# **Getting Started**
##### Prerequisites
Make sure you have the following installed:
<ul> 
  - Python 3.8+ (preferably in a virtual environment)<br>
  - pip (Python package manager)
</ul>


# **Running the Application**
Start the Streamlit app: <br>
```bash
streamlit run app.py <br>
```
This will launch the Streamlit interface at http://localhost:8501.

# Install the dependencies using:
```bash
pip install -r requirements.txt
```
