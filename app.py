import streamlit as st
import pandas as pd
import PyPDF2
import io
from generate_videos import generate_video
import time

# Streamlit page configuration
st.set_page_config(page_title="Master's Unlimited Veo 3 Video Generator", layout="wide")

# Title and description
st.title("Master's Bulk Veo 3 Video Generator")
st.write("Paste prompts or upload a PDF to generate 8-second video scenes using Veo 3 API!")

# Proxies from master's list
proxies = [
    {"http": "http://45.12.30.237:80"},
    {"http": "http://170.114.45.57:80"},
    {"http": "http://23.227.38.75:80"},
    {"http": "http://104.16.1.142:80"},
    {"http": "http://45.131.7.163:80"}
]
api_key = "09f5dd9b970eb9a13a8b6d805cbcf597"  # Master's Kie.ai API key
endpoint = "https://api.kie.ai/api/v1/veo/generate"

# Input section
st.header("Enter Prompts or Upload PDF")
input_method = st.radio("Choose input method:", ("Paste Prompts", "Upload PDF"))

prompts = []
if input_method == "Paste Prompts":
    prompt_text = st.text_area("Paste prompts (one per line, e.g., 'Scene 1: A dog running', 'Scene 2: A spaceship landing')")
    if prompt_text:
        prompts = [p.strip() for p in prompt_text.split("\n") if p.strip()]
else:
    uploaded_file = st.file_uploader("Upload PDF with prompts (one per line)", type="pdf")
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            prompts.extend([p.strip() for p in text.split("\n") if p.strip()])

# Generate button
if st.button("Generate Videos"):
    if not prompts:
        st.error("Please provide prompts via text or PDF!")
    else:
        st.info(f"Generating {len(prompts)} video scenes...")
        results = []
        for i, prompt in enumerate(prompts, 1):
            st.write(f"Generating Scene {i}: {prompt}")
            video_url = generate_video(prompt, api_key, endpoint, proxies)
            if video_url:
                results.append({"Scene Number": i, "Prompt": prompt, "Video URL": video_url})
                st.success(f"Scene {i} generated! [Download]({video_url})")
            else:
                results.append({"Scene Number": i, "Prompt": prompt, "Video URL": "Failed"})
                st.error(f"Scene {i} failed to generate!")
            time.sleep(1)  # Avoid overwhelming API

        # Display results table
        st.header("Generated Videos")
        st.dataframe(pd.DataFrame(results))

        # Download all results as CSV
        csv = pd.DataFrame(results).to_csv(index=False)
        st.download_button("Download Results as CSV", csv, "video_results.csv", "text/csv")
