# With this code we will build a Streamlit LLM that can generate text from a user-provided prompt. This app uses the Langchain framework and Streamlit

import streamlit as st
from langchain.llms import OpenAI

st.title("Quickstart LLM App using Langchain")

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Defining a function to authenticate to OpenAI API with the user's key, send a prompt, and get an AI-generated response
# This function accepts the user's prompt as an argument and displays the AI-generated response in a blue box using ```st.info()```
def generate_response(input_text):
    llm = OpenAI(temperature=0.7, api_key=api_key)
    st.info(llm(input_text))

# Using ```st.form()```to create a text box (```st.text_area()```) for user input.
# When the user klicks Submit, the ```generate_response()``` function is called with the user's input as an argument.
# Todo - add a typewriter effect (see LLMChat_tutorial.py)
with st.form("my_form"):
    text = st.text_area("Enter text:", "What are the three key pieces of advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not api_key.startswith("sk-"):
        st.warning("Please enter a valid OpenAI API Key", icon = "⚠️")
    if submitted and api_key.startswith("sk-"):
        generate_response(text)