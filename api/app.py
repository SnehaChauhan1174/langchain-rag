from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
import uvicorn
import os
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

app=FastAPI(
    title="Langchain server",
    version="1.0",
    description="a simple api server"
)



## gen ai model with key
model=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
## ollama
llm=OllamaLLM(model="llama3.2:1b")

prompt1=ChatPromptTemplate.from_template("write me an essay about {topic} with 100 words")
prompt2=ChatPromptTemplate.from_template("write me a poem about {topic} with 100 words")

add_routes(
    app,
    model,
    path="/gemini"
)

add_routes(
    app,
    prompt1|model,
    path="/essay"
)

add_routes(
    app,
    prompt2|llm,
    path="/poem"
)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)






