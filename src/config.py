# General
import os
import streamlit as st

# LangChain
from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

def create_model():
    return ChatGoogleGenerativeAI(
        model=st.secrets["GEMINI_MODEL"],
        max_retries=2,
    )