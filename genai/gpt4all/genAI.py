from gpt4all import GPT4All
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    with model.chat_session():
        response = model.generate(request.prompt, max_tokens=1024)
    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    uvicorn.run("genAI:app", host="0.0.0.0", port=5000, reload=True)