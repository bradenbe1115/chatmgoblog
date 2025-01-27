import streamlit as st
import requests
import time

background_color = """
    <style>
    .stApp {
        background-color: #00274C;
        color: #FFCB05;
    }
    .stMarkdown {
        color: #FFCB05;
    }
    </style>
"""
st.markdown(background_color, unsafe_allow_html=True)

st.title("ChatMgoBlog")
st.write("This is a RAG application that answers questions about University of Michigan sports using content from Mgoblog")

if prompt := st.chat_input("Let's talk about Michigan sports"):
    
    with st.chat_message("user"):
        st.markdown(prompt)

    start_time = time.perf_counter()
    context = requests.get("http://localhost:5005/user_query", json={"user_query": prompt})
    end_time = time.perf_counter()
    print(end_time-start_time)

    start_time = time.perf_counter()
    response = requests.get("http://localhost:5008/gen_chat_with_context", json={"question": prompt, "context": [x["text"] for x in context.json()]})
    end_time = time.perf_counter()
    print(end_time-start_time)

    with st.chat_message("assistant"):
        st.write([x["text"] for x in context.json()] )
        response = st.write(response.json()["response"]["answer"])