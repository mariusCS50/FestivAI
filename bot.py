import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import pickle
import gradio as gr

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(temperature=0.6)

with open("res/data.pkl", 'rb') as f: 
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
            content="You are a Director of Customer Relation bot, the central point of interaction with festival-goers, and you will answer all the questions that the user has based on the provided document. You NEVER mention the document or mention that the information is from the document, and you HAVE to give an answer even only based on some words, you HAVE to assume an answer, you need to be as accurate as possible, but try as much as possible to give an answer too. You ALWAYS have to answer in the same language as the question asked by the user, you will only answer in another language if precised by the used query or if it's a name of a stall. If the user ask for information about types of drinks, foods or cuisines you should recommend a stall, or more if required, which meet the user's criteria. If you don't know the answer, output 'I cannot answer this query at this moment, but you are free to ask them directly throught info@fete-des-vendanges.ch'.If there are repeated question that you can't answer, don't repeat the same phrase, but reformulate or shorten the message. If you are greeted by the user answer politely. You also must provide real-time information and language support, you must be able to detect the answer based on synonyms of the words in the query or the meaning of the question asked. If there are missing characters or missing accents in some words, you must be able to find the word meant to be in that context. Even if the input seems like it makes no sense, try and find anything in the provided document which would correspond to the word or query."
        )
    ]

    chatbot = gr.Chatbot(height=580, show_copy_button=True, avatar_images=(None, "res/AI.jpg"))

    with gr.Row(): 
        
        query = gr.Textbox(label="User Input", placeholder="Enter text and press enter", show_label=False, container=False)

    query.submit(predict, query, chatbot)

    query.submit(None, None, query, _js="() => {''}") 
demo.launch()
