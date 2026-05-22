import streamlit as st


st.set_page_config(page_title="Multi-Task Chatbot", page_icon="🤖")

st.title("Choisir le Chatbot")

def redirect_to_sentiment():
    st.switch_page("pages/sentiment_app.py")

def redirect_to_pandas():
    st.switch_page("pages/pandas_app.py")

st.button("Chatbot Analyse de Sentiment", on_click=redirect_to_sentiment)
st.button("Chatbot Table Question Answering", on_click=redirect_to_pandas)