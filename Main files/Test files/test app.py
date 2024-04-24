import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

if "chat history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Streaming bot", page_icon="🤖")

st.title("Streaming bot")

api_key = st.text_input("OpenAI API Key", type="password")

# get response
def create_prompt(system_description, human_description, content):
    system_prompt = SystemMessagePromptTemplate.from_template(system_description)
    human_prompt = HumanMessagePromptTemplate.from_template(human_description)
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    request = chat_prompt.format_prompt(content=content).to_messages()
    chat_api = ChatOpenAI(api_key=api_key)
    return chat_api.stream(request).content


#conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

#user input
job_description = st.chat_input("Enter the Job-to-be-done")
if job_description is not None and job_description != "":
    st.session_state.chat_history.append(HumanMessage(job_description))

    with st.chat_message("user"):
        st.write(job_description)

    with st.chat_message("assistant"):
        ai_response = st.write_stream(create_prompt(
            st.session_state.chat_history,
            system_description="You are an expert in identifying the hardest part of a job to be done. The user will give you a job-to-be-done and you need to identify the hardest part of the job-to-be-done. Provide the hardest part of this job.",
            human_description="The job-to-be-done is: {content}",
            content=job_description
            ))

    st.session_state.chat_history.append(AIMessage(ai_response))