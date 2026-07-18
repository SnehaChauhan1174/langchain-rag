from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# langchain api key will let us know where the montioring results get stored 
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "langchain-rag")

# prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are a helpful assistant. please response to the user queries"),
        ("user","Question:{question}")
    ]
)

st.title('Langchain demo with openai api')
input_text=st.text_input("search the topic u want")

# open ai llms
llm=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))




