import os
import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment

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
