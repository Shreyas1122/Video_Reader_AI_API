🎥 AI RAG-Based YouTube Video Reader
An AI-powered Retrieval-Augmented Generation (RAG) application that can watch YouTube videos for you and answer your questions based on the content.
Simply provide a YouTube video link, and the system will process it, extract its transcript, store it in a vector database, and let you query the content in natural language.

🚀 Features
🎯 Direct YouTube Link Input – Just paste a YouTube video URL.

📝 Transcript Extraction – Automatically fetches and processes the transcript.

🔍 Vector Store Search – Uses embeddings to retrieve the most relevant parts of the video.

🤖 AI-Powered Answers – Uses LLMs to generate answers from retrieved context.

⚡ Fast & Scalable – Efficient chunking and embedding for quick responses.

📜 Context-Aware – Keeps answers relevant to the video’s content.

🛠️ Tech Stack
Python – Backend processing

LangChain – RAG pipeline

HuggingFace / OpenAI Embeddings – Semantic search

FAISS / Chroma – Vector database

YouTube Transcript API – Transcript fetching

FastAPI / Flask – API layer

📦 Installation
bash
Copy
Edit
# 1️⃣ Clone the repo
git clone https://github.com/yourusername/ai-youtube-video-reader.git
cd ai-youtube-video-reader

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt
⚙️ Environment Variables
Create a .env file in the root directory and set:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key   # optional if using HuggingFace embeddings
▶️ Usage
bash
Copy
Edit
python main.py
Example request (via API or script):

python
Copy
Edit
from video_rag import ask_video

video_url = "https://www.youtube.com/watch?v=abcd1234"
question = "What are the main points discussed in the video?"

answer = ask_video(video_url, question)
print("Answer:", answer)
🔍 How It Works
Extract Transcript – Fetches the transcript from the YouTube link.

Chunk & Embed – Splits transcript into smaller chunks and creates embeddings.

Store in Vector DB – Saves embeddings in FAISS/Chroma for fast retrieval.

RAG Query – Searches the vector DB for relevant chunks.

Generate Answer – Feeds retrieved context to the LLM for a natural answer.

📌 Example
Input:

arduino
Copy
Edit
LINK: https://www.youtube.com/watch?v=dQw4w9WgXcQ  
Question: "What is the key message of the video?"
