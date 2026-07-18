day 1 - 16th jul
Langchain
Langsmith- used for mlops
  -  debugging
   - evaluation
  - annotation
Langserve uses api for routes, use fast api- deployment
Chains
Agents and retrieval
Langchain expression language 

## models
So when we implement or access api keys from different llm api keys right like
Gemini or chatgpt or groq all will have diff code implementations for each 
This was the problem with using diff llms api keys 
We need to change whole of that structure 
So there was no standardization
Then langchain said ki if we made some interface that 
```
  from langchain_openai import ChatOpenAI
  model=ChatOpenAI(model=’gpt)
  res=model.invoke(“now divide the result by 1.5”)
  print(res.content)
```
this is model's componenet
now two types of models -- language models and embedding models
embedding model gives vector from text
explore doc to explore which each types of models are available in lang chain

## prompts
- dynmaic and reusable prompts
  prompt=PromptTemplate.from_template('summarize {topic} in {emotion} tone')
  print(prompt.format(topic='cricket', length='fun'))
so now its a generic prompt and we have put kind of placeholders as topic and emotion

## ollama
now ollama is not a model but a tool which is used to run open sorce llms locally on our system now there are two types of models-
  - closed source models
  - open source models
    now llama and google's gemma are the models which are open source means their trained wts we have and we can load them and run our own computer in this our own ram and gpu will be used
    now this ensures data privacy and 100% offline we can run it via ollama
and the api keys calling is calling their server like google's gemin

## chains
chains means pipleine now like:
pdf->llm->summary->llm->structured output
or we can have parallel pipeline also like :
pdf->llm1 and pdf->llm2 then combined reponse goes to llm3 to get another response.

## indexes
indexes connect our application to external knowledge- such as pdfs, webistes or datbases.
 - doc loader
 - text splitter
 - vector store
 - retrivars

eg:
pdf->upload->aws s3->doc loader->pdf-> text splitter-> page1, page2...-> embedding1, embedding2...->
database
now user query will come and retrievar will come into picture finding its embedding then semantic search in database to get the matched pages then with user  query sending to llm to get the response.

## memory
LLM API calls are stateless
now what it means - when we call each rquest then llm has no memeory of previous questions.
so we can have diff types of memory for this problem:
 - conversation buffer memory: stors a transcript of recent messages. freat for short chats but can grow large quickly.
 - conversation buffer window memory: only keeps the last n interactions to avoid excessive token usage.
 - summarizer based memory: periodically summarizes lder chat segments to keep a condensed memory footprint.
 - custom memory: for adnaced use cases, we can store specialized state( user's prefrnces or key facts ) in a custom meory class.

## agents 
reasoning capabilities and tools







