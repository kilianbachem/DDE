import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Setup Streamlit interface for user input
st.title("Elevator Pitch Generator")
st.markdown("This app generates an elevator pitch for your startup idea. Please enter your startup idea and click the button to generate the elevator pitch.")

api_key = st.text_input("OpenAI API Key", type="password")
job_description = st.text_input("Enter the Job-to-be-done")
generate_pitch = st.button("Generate Elevator Pitch")
st.caption("Powered by OpenAI's GPT-3")
st.divider()
st.markdown("See the generated elevator pitch below:")

def create_prompt(system_description, human_description, content):
    system_prompt = SystemMessagePromptTemplate.from_template(system_description)
    human_prompt = HumanMessagePromptTemplate.from_template(human_description)
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    request = chat_prompt.format_prompt(content=content).to_messages()
    chat_api = ChatOpenAI(api_key=api_key)
    return chat_api.invoke(request).content

if generate_pitch:
    # Identify the pain point
    with st.spinner("Identifying the pain point..."):
        hardest_part = create_prompt(
            system_description="You are an expert in identifying the hardest part of a job. Provide the hardest part of this job.",
            human_description="The job-to-be-done is: {content}",
            content=job_description
        )
        st.markdown('**The hardest part of the job:**')
        st.write(hardest_part)

    # Create the value proposition
    with st.spinner("Creating the value proposition..."):
        value_proposition = create_prompt(
            system_description="Transform the hardest part of a job into a value proposition.",
            human_description="The hardest part of the job-to-be-done is: {content}",
            content=hardest_part
        )
        st.markdown('**The value proposition:**')
        st.write(value_proposition)

    # Generate the elevator pitch
    with st.spinner("Generating the elevator pitch..."):
        elevator_pitch = create_prompt(
            system_description="Generate an elevator pitch from a value proposition.",
            human_description="The value proposition is: {content}",
            content=value_proposition
        )
        st.markdown('**Here is the elevator pitch:**')
        st.write(elevator_pitch)
