from flask import Flask, request, jsonify, send_from_directory
import openai
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, OpenAI 
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv
import requests
from io import BytesIO

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

openai.api_key = os.getenv("OPENAI_KEY")

PDF_URL = "https://drive.google.com/uc?export=download&id=146Mad_ka8HwkntGxtEKPjLjAnEJfEvHs"

docsearch = None
chain = None

def fetch_and_process_pdf():
    global docsearch, chain
    
    try:
        response = requests.get(PDF_URL)
        response.raise_for_status()  
        pdf_file = BytesIO(response.content)

        pdf_reader = PdfReader(pdf_file)
        raw_text = ''
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text
        
        # Split text and create FAISS index
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(raw_text)
        embeddings = OpenAIEmbeddings()
        docsearch = FAISS.from_texts(texts, embeddings)

        
        chain = load_qa_chain(OpenAI(), chain_type="stuff")
        
        print("PDF fetched and processed successfully")

    except requests.RequestException as e:
        print(f"Failed to fetch PDF: {str(e)}")

fetch_and_process_pdf()

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    if docsearch is None or chain is None:
        return jsonify({"error": "No document loaded. Please contact the administrator."}), 400
    
    data = request.json
    query = data.get('query', '')

    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    
    return jsonify({"answer": answer}), 200

if __name__ == '__main__':
    app.run(debug=True)
