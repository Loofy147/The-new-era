from flask import Flask, request, jsonify
from pathlib import Path<<<<<< feature/prompt-memory-vector-search
from src.prompt_memory import PromptMemory
======
from src import PromptMemory
>>>>> main

app = Flask(__name__)

storage_path = Path("prompts.json")
index_path = Path("prompt_index.faiss")
prompt_memory = PromptMemory(storage_path, index_path)

@app.route("/add", methods=["POST"])
def add_prompt():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt not provided"}), 400
    prompt_memory.add(prompt)
    return jsonify({"message": "Prompt added successfully"}), 201

@app.route("/search", methods=["POST"])
def search_prompts():
    data = request.get_json()
    query = data.get("query")
    k = data.get("k", 5)
    if not query:
        return jsonify({"error": "Query not provided"}), 400
    results = prompt_memory.search(query, k)
    return jsonify({"results": results}), 200

@app.route("/prompts", methods=["GET"])
def get_all_prompts():
    prompts = prompt_memory.get_all()
    return jsonify({"prompts": prompts}), 200

if __name__ == "__main__":
    app.run(debug=True)
