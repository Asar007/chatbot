AI-Powered Chatbot with Semantic Search
An intelligent, full-stack chatbot application that leverages a Retrieval-Augmented Generation (RAG) architecture to provide highly accurate and contextually relevant responses. Unlike traditional chatbots that rely on keyword matching, this project uses semantic search powered by vector embeddings to understand the true intent behind user queries.

## Key Features
 Semantic Understanding: Utilizes sentence-transformer models to convert both the dataset and user queries into dense vector embeddings, capturing deep contextual meaning.

 High-Speed Retrieval: Employs a FAISS (Facebook AI Similarity Search) vector index for efficient, sub-second retrieval of the most relevant information from the knowledge base.

 RAG Architecture: Implements a modern Retrieval-Augmented Generation pipeline to find relevant context and deliver accurate, nuanced answers.

 Interactive Web UI: A clean and responsive frontend built with HTML, CSS, and vanilla JavaScript for a seamless user experience.

 Python Backend: A robust backend powered by Flask to handle API requests, query processing, and communication with the vector database.

## Architecture Overview
The project is divided into two main stages: Offline Indexing and Online Inference.

### 1. Offline Indexing
First, the knowledge base (copbot_dataset_cleaned.csv) is processed. Each entry is passed through the all-MiniLM-L6-v2 sentence-transformer model to generate a 384-dimensional vector embedding. These embeddings are then indexed and saved in a FAISS index file for fast retrieval.

### 2. Online Inference (Live Chat)
When a user sends a message, the following happens in real-time:

The user's query is converted into a vector embedding using the same sentence-transformer model.

This query vector is used to search the FAISS index for the top 'k' most similar vectors (i.e., the most relevant pieces of information from the original dataset).

The context associated with these top vectors is retrieved.

This retrieved context is used to generate a precise and relevant response, which is sent back to the user.

## Technology Stack
Backend: Python, Flask

Frontend: HTML, CSS, JavaScript

ML/AI Libraries:

sentence-transformers (for generating embeddings)

faiss-cpu (for vector indexing and search)

pandas (for data handling)

Environment: venv

## Project Structure
chatbot/
├── backend.py                 # Flask backend with API endpoints and RAG logic
├── index.html                 # Main HTML page for the chat interface
├── script.js                  # Frontend JavaScript for handling user interaction
├── styles.css                 # CSS for styling the web interface
├── copbot_dataset_cleaned.csv # The source dataset
├── requirements.txt           # List of Python dependencies
├── create_index.py            # Script for offline data processing and FAISS index creation
└── faiss_index.bin            # The generated vector index file
## Installation & Usage
Follow these steps to set up and run the project locally.

### Prerequisites
Python 3.9 or higher

pip and venv

### 1. Clone the Repository
Bash

git clone https://github.com/Asar007/chatbot.git
cd chatbot
### 2. Create a Virtual Environment
Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
### 3. Install Dependencies
Install all the required Python packages.

Bash

pip install -r requirements.txt
### 4. Create the Vector Index
Run the one-time script to process the dataset and create the FAISS index file.

Bash

python create_index.py
This will generate the faiss_index.bin file.

### 5. Run the Backend Server
Start the Flask application.

Bash

python backend.py
The server will start, typically on http://127.0.0.1:5000.

### 6. Access the Chatbot
Open the index.html file in your web browser to begin chatting.

## Contributing
Contributions are welcome! Please feel free to fork the repository, make improvements, and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more deta
