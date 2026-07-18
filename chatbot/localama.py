from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

llm = OllamaLLM(model="llama3.2:1b")

# prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are a helpful assistant. please response to the user queries"),
        ("user","Question:{question}")
    ]
)

st.title('Langchain demo with llama3.2:1b')
input_text=st.text_input("search the topic u want")

# open ai llms

output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))
