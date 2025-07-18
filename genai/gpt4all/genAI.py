from gpt4all import GPT4All
from fastapi import Body, FastAPI
import requests
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
import weaviate
import weaviate.classes.config as wc

BACKEND_URL = "http://server:1111"
WEAVIATE_HOST = "weaviate"
AI_BACKEND = {"mode": "local"}  # or "cloud"
OLLAMA_API_URL = "https://gpu.aet.cit.tum.de/api/chat/completions"
OLLAMA_API_KEY = "sk-741cb60afc8d499da35726c28be3e054"
OLLAMA_MODEL = "llama3.3:latest"

app = FastAPI()
Instrumentator().instrument(app).expose(app)

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM

class ChatRequest(BaseModel):
    prompt: str

def get_weaviate_collection():
    try:
        client = weaviate.connect_to_custom(
            http_host=WEAVIATE_HOST,
            http_port=8080,
            http_secure=False,
            grpc_host=WEAVIATE_HOST,
            grpc_port=50051,
            grpc_secure=False,
        )
        try:
            return client.collections.get("WikiPage")
        except Exception:
            client.collections.create(
                name="WikiPage",
                properties=[
                    wc.Property(name="title", data_type=wc.DataType.TEXT),
                    wc.Property(name="content", data_type=wc.DataType.TEXT),
                    wc.Property(name="pageId", data_type=wc.DataType.NUMBER),
                ],
            )
            return client.collections.get("WikiPage")
    except Exception:
        return None

@app.post("/update_weaviate")
async def update_weaviate():
    wiki_collection = get_weaviate_collection()
    if not wiki_collection:
        return JSONResponse(
            status_code=503,
            content={"status": "Weaviate unavailable, not updated"}
        )
    try:
        resp = requests.get(f"{BACKEND_URL}/pages", timeout=5)
        resp.raise_for_status()
        pages = resp.json()
        for page in pages:
            data_object = {
                "title": page["title"],
                "content": page["content"],
                "page_id": page["pageId"]
            }
            wiki_collection.data.insert(data_object)
        return {"status": "Weaviate updated with wiki pages"}
    except requests.RequestException as e:
        return JSONResponse(
            status_code=503,
            content={"status": "Backend unavailable, Weaviate not updated", "error": str(e)}
        )

def get_context_from_weaviate(query, limit=3):
    wiki_collection = get_weaviate_collection()
    if not wiki_collection:
        return ""  # No context if collection is unavailable
    response = wiki_collection.query.near_text(query=query, limit=limit)
    context = ""
    for obj in response.objects:
        title = obj.properties.get("title", "")
        content = obj.properties.get("content", "")
        context += f"{title}: {content}\n"
    return context

@app.post("/set_backend")
async def set_backend(mode: str = Body(..., embed=True)):
    if mode not in ("local", "cloud"):
        return JSONResponse(status_code=400, content={"error": "Invalid mode"})
    AI_BACKEND["mode"] = mode
    return {"status": f"AI backend set to {mode}"}

@app.get("/get_backend")
async def get_backend():
    return {"mode": AI_BACKEND["mode"]}

@app.post("/chat")
async def chat(request: ChatRequest):
    context = get_context_from_weaviate(request.prompt)
    if AI_BACKEND["mode"] == "local":
        full_prompt = f"Context:\n{context}\n\nUser: {request.prompt}"
        with model.chat_session():
            response = model.generate(full_prompt, max_tokens=1024)
        return JSONResponse(content={"response": response})
    else:
        # Cloud AI via Ollama API Proxy, include context in prompt
        headers = {
            "Authorization": f"Bearer {OLLAMA_API_KEY}",
            "Content-Type": "application/json"
        }
        prompt_with_context = f"Context:\n{context}\n\nUser: {request.prompt}"
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt_with_context}]
        }
        try:
            resp = requests.post(OLLAMA_API_URL, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            response_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return JSONResponse(content={"response": response_text})
        except Exception as e:
            return JSONResponse(status_code=503, content={"error": str(e)})

if __name__ == "__main__":
    update_weaviate()
    uvicorn.run("genAI:app", host="0.0.0.0", port=5000, reload=True)