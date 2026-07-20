# when to use @app.post() and when langserve's add_routes
> concened folder - api folder
so we are making api file in which we are using __langserve__ using add_routes
- now we are making apis using add_routes() with passing the app,chain,path
now std fast api route : @app.post()
1.  ```
    @app.post("/essay")
    def generate():
        ...
    ```
2. add_routes() comes from LangServe
 ```
   from langserve import add_routes
    add_routes(
        app,
        prompt | llm,
        path="/essay"
    )
```
now we are telling langserve:
> "I already have a runnable chain. Please automatically expose it as an API."
this creates api routes that simply call chain.invoke(...) behind he scens
### it also creates multiple endpoints:
```
POST /essay/invoke
POST /essay/stream
POST /essay/batch
GET  /essay/input_schema
GET  /essay/output_schema
GET  /essay/config_schema
```
* each path is connected to a different chain

### now for each what is the primary usecase for each:
- FastAPI knows how to expose Python functions as APIs.
- LangServe knows how to expose LangChain Runnables or LangGraoh as APIs.


### use @app.post() when:
we need custom logic before or after the chain'
for example:
```
@app.post("/chat")
def chat(req: ChatRequest):

    # Authenticate user
    authenticate(req.token)

    # Query database
    history = load_chat(req.user_id)

    # Call chain
    response = chain.invoke({
        "history": history,
        "question": req.question
    })

    # Save response
    save_chat(response)

    return response
```
## which approach s used in projects:
- Prototypes, demos, internal AI services → add_routes() is great because it's quick.
- Production applications with authentication, billing, databases, permissions, logging, etc. → Developers often use @app.post() and invoke the chain manually.



