from langchain_community.vectorstores import FAISS
import warnings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
import os
from fastapi import FastAPI
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from decouple import config 
from langchain_google_genai import GoogleGenerativeAI
import re


warnings.filterwarnings("ignore", category=FutureWarning)

SECRET_KEY =config('OPEN_AI_API_KEY')

# Model
llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=SECRET_KEY)

app = FastAPI()

#object 
class Query(BaseModel):
    Question:str
    LINK:str

#Extract Video ID FROM URL 

def extract_video_id(url: str) -> str:
    match = re.search(
        r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)', url)
    return match.group(1) if match else None


def error_throw(var):
    return var
try:
    @app.post("/getvideo")
    def process_video_transcript(videodetails : Query):
        video_id = extract_video_id(videodetails.LINK)
        ytt_api = YouTubeTranscriptApi()
        transcriptlist = ytt_api.fetch(video_id, languages=['en'])
        transcript = "".join(i.text for i in transcriptlist)

    # Text Splitters for the document splitting
        splitters = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=10
        )
        chunks = splitters.create_documents([transcript])

    # Vector embedding and searching starts here
        retriver = FAISS.from_documents(
        documents=chunks,
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        )

        output = retriver.as_retriever(
        search_type="similarity",
        search_kwags={"k": 2}
       )

        result = output.invoke(videodetails.Question)
        print("the result string is as follows ")
        context = " ".join(str(d.page_content) for d in result)

        chatmessage = ChatPromptTemplate.from_messages([
        ("system", "You are helpful Kind assistant ! With the help of following Context {context} create a well structured and well formatted summary answer  for Question ! IF the Context is insufficient just say i don't know,i can answer you realated to Video  Data ON which I Have Trained or Try to Give Relevant Answer based on the Question and context.But if someone Greets you or ask you about youself as them as you are video AI Reader  Developed By shreyas! "),
        ("human", "{question}")
    ])

        final_prompt = chatmessage.invoke({"context": context, "question": videodetails.Question})

        resultofllm = llm.invoke(final_prompt)
        print("AI ANSWER STARTS FROM HERE")
        print(resultofllm)
        return resultofllm
except TranscriptsDisabled:
    print("No captions available for this video.")
    error_throw("No captions available for this video.")
except Exception as e:
    print("An error occurred:")
    error_throw("No captions available for this video.")


@app.get("/")
def read_root():
    return {"message": "App is running successfully!"}





