import streamlit as st
from streamlit_chat import message
import requests


import yaml
import openai

import databutton as db

openai.api_key = db.secrets.get("OPENAI_API_KEY")


st.set_page_config(
    page_title="BeerGPT",
    page_icon="twemoji:beer-mug"
)

st.image("https://1cms-img.imgix.net/san-miguel-banner.jpg?auto=compress")


# model_engine = "gpt-3.5-turbo"
model_engine = "gpt-3.5-turbo"


# This is where we set the personality and style of our chatbot
prompt_template = """
    You are a helpful online store order taking chat bot named BeerGPT. Your replies are respectful, direct, and specific.
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
    
    # initiate the information that the bot knows
    st.session_state.prompt.append({"role": "system", "content": prompt_template})
    st.session_state.prompt.append({"role": "system", "content": "You are BeerGPT, you simulate accepting orders of San Miguel Beer Products."})
    st.session_state.prompt.append({"role": "system", "content": """The products are San Miguel Pale Pilsen with price php 100: This is the flagship beer of San Miguel Brewery, known for its crisp and full-bodied taste.
        San Miguel Light with price of php 40: A lighter version of San Miguel Pale Pilsen with lower calorie content and a milder flavor profile.
        San Miguel Super Dry with price of php 110: A dry and refreshing beer with a clean and crisp taste.
        san Miguel Premium All-Malt Beer with price of php 72: A premium beer made exclusively from malted barley, resulting in a rich and flavorful brew.
        San Miguel Flavored Beers with price of php 48: San Miguel Brewery offers a range of flavored beers, including options like San Miguel Apple, San Miguel Lemon, and San Miguel Strawberry, which feature fruit-infused flavors."""})
    st.session_state.prompt.append({"role": "system", "content": "you only accept orders in cases of 24 cans or cases of 6 cans. There are cases of 12 bottles but only for 500 ml products."})
    st.session_state.prompt.append({"role": "system", "content": "once the customer says thank you, display a summary of the order and customer details."})

    # provide an example transaction
    st.session_state.prompt.append({"role": "user", "content": "Hi, i would like to order"})
    st.session_state.prompt.append({"role": "assistant", "content": "Ok, what are you looking to buy?"})
    st.session_state.prompt.append({"role": "user", "content": "Hi, i would like 1 case of san mig light"})
    st.session_state.prompt.append({"role": "assistant", "content": "Ok, here is a summary of the order. do you confirm?"})
    st.session_state.prompt.append({"role": "user", "content": "yes confirmed thank you"})
    st.session_state.prompt.append({"role": "assistant", "content": "here is the summary of your order and your delivery and contact details. Thank you for patronizing us!"})
    
# Send an API request and get a response, note that the interface and parameters have changed compared to the old model

def get_response(input_text):
    
    st.session_state.prompt.append({"role": "user", "content": input_text})

    messages = st.session_state.prompt
    response = openai.ChatCompletion.create(model=model_engine,messages=messages)
    output = response['choices'][0]['message']['content']
    
    
    # When we get an answer back we add that to the message history
    st.session_state.prompt.append({"role": "assistant", "content": output})
    return output





st.header("BeerGPT")
st.markdown("https://github.com/ogbinar")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ","Hello, What products are available?", key="input")
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
        