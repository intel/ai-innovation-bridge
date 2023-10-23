import streamlit as st
from PIL import Image
import requests

st.title('Robot Maintenance Support Chatbot')

col11, col22= st.columns(2)

with col11:
    image = Image.open('./assets/chat.png')
    st.image(image)
with col22:
    st.markdown("##### The Robot Maintenance Support ChatBot component, SupportBot, is a generative AI question-answering\
        model based on the open-source LLM, gpt4all-j. The performance of this model is augmented by\
            leveraging a similarity search and prompt injection through the Langchain library. ")
    
st.divider()

st.markdown('#### Configure SupportBot')

data = st.text_input('Similiary Search Document Path', value='./store/datasets/supportbot_chatbot/dialogues.txt')

st.divider()
    
st.markdown('#### SupportBot Chat')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to ask SupportBot?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    URL = 'http://supportbot_chatbot:5004/predict'
    DATA = {'data':data, 'user_input':prompt}
    INFERENCE_RESPONSE = requests.post(url = URL, json = DATA)
   
    response = f"{str(INFERENCE_RESPONSE.json().get('SupportBot Response'))}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})