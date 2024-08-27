from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
import os


def get_response_from_llm(human_input):
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        temperature=0.2, model_name="Mixtral-8x7b-32768", groq_api_key=api_key
    )

    response = llm.predict(human_input)
    return response
