# Import necessary libraries
import os
import pickle
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set the OPENAI_API_KEY environment variable with the value from the .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Open and read the PDF document 'data.pdf' using PyPDF2
reader = PdfReader('res/files/data.pdf')

# Initialize an empty string to store the extracted text
raw_text = ''

# Iterate through each page of the PDF and extract the text
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

# Initialize a CharacterTextSplitter to split the raw text into smaller chunks
text_splitter = CharacterTextSplitter(        
    separator="\n",          # Specify the separator for text splitting
    chunk_size=500,           # Set the size of each text chunk
    chunk_overlap=100,       # Specify the overlap between chunks
    length_function=len,      # Use the 'len' function to measure chunk length
)

# Split the raw text into smaller chunks
texts = text_splitter.split_text(raw_text)

# Initialize OpenAI embeddings with disallowed special characters
embeddings = OpenAIEmbeddings(disallowed_special=())

# Create a vector store (docsearch) from the text chunks and embeddings
docsearch = FAISS.from_texts(texts, embeddings)

# Serialize and save the vector store to a file named 'data.pkl'
with open("res/files/data.pkl", 'wb') as f:
    pickle.dump(docsearch, f)
