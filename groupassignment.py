
# Todo - LangChainDeprecationWarning: Importing LLMs from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead: `from langchain_community.llms import OpenAI` To install langchain-community run `pip install -U langchain-community`.

# Todo - add Chat history fuctionality to the code - the AI should also be able to remember the conversation history and respond accordingly (follow-up questions, etc.)

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# import time * This import is not used in the current implementation, but can be used to create a typewriter effect

# Setup Streamlit interface for user input
st.title("Elevator Pitch Generator")
st.markdown("This app generates an elevator pitch for your startup idea. Please enter your startup idea and click the button to generate the elevator pitch.")

# Define API Key and user input field
api_key = st.text_input("OpenAI API Key", type="password")
user_input = st.chat_input("Enter the Job-to-be-done")

# generate_pitch = st.button("Generate Elevator Pitch") * Removed this button in favor of the chat_input function above
st.caption("Powered by OpenAI's GPT-3")
st.divider()
st.markdown("See the generated elevator pitch below:")

# Todo - check if it is better to have the "official" error message from OpenAI
# Todo - fix bug that the API key is displayed as invaild eventhough it is valid
# Function that proofs if the entered key is a valid OpenAI API key
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

# ? Created this for a typewriter effect, but it is not working properly as text is not broken at line breaks, maybe chat_stream would be better
# def typewriter_effect(text):
#     output = st.empty()
#     for i in range(len(text) + 1):
#         output.text(text[:i])
#         time.sleep(0.05)  # Adjust typing speed here

if user_input:
    # if test_api_key(api_key): * This function is not used in the current implementation, but can be used to test the API key
    # Todo - add chat.stream to have a typewriter effect
    # ? Currently with chat.stream, already generated text is displayed repatedly before the new text is generated. How to fix this?
    
    # Identify the pain point
    with st.spinner("Identifying the pain point..."):
        hardest_part = create_prompt(
            system_description="You are an expert in identifying the hardest part of a job to be dobe. The user will give you a job-to-be-done and you need to identify the hardest part of the job-to-be-done. Provide the hardest part of this job.",
            human_description="The job-to-be-done is: {content}",
            content=user_input
        )
        st.markdown('**The hardest part of the job:**')
        st.write(hardest_part)

    # Create the value proposition
    with st.spinner("Creating the value proposition..."):
        value_proposition = create_prompt(
            system_description="You are an expert in transforming the hardest part of a job to be done into a value proposition. The user will give you the hardest part of a job-to-be-done and you need to transform the hardest part of the job-to-be-done into a value proposition.",
            human_description="The hardest part of the job-to-be-done is: {content}",
            content=hardest_part
        )
        st.markdown('**The value proposition:**')
        st.write(value_proposition)

    # Generate the elevator pitch
    with st.spinner("Generating the elevator pitch..."):
        elevator_pitch = create_prompt(
            system_description="You are an expert in generating elevator pitches. The user will give you a value proposition and you need to generare an elevator pitch.",
            human_description="The value proposition is: {content}",
            content=value_proposition
        )
        st.markdown('**Here is the elevator pitch:**')
        st.write(elevator_pitch)