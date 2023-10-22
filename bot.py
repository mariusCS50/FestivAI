import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import pickle
import gradio as gr

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(temperature=0.6)

with open("FAQ.pkl", 'rb') as f: 
    faiss_index = pickle.load(f)

message_history = []

def predict(input):

    docs = faiss_index.similarity_search(input)

    main_content = input + "\n\n"
    for doc in docs:
        main_content += doc.page_content + "\n\n"

    message_history.append({"role": "user", "content": f"{input}"})

    messages.append(HumanMessage(content=main_content))
    ai_response = chat(messages).content
    messages.pop()
    messages.append(HumanMessage(content=input))
    messages.append(AIMessage(content=ai_response))

    message_history.append({"role": "assistant", "content": f"{ai_response}"}) 

    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)] 
    return response

with gr.Blocks() as demo: 

    messages = [
        SystemMessage(
            content="You are a Director of Customer Relation bot and you will answer all the questions that the user has based on the provided document. You NEVER mention the document or mension that the information is from the document, and you HAVE to give an answer even only based on some words, you HAVE to assume an answer, but you need to be as accurate as possible. If you dont know the answer, output 'Sorry, I am unable to give an answer to this query.")
    ]

    chatbot = gr.Chatbot(height=580, show_copy_button=True, avatar_images=(None, "AI.jpg")) 

    with gr.Row(): 
        
        query = gr.Textbox(label="User Input", placeholder="Enter text and press enter", show_label=False, container=False)

    query.submit(predict, query, chatbot)

    query.submit(None, None, query, _js="() => {''}") 
demo.launch()
