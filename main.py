import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment

# Function to transcribe video to text
def transcribe_video_to_text(video_file_path):
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

# Streamlit app interface
st.title('Video to Text Transcription')
st.header('Upload a video file for transcription')

uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov", "mkv"])
if uploaded_file is not None:
    video_file_path = uploaded_file.name
    with open(video_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video(video_file_path)
    if st.button('Transcribe Video'):
        st.text('Processing...')
        transcription = transcribe_video_to_text(video_file_path)
        st.text_area("Transcription", transcription, height=300)
