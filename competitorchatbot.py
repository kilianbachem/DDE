import streamlit as st
from openai import OpenAI
import time

# Streamlit title for the chatbot
st.title('Welcome to the WHU Company Chatbot! - A Chatbot powered by OpenAI')

# Input fields for API key and user question
api_key = st.text_input('Enter your OpenAI API key', type='password')
user_question = st.chat_input("What's your question?")

# Process the question on button click
if user_question is not None and user_question !="":
    with st.spinner('Processing your question...'):
        # Initialize OpenAI client and create a new conversation thread
        client = OpenAI(api_key=api_key)
        thread = client.beta.threads.create()
        
        # Send the user's question to OpenAI
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question,
        )
        
        # Start processing the question and wait for the completion
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_VQlgXtUa1B0GypJwkfcvsp2x"  # Your Assistant ID
        )
        
        while client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != 'completed':
            time.sleep(3)  # Wait for 3 seconds before checking the status again

        # Retrieve the response once processing is completed
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        output = messages.data[0].content[0].text.value
        st.text_area("Answer", value=output)
