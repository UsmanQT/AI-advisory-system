
from flask import Flask, render_template, request
import asyncio
import os
#os.environ['HF_HOME'] = '/Users/usmanq/cache/directory/'
#os.environ['TRANSFORMERS_CACHE'] = '/var/lib/docker'
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

from langchain.text_splitter import CharacterTextSplitter #text splitter
from langchain.embeddings import HuggingFaceEmbeddings #for using HugginFace models
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from langchain.indexes import VectorstoreIndexCreator #vectorize db index with chromadb
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredURLLoader  #load urls into docoument-loader
from langchain.chains import RetrievalQA



import requests

llm2=HuggingFaceHub(repo_id="declare-lab/flan-alpaca-large", model_kwargs={"temperature":0, "max_length":512})



app = Flask(__name__)

async def process_question(q):
    # Simulate some asynchronous processing (e.g., waiting for 3 seconds)
    await asyncio.sleep(3)

    # Replace this with your actual processing logic
    urls = [
    "https://www.gvsu.edu/",
    "https://www.gvsu.edu/about.htm",
    "https://www.gvsu.edu/acad-index.htm",
    "https://www.gvsu.edu/admissions/",
    "https://www.gvsu.edu/admissions/graduate-application-24.htm",
    "https://www.gvsu.edu/library/",
    "https://cal.library.gvsu.edu/hours/"
]
    loader2 = [UnstructuredURLLoader(urls=urls)]
    index2 = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(),
        text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)).from_loaders(loader2)
    

    qa_chain = RetrievalQA.from_chain_type(llm2,retriever=index2.vectorstore.as_retriever(),
                                       return_source_documents=True)
    result = qa_chain({"query": q})

    response = f"Answer: {result['result']}"

    return response


@app.route('/')
def index():
    return render_template('index.html', response=None)

@app.route('/submit_question', methods=['POST'])
async def submit_question():
    question = request.form['question']
    # Process the question here (e.g., provide an answer)
    
    task = asyncio.create_task(process_question(question))
    
    response = await task
    
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True, port= 8080)
