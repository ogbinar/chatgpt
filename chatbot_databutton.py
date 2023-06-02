import streamlit as st
from streamlit_chat import message
import requests


import yaml
import openai

import databutton as db

openai.api_key = db.secrets.get("OPENAI_API_KEY")



st.set_page_config(
    page_title="PunnyGPT",
    page_icon=":robot:"
)



# model_engine = "gpt-3.5-turbo"
model_engine = "gpt-3.5-turbo"


# This is where we set the personality and style of our chatbot
prompt_template = """
        You are PiPunsGPT and tries to answer all questions with Pi puns. 
        You like joking about math, logic, pi, related geeky references. 
        Your jokes are very short, sarcastic, and corny. 
    """

# When calling ChatGPT, we   need to send the entire chat history together
# with the instructions. You see, ChatGPT doesn't know anything about
# your previous conversations so you need to supply that yourself.
# Since Streamlit re-runs the whole script all the time we need to load and
# store our past conversations in what they call session state.
# prompt = st.session_state.get("prompt", None)

if 'prompt' not in st.session_state:
    # This is the format OpenAI expects
    st.session_state['prompt'] = []
    
    st.session_state.prompt.append({"role": "system", "content": prompt_template})
    
# Send an API request and get a response, note that the interface and parameters have changed compared to the old model

def get_response(input_text):
    
    st.session_state.prompt.append({"role": "user", "content": input_text})

    messages = st.session_state.prompt
    response = openai.ChatCompletion.create(model=model_engine,messages=messages)
    output = response['choices'][0]['message']['content']
    
    
    # When we get an answer back we add that to the message history
    st.session_state.prompt.append({"role": "assistant", "content": output})
    return output





st.header("PunnyGPT")
st.markdown("https://github.com/ogbinar")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ","Hello, can tell me a Pi joke?", key="input")
    return input_text 


user_input = get_text()

if user_input:
    output = get_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


# this is to reprint the chat history
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        