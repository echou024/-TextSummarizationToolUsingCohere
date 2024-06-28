import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv('COHERE_API_KEY')
API_URL = 'https://api.cohere.ai/generate'

def summarize_text(text):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'command-xlarge-nightly',  # Use 'command-xlarge-nightly' or another accessible model
        'prompt': f'Summarize the following text: {text}',
        'max_tokens': 50,  # Adjust as needed for your summary length
        'temperature': 0.5,  # Control the creativity of the response
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        if 'text' in result:
            return result['text'].strip()
        else:
            st.error(f"Unexpected response structure: {result}")
            return None
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    st.title("Text Summarization Tool")
    st.write("Enter the text you want to summarize below:")

    input_text = st.text_area("Input Text", height=200)
    
    if st.button("Summarize"):
        if input_text:
            summary = summarize_text(input_text)
            if summary:
                st.subheader("Summary:")
                st.write(summary)
            else:
                st.error("Failed to generate summary.")
        else:
            st.error("Please enter some text to summarize.")

if __name__ == '__main__':
    main()
