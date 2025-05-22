from gpt4all import GPT4All
from flask import Flask, request, jsonify

app = Flask(__name__)
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    with model.chat_session():
        response = model.generate(prompt, max_tokens=1024)
    return jsonify({"response": response})

if __name__ == "__main__":
    # Start REST API
    app.run(host="0.0.0.0", port=5000)