day 2- 17th jul
## implementing chat bot using langchain and ollama
so can see in app.py file in chatbot folder containing code 
  a chain of prompt -> llm -> reponse
used ChatPromptTemplate and gemini model for llm and stroutputParser
and seeing tracing in langsmith tracing 

now downloading ollama for running open source models
***
- for using third party configurations like ollama or embedding models we use langchain_community

## using open source model of llama3.2:1b vis ollama
- now the problem i was facing while using llama2 model was it showing:
```
ollama._types.ResponseError: llama-server reported out-of-memory during startup: ggml_backend_cpu_buffer_type_alloc_buffer: failed to allocate buffer of size 2147483648
alloc_tensor_range: failed to allocate CPU buffer of size 2147483648
llama_init_from_model: failed to initialize the context: failed to allocate buffer for kv cache (status code: 500)
```
so llama2 is 3.8 gb on disk
when ollama loads it:
- reads model from disk
- decompress part of it
- creates temporary buffers
- creates kv cache
- iniializes inference engine

  ### now what is kv cache
  suppose it we have already generated: the cat sat
  now model wants o prefict: on
  without a cache, it would reread:
  ```
  The
  The cat
  The cat sat
  ```
  with kv cache model stores useful info in memory: now, when predicting the next word, it resuses the stored information instead of recomputing everything.
  every attention layer creates 3 vectors:
  attention(q,k,v)=softmax(qk/root(d))v
  model stores k and v for every token.

  __why it can become so large__:
  suppose our prompt has 1000 tokens
 each transf



  
