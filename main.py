import os
import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment


def transcribe_video_to_text(video_file_path: str) -> str:
    try:
        video = mp.VideoFileClip(video_file_path)
        audio = video.audio
        audio_file_path = "extracted_audio.wav"
        audio.write_audiofile(audio_file_path)
        recognizer = sr.Recognizer()
        audio_segment = AudioSegment.from_wav(audio_file_path)
        chunk_length_ms = 15000  # 15 seconds in milliseconds
        chunks = [audio_segment[i:i + chunk_length_ms] for i in range(0, len(audio_segment), chunk_length_ms)]
        full_text = ""
        for i, chunk in enumerate(chunks):
            chunk.export("temp_chunk.wav", format="wav")
            with sr.AudioFile("temp_chunk.wav") as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='es-ES')
                    full_text += text + " "
                except sr.UnknownValueError:
                    print(f"Google Speech Recognition could not understand audio chunk {i}")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
        return full_text.strip()
    except Exception as e:
        return str(e)


def transcribe_audio_to_text(audio_file_path: str) -> str:
    try:
        recognizer = sr.Recognizer()
        audio_segment = AudioSegment.from_file(audio_file_path)
        chunk_length_ms = 15000  # 15 seconds in milliseconds
        chunks = [audio_segment[i:i + chunk_length_ms] for i in range(0, len(audio_segment), chunk_length_ms)]
        full_text = ""
        for i, chunk in enumerate(chunks):
            chunk.export("temp_chunk.wav", format="wav")
            with sr.AudioFile("temp_chunk.wav") as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='es-ES')
                    full_text += text + " "
                except sr.UnknownValueError:
                    print(f"Google Speech Recognition could not understand audio chunk {i}")
                except sr.RequestError as e:
                    st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return full_text.strip()
    except Exception as e:
        return str(e)


# Streamlit app interface
st.title('Video / Audio to Text Transcription')
st.header('Upload a video or audio file for transcription')
audio_extensions = ["wav", "mp3", "aac", "flac"]
video_extensions = ["mp4", "avi", "mov", "mkv"]
accepted_extensions = audio_extensions + video_extensions
uploaded_file = st.file_uploader("Choose a file...", type=accepted_extensions)
if uploaded_file is not None:
    file_path = uploaded_file.name
    file_extension = os.path.splitext(file_path)[1].lower().replace('.', '')
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video(file_path)
    if st.button('Transcribe'):
        st.text('Processing...')
        if file_extension in audio_extensions:
            transcription = transcribe_audio_to_text(file_path)
        elif file_extension in video_extensions:
            transcription = transcribe_video_to_text(file_path)
        st.text_area("Transcription", transcription, height=300)
