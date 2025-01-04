#%%
import psycopg2
conn=psycopg2.connect(host="localhost",database="postgres",user="postgres",password="Porus04$",)
cur=conn.cursor()

#%%

ref= {"inventory":"https://drive.google.com/uc?export=download&id=1mT4XlNU6LBMqklHrO6-yAXqtqx70VfCO", 
      "store": "https://drive.google.com/uc?export=download&id=1dJPSVnJa7_njPKlDKathRKQ5U7E3594L/"}

#%%

cur.execute("CREATE TABLE Manual (Role VARCHAR(20), Url VARCHAR);")

#%%

for i in ref.keys():
    t=(i,ref[i])
    cur.execute("INSERT INTO Manual VALUES"+str(t))



#%%

inp_role="inventory manager" #You have to get it from the login page
flag= False #THis means you have got a new input
link="" #Drive link for new manual, empty if no new manual
def get_url(inp_role,flag,link):
    if(flag):
        global ref
        if(inp_role not in ref.keys()):
            ref[inp_role]=link #insert
            t=(inp_role,link)
            cur.execute("INSERT INTO Manual VALUES"+str(t))
            return link
        else:
            ref[inp_role]=link #update
            cur.execute("UPDATE Manual SET Url= '%s' WHERE Role='%s';" %(link,inp_role))
            return link
    else:
        cur.execute("Select * From Manual where Role='%s'" %(inp_role)) 
        pdf_url=cur.fetchone()[1]
        print(pdf_url)
        return pdf_url

PDF_URL=get_url(inp_role,flag,link)


#%%

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

openai.api_key = os.getenv("OPENAI_API_KEY")


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



def ask_question():
    if docsearch is None or chain is None:
        print("No such document")
    query = "What are the precautionary steps to be followed when entering the office"

    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    
    print(answer)

    

ask_question()