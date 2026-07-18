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
# LLM Memory Concepts: Model Weights, Inference Engine, Context Window & KV Cache

## Overall Flow

```text
User Prompt
      │
      ▼
Tokenizer
      │
      ▼
Inference Engine (Ollama / vLLM / llama.cpp)
      │
      ├── Load Model Weights
      ├── Allocate KV Cache
      ├── Run Transformer Layers
      └── Generate Tokens
      │
      ▼
Model Response
```

---

# 1. Model Weights

Model weights are the **learned parameters** of the neural network.

- Stored in model files like `.gguf`
- Contain all the knowledge learned during training
- Cannot execute by themselves

Examples:

| Model | Parameters |
|--------|------------|
| llama3.2:1b | 1 Billion |
| llama2 | 7 Billion |

### Think of them as:

> The **brain** of the model.

---

# 2. Inference Engine

The inference engine is the software that **runs** the model.

Examples:

- Ollama
- llama.cpp
- vLLM
- TensorRT-LLM
- LM Studio

Its responsibilities:

- Load model weights
- Allocate RAM
- Create KV Cache
- Execute transformer computations
- Generate tokens

### Analogy

Model weights are like a **PDF file**.

Inference engine is like **Adobe Reader**.

Without the reader, the PDF cannot be opened.

Similarly,

Without an inference engine, the model cannot answer questions.

---

# 3. Context Window

The context window is the **maximum number of tokens the model can process at one time**.

It contains:

```text
Previous Conversation
+
Current Prompt
+
Response Generated So Far
```

Everything together must fit inside the context window.

Example:

```
Context Window = 4096 tokens

Previous chat = 2000
Current prompt = 500
Generated response = 1000

Total = 3500 tokens
```

Still within the limit.

---

# 4. KV Cache

LLMs generate text **one token at a time**.

Without caching:

```text
Predict Token 1

↓

Recompute entire prompt

↓

Predict Token 2

↓

Recompute entire prompt

↓

Predict Token 3

...
```

This would be extremely slow.

Instead, after processing each token, the model stores:

- Key vectors
- Value vectors

These stored vectors form the **KV Cache**.

The cache lets the model reuse previous computations instead of recalculating them.

### Think of it as

The model's **working memory**.

---

# 5. Relationship Between Context Window & KV Cache

Suppose

```
Context Window = 8 tokens
```

Initially

```
Token 1

KV Cache = 1 token
```

Then

```
Token 2

KV Cache = 2 tokens
```

...

Eventually

```
Token 8

KV Cache = 8 tokens
```

Now the window is full.

Generate Token 9.

Instead of

```
1 2 3 4 5 6 7 8 9
```

the model keeps

```
2 3 4 5 6 7 8 9
```

The oldest token is removed.

KV Cache still stores information for only **8 tokens**.

### Important

- Before reaching the limit → KV Cache grows.
- After reaching the limit → KV Cache size remains approximately constant.

---

# 6. Why Larger Context Windows Need More RAM

Suppose

```
Model A

Context = 2K
```

Maximum KV Cache stores

```
2000 tokens
```

Now

```
Model B

Context = 32K
```

Maximum KV Cache stores

```
32000 tokens
```

A larger context window means more tokens can be stored simultaneously, so more RAM is required.

---

# 7. Why `llama2` Failed

When Ollama starts a model, it roughly performs:

```text
Load Model Weights
        ✓

Allocate KV Cache
        ✗

Out of Memory
```

The error

```
failed to allocate buffer for kv cache
```

means Ollama could not allocate enough RAM for the model's working memory.

It never reached the stage of generating a response.

---

# 8. Does the Model Forget?

Yes.

Suppose

```
Context Window = 100 tokens
```

Conversation grows to

```
500 tokens
```

The model can only see something like

```
401 ... 500
```

Everything before that is outside the context window.

The model itself no longer has access to those earlier tokens.

---

# 9. Then How Does ChatGPT Remember Earlier Chats?

The **LLM itself does not remember**.

The application (ChatGPT) helps by reconstructing the prompt.

Common techniques:

### Conversation Summary

```
Long Conversation

↓

Short Summary

↓

Sent to LLM
```

---

### Retrieval (RAG)

```
Large Knowledge Base

↓

Retriever

↓

Relevant Chunks

↓

LLM
```

---

### Persistent Memory

Applications may store long-term user preferences separately and insert only relevant information into the prompt.

The LLM still only sees whatever fits inside its context window.

---

# 10. Memory Usage

Approximate memory usage during inference:

```
Total Memory

≈

Model Weights

+

KV Cache

+

Temporary Buffers
```

This is why two models with similar file sizes may require different amounts of RAM while running.

---

# Real-Life Analogy

Imagine solving a problem on a whiteboard.

- **Model Weights** → Your knowledge in your brain.
- **Inference Engine** → You, performing the calculations.
- **Context Window** → Size of the whiteboard.
- **KV Cache** → Notes already written on the whiteboard.

As long as there is space, you keep writing.

Once the whiteboard becomes full, every new note requires erasing an old one.

---

# Key Takeaways

### Model Weights

- Long-term knowledge
- Learned during training
- Stored in model files

---

### Inference Engine

- Software that executes the model
- Examples:
  - Ollama
  - llama.cpp
  - vLLM
  - TensorRT-LLM

---

### Context Window

- Maximum number of tokens visible to the model
- Includes:
  - Conversation history
  - Current prompt
  - Generated response so far

---

### KV Cache

- Temporary memory
- Stores Key and Value vectors
- Speeds up token generation
- Grows until the context window is full
- Then remains approximately constant in size

---

### Why Memory Errors Occur

Running an LLM requires memory for:

1. Model Weights
2. KV Cache
3. Temporary Buffers

If RAM is insufficient, the inference engine cannot initialize the model, resulting in errors such as:

```
failed to allocate buffer for kv cache
```

---

# One-Line Summary

- **Model Weights** → What the model knows.
- **Inference Engine** → Software that runs the model.
- **Context Window** → Maximum number of tokens the model can consider at once.
- **KV Cache** → Temporary working memory that stores attention information for the current context and avoids recomputing previous tokens.
- **Total Memory ≈ Model Weights + KV Cache + Temporary Buffers.**





  
