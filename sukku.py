from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
# setting up api
load_dotenv()
api_key = os.getenv("Google_api_key")
prompt = PromptTemplate(
    input_variables=['chat_history', 'question'],
    template="""You are a very kind and friendly AI assistant who doesnt talk a lot.
    You specialize in listening helping the person reflect on theirthoughts and fears etc. 
    do not talk too much. ask questions. try to engage the user into talking more and 
    then analyze and help them reflect on their issues and come to conclusions themselves.
    You are currently having a conversation with a human. 
    Analyze the query given to understand the context and 
    ONLY ANSWER the question or statement given in the last part after the '|' in a kind and compassionate tone with some sense of humor if needed.
    
    chat_history: {chat_history},
    Human: {question}
    ΑΙ:"""
)
llm = ChatGoogleGenerativeAI (model='gemini-pro', google_api_key=api_key)
memory = ConversationBufferWindowMemory (memory_key='chat_history', k=6)
count = 0
llm_chain = LLMChain(
    llm = llm,
    memory = memory,
    prompt = prompt
)

st.set_page_config(
    page_title="youright",
    page_icon="✨",
    layout = "wide"
)
st.title('Sukoon')

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role":"assistant","content":"Hey! how are you?"}
    ]
    count +=1

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        count+=1
    
user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role":"user","content":user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)
        
# Get last 4 messages (excluding the current user prompt)
if count>8 : count = 8
if count > 2: 
    context_messages = st.session_state.messages[-count:-1:2] 
    
else: context_messages=""
    
# Prepare context string
context_text = " | ".join([message["content"] for message in context_messages]) 
if count<3: context_text = context_text+" | "
else: context_text = context_text+" | your last response: "+ st.session_state.messages[-2]["content"] + " | "


if st.session_state.messages[-1]['role']!= 'assistant':
    with st.chat_message('assistant'):
        with st.spinner("just a sec..."):
            #ai_response = llm_chain.predict(question=user_prompt)
            user_prompt = context_text + user_prompt
            ai_response = llm_chain.predict(question=user_prompt)

            st.write(ai_response)
    new_ai_message = {"role":"assistant", "content":ai_response}
    st.session_state.messages.append(new_ai_message)