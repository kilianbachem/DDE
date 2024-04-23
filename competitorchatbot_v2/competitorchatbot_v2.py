import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader

#Initial Page setup
st.set_page_config(page_title="Competitor Chatbot", page_icon="🤖")
st.title ("Competitor Intelligence Chatbot")
st.header("Welcome to the Competitor Intelligence Chatbot! 💬📚")

api_key = st.text_input('Enter your OpenAI API key', type='password')
openai.api_key = api_key

# initialize Session State
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]

@st.cache_resource(show_spinner=False) # Caches the result of the function to optimize performance and avoid reloading data on each app interaction, which is particularly useful in data-intensive operations.
def load_data():
    with st.spinner(text="Loading the WHU Company Database - hang tight! This should take just a few seconds. ⏳"):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt = "You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.'"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index
    
index = load_data()

chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant": # If the last message was from the, generate a response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)