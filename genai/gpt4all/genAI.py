from gpt4all import GPT4All
from fastapi import FastAPI, requests
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import weaviate

WEAVIATE_URL = "http://weaviate:8080"
BACKEND_URL = "http://backend:5000"

app = FastAPI()
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM

# Connect to Weaviate instance
weaviate_client = weaviate.Client(WEAVIATE_URL)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/update_weaviate")
async def update_weaviate():
    resp = requests.get(f"{BACKEND_URL}/pages")
    resp.raise_for_status()
    pages = resp.json()
    for page in pages:
        data_object = {
            "title": page["title"],
            "content": page["content"],
            "page_id": page["pageId"]
        }
        weaviate_client.data_object.create(
            data_object,
            class_name="WikiPage"
        )
    return {"status": "Weaviate updated with wiki pages"}

def get_context_from_weaviate(query, limit=3):
    # Simple semantic search in Weaviate
    result = weaviate_client.query.get("WikiPage", ["title", "content"]) \
        .with_near_text({"concepts": [query]}) \
        .with_limit(limit) \
        .do()
    context = ""
    for obj in result["data"]["Get"]["WikiPage"]:
        context += f"{obj['title']}: {obj['content']}\n"
    return context

@app.post("/chat")
async def chat(request: ChatRequest):
    # Query Weaviate for context
    context = get_context_from_weaviate(request.prompt)
    full_prompt = f"Context:\n{context}\n\nUser: {request.prompt}"
    with model.chat_session():
        response = model.generate(full_prompt, max_tokens=1024)
    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    update_weaviate()  # Initial update of Weaviate with wiki pages
    uvicorn.run("genAI:app", host="0.0.0.0", port=5000, reload=True)