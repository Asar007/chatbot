import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)


model_path = r"C:\Users\iqbal\Downloads\mistral-7B-v0.1"  # Update this to your extracted Mistral model path


if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model directory not found: {model_path}")


tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load Mistral Model with 4-bit Quantization
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quant_config,
    device_map="auto"
)


faiss_index_path = r"C:\Users\iqbal\chatbot\police_fais.index"
dataset_path = r"C:\Users\iqbal\Downloads\copbot_dataset_cleaned.csv"

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Ensure FAISS index exists
if not os.path.exists(faiss_index_path):
    print("FAISS index not found! Creating one...")

    df = pd.read_csv(dataset_path)
    police_records = df["Question"] + " " + df["Answer"]
    police_records = police_records.tolist()

    embeddings = embedder.encode(police_records, convert_to_numpy=True).astype('float32')

    index = faiss.IndexFlatL2(embeddings.shape[1])  
    index.add(embeddings)

    faiss.write_index(index, faiss_index_path)
    print("FAISS index created and saved!")


index = faiss.read_index(faiss_index_path)

df = pd.read_csv(dataset_path)
police_records = df["Question"] + " " + df["Answer"]
police_records = police_records.tolist()


def retrieve(query, top_k=5):  # Increased from 3 to 5 for more context
    """Retrieve the most relevant police records using FAISS"""
    query_embedding = embedder.encode([query], convert_to_numpy=True).astype('float32')
    distances, indices = index.search(query_embedding, top_k)

    retrieved_docs = []
    for idx in indices[0]:
        if 0 <= idx < len(police_records):
            retrieved_docs.append(police_records[idx].strip())
        else:
            print(f"Warning: Skipping out-of-range index {idx}")

    return retrieved_docs


def generate_response(query):
    """Generate a response using Mistral 7B + retrieved police records"""
    retrieved_docs = retrieve(query, top_k=5)  # Increased from 3 to 5
    context = "\n".join(retrieved_docs) if retrieved_docs else "No relevant police record found."

    # Enhanced prompt format for more accurate responses
    system_message = "You are a police procedure expert. Provide accurate, concise, and direct responses based on the given information. If the information is not sufficient, say so clearly."
    final_prompt = f"{system_message}\n\nInformation: {context}\n\nQuery: {query}\n\nResponse:"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer(final_prompt, return_tensors="pt", truncation=True, max_length=512).to(device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,  # Increased for more detailed responses
            do_sample=True,
            temperature=0.3,  # Reduced for more focused responses
            top_p=0.95,  # Increased for better quality
            repetition_penalty=1.2,  # Increased to avoid repetition
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    # Remove the prompt and get only the answer
    response = response.replace(final_prompt, "").strip()
    
    # Clean up the response
    response = response.replace("Question:", "").replace("Answer:", "").strip()
    
    # If the response is too short or seems incomplete, add a note
    if len(response.split()) < 10:
        response += " (Note: This is a brief response. Please ask for more details if needed.)"
    
    return response

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API endpoint for chat
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = generate_response(message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return jsonify({'error': 'Failed to generate response'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)