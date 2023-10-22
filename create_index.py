import os
import pickle
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

'''enter your openai api key'''
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

'''Add the path to your pdf file'''
reader = PdfReader('FAQ_eng.pdf')

raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

'''Divide the input data into chunks
    This will help in reducing the embedding size as we will se in the code
    as well as reduce the token size for the query,'''
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 500,
    chunk_overlap  = 100,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)


embeddings = OpenAIEmbeddings(disallowed_special=())
docsearch = FAISS.from_texts(texts, embeddings)


with open("FAQ_eng.pkl", 'wb') as f:
    pickle.dump(docsearch, f)
