# Import necessary libraries
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import pickle
import gradio as gr

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key from the environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create an instance of the ChatOpenAI model with a temperature setting of 0.6
chat = ChatOpenAI(temperature=0.6)

# Load Faiss index from a pickled file
with open("res/files/data.pkl", 'rb') as f:
    faiss_index = pickle.load(f)

# Initialize an empty list to store the message history
message_history = []

# Define a function 'predict' for generating responses
def predict(input):
    # Perform a similarity search using Faiss index
    docs = faiss_index.similarity_search(input)

    # Initialize the main content with the user's input
    main_content = input + "\n\n"

    # Concatenate the content of the similar documents
    for doc in docs:
        main_content += doc.page_content + "\n\n"

    # Append the user's message to the message history
    message_history.append({"role": "user", "content": f"{input}"})

    # Create a HumanMessage object with main content
    messages.append(HumanMessage(content=main_content))

    # Generate an AI response using the ChatOpenAI model
    ai_response = chat(messages).content

    # Remove the HumanMessage and append the user's message and AI response
    messages.pop()
    messages.append(HumanMessage(content=input))
    messages.append(AIMessage(content=ai_response))

    # Append the AI response to the message history as the assistant's reply
    message_history.append({"role": "assistant", "content": f"{ai_response}"})

    # Pair up the user's input with the assistant's response and return as a list of tuples
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)]
    return response

# Create a Gradio Blocks interface for the chatbot
with gr.Blocks() as demo:
    # Initialize the list of messages with a SystemMessage
    messages = [
        SystemMessage(
            content="You are a Director of Customer Relation bot, the central point of interaction with festival-goers, and you will answer all the questions that the user has based on the provided document. You NEVER mention the document or mention that the information is from the document, and you HAVE to give an answer even only based on some words, you HAVE to assume an answer, you need to be as accurate as possible, but try as much as possible to give an answer too. Try to provide an answer as fast as possible, users do not like to wait. You ALWAYS have to answer in the same language as the question asked by the user, you will only answer in another language if precised by the used query or if it's a name of a stall. If the user ask for information about types of drinks, foods or cuisines you should recommend a stall, or more if required, which meet the user's criteria. NEVER refer to the stalls by their number, but by their name. If the user asks or mentions for the location or directions for a stall, answer with a google-maps link that shows the location of that stall,you find in the data file in JSON format, where each 'nr' attribue has two coordinates, the latitude and the longitude, according to the stall. If you don't know the answer, output 'I cannot answer this query at this moment, but you are free to ask them directly throught info@fete-des-vendanges.ch'. If you are greeted by the user with 'Hi','Hello', or any other kind of expression alike, say 'Hello, how can I help you today?'. You also must provide real-time information and language support, you must be able to detect the answer based on synonyms of the words in the query or the meaning of the question asked. If there are missing characters or missing accents in some words, you must be able to find the word meant to be in that context. Even if the input seems like it makes no sense, try and find anything in the provided document which would correspond to the word or query."
        )
    ]

    # Create a chatbot interface
    chatbot = gr.Chatbot(height=580, show_copy_button=True, avatar_images=(None, "res/files/AI.jpg"))

    # Define a text input box for user input
    with gr.Row():
        query = gr.Textbox(label="User Input", placeholder="Enter text and press enter", show_label=False, container=False)

    # Set the 'predict' function as the callback for user input submission
    query.submit(predict, query, chatbot)

    # Create a dummy submission to clear the input field
    query.submit(None, None, query, _js="() => {''}")

# Launch the Gradio Blocks interface
demo.launch()
