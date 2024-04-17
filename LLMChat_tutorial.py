import streamlit as st
import random
import time
from openai import OpenAI

# For creating a basic chat interface, we can use both of the two options below
with st.expander("Basic Chat Interface"):
    with st.chat_message("assistant"):
        st.write("Hello! I am the assistant. How can I help you today?")

    message = st.chat_message("user")
    message.write("I would like to know more about your services.")

# For creating a more advanced chat interface, we can use the chat_input function
with st.expander("Explaining chat_input"):
    prompt = st.chat_input("Please enter your message here")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")

# In the code below we have added a title to our app
# With the list we store the messages and append to it every time the user or bot sends a message
# With the for-loop we iterate through the chat history and display each message in the chat message container (with author role and message content)
with st.expander("Building a bot that mirrors your input"):
    st.title("Echo Bot")
    # Initalize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from chat history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input ( ":=" is used to assign user's input to prompt and check if its empty)
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"Echo: {prompt}"

        # Display assistants response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistants response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

with st.expander("Build a simple chatbot GUI that responds with a random message"):

    # Function to generate random response
    def response_generator():
        response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, Human! Is there anything I can help you with?",
                "Do you need help?"
            ]
        )
        for word in response.split(): # split method splits the string (words above) at the spaces and returns a list of words
            yield word + "" # yield is a keyword that is used like return, except that it saves the state of the function. The next time the function is called, execution continues from the last yield statement.
            time.sleep(0.05) # We add time.sleep here to slow down the response and thereby simulating a typing effect

    st.title("Simple chatbot")

    # Initalize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from chat history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("What's up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)


        #Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator()) # We use the write_stream method to write the streamed response with a typewriter effect
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

with st.expander("Build a ChatGPT-like app"):

    st.title("ChatGPT-like clone")

    api_key = st.text_input("OpenAI API Key", type="password")
    client = OpenAI(api_key=api_key)

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from chat history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("How are you doing?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model = st.session_state["openai_model"],
                messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream = True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
