## rag pipeline
### 1. Loading the data
- TextLoader
- WebBaseLoader
- PyPdfLoader

### 2. chunking the data
Used text_splitter with defining chunk size and chunk overlap

### 3. vector embeddings
we have usd OllamaEmbeddings with ```nomic-embed-text``` model 

### 4. Vector store
used Chromadb and faiss and then simantic search

## Retriever stuff
suppose we have retrieved documents
after retrieval, we might get: ```docs = retriever.invoke("What is attention?")```
which returns some documents like doc1,doc2,doc3
now question is:
### how do we give all of this to the LLM?
- doing it manually, looping thru documents -> extracting -> joining hem together -> building the prompt -> sending to the llm

__That's exactly what ```create_stuf_documents_chain()``` automates__
when we write: 
```
doc_chain = create_stuff_documents_chain(
    llm,
    prompt
)
```
create_stuff_documents_chain() automatically creates something like
```
Answer the question based only on the following context.

Context:

Attention is...

Transformers...

Multi-head attention...

Question:
What is attention?
```
## Where does this fit in a RAG pipeline?
```
                User Question
                      │
                      ▼
                 Retriever
                      │
          Retrieved Documents
                      │
                      ▼
      create_stuff_documents_chain
          (joins documents)
                      │
                      ▼
             Builds Prompt
                      │
                      ▼
                   LLM
                      │
                      ▼
                Final Answer
```
