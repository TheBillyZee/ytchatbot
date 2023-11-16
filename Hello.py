import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import os

# Set OpenAI secret key
openai.api_key = st.secrets["OPENAI_KEY"]


def get_transcript(video_url):
    # Extract video id from the URL
    video_id = video_url.split("watch?v=")[1]

    # Fetch the list of all available transcripts of video
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Try and get English transcript if available, else take the first available one
    try:
        transcript = transcript_list.find_transcript(['en'])
    except:
        transcript = transcript_list.find_transcript([t.language_code for t in transcript_list])

    # Fetch the transcript
    transcript_fetched = transcript.fetch()

    # Concatenate all the text fields
    full_transcript_text = " ".join([t['text'] for t in transcript_fetched])

    return full_transcript_text

st.title("YouTube Video Summarizer")
video_url = st.text_input('Enter a YouTube video URL:')
start_summarization = st.button("Summarize Video")

if start_summarization and video_url:
    full_transcript = get_transcript(video_url)
    prompt = f"I read a YouTube video transcript that says: \"{full_transcript}\" I need to summarise the key points from the transcript."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    summary = response['choices'][0]['message']['content'].strip()
    st.subheader("Summary")
    st.write(summary)
