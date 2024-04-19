
# Todo - LangChainDeprecationWarning: Importing LLMs from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead: `from langchain_community.llms import OpenAI` To install langchain-community run `pip install -U langchain-community`.
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import time

# Setup Streamlit interface for user input
st.title("Elevator Pitch Generator")
st.markdown("This app generates an elevator pitch for your startup idea. Please enter your startup idea and click the button to generate the elevator pitch.")

api_key = st.text_input("OpenAI API Key", type="password")

# Todo - Replace text_input with chat_input
user_input = st.chat_input("Enter the Job-to-be-done")
# generate_pitch = st.button("Generate Elevator Pitch")
st.caption("Powered by OpenAI's GPT-3")
st.divider()
st.markdown("See the generated elevator pitch below:")

# Function that proofs if the entered key is a valid OpenAI API key
# Todo - check if it is better to have the "official" error message from OpenAI
# Todo - fix bug that the API key is displayed as invaild eventhough it is valid
# def test_api_key(api_key):
#     """ Function to test if the provided API key is valid by making a simple API call. """
#     try:
#         chat_api = ChatOpenAI(api_key=api_key)
#         response = chat_api.invoke(["Test"])  # Simple test message
#         # Check if the response is successful
#         if response.status_code == 200:
#             st.success("API Key is valid. Generating elevator pitch...")
#             return True
#         else:
#             st.warning("Invalid API Key. Please check your API Key and try again.")
#             return False
#     except Exception as e:
#         # This block catches any kind of exception and logs a generic warning
#         st.warning("Invalid API Key. Please check your API Key and try again.")
#         return False

def create_prompt(system_description, human_description, content):
    system_prompt = SystemMessagePromptTemplate.from_template(system_description)
    human_prompt = HumanMessagePromptTemplate.from_template(human_description)
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    request = chat_prompt.format_prompt(content=content).to_messages()
    chat_api = ChatOpenAI(api_key=api_key)
    return chat_api.invoke(request).content

def typewriter_effect(text):
    output = st.empty()
    for i in range(len(text) + 1):
        output.text(text[:i])
        time.sleep(0.05)  # Adjust typing speed here

if user_input:
    # if test_api_key(api_key):
    # Identify the pain point # Todo - add chat.stream to have a typewriter effect
    with st.spinner("Identifying the pain point..."):
        hardest_part = create_prompt(
            system_description="You are an expert in identifying the hardest part of a job to be dobe. The user will give you a job-to-be-done and you need to identify the hardest part of the job-to-be-done. Provide the hardest part of this job.",
            human_description="The job-to-be-done is: {content}",
            content=user_input
        )
        st.markdown('**The hardest part of the job:**')
        typewriter_effect(hardest_part)

    # Create the value proposition
    with st.spinner("Creating the value proposition..."):
        value_proposition = create_prompt(
            system_description="You are an expert in transforming the hardest part of a job to be done into a value proposition. The user will give you the hardest part of a job-to-be-done and you need to transform the hardest part of the job-to-be-done into a value proposition.",
            human_description="The hardest part of the job-to-be-done is: {content}",
            content=hardest_part
        )
        st.markdown('**The value proposition:**')
        typewriter_effect(value_proposition)

    # Generate the elevator pitch
    with st.spinner("Generating the elevator pitch..."):
        elevator_pitch = create_prompt(
            system_description="You are an expert in generating elevator pitches. The user will give you a value proposition and you need to generare an elevator pitch.",
            human_description="The value proposition is: {content}",
            content=value_proposition
        )
        st.markdown('**Here is the elevator pitch:**')
        typewriter_effect(elevator_pitch)