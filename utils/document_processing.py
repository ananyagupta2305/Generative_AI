# utils/document_processing.py
import PyPDF2
import docx
import requests
import os
import speech_recognition as sr
import moviepy.editor as mp

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    elif file.type == "text/plain":
        return extract_text_from_txt(file)
    elif file.type in ["audio/mpeg", "audio/wav"]:
        return process_audio(file)
    elif file.type in ["video/mp4", "video/x-msvideo"]:
        return process_video(file)
    elif file.type == "text/uri-list":
        return extract_text_from_url(file)
    else:
        return ""

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)  # Removed 'with' statement
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ''  # Avoid NoneType errors
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file):
    text = file.read().decode("utf-8")
    return text

def process_audio(file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Audio not understandable."
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service."

def process_video(file):
    # Extracting audio from video
    video = mp.VideoFileClip(file)
    audio_file = "temp_audio.wav"
    video.audio.write_audiofile(audio_file)

    # Now process the extracted audio
    text = process_audio(audio_file)

    # Cleanup temporary audio file
    os.remove(audio_file)

    return text

def extract_text_from_url(file):
    url = file.read().decode("utf-8")
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "Could not retrieve content from URL."
