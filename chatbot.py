import streamlit as st
from langchain import OpenAI, ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'

# ChromaDBへの接続
chroma_db = Chroma(
    collection_name='text_collection',
    embedding_function=OpenAIEmbeddings(model='text-embedding-ada-002'),
    persist_directory='./.data'
)

# Langchainの設定
llm = OpenAI(model_name="text-davinci-003")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# StreamlitのUI設定
st.title("Langchain + ChromaDB Chat App")

# チャットの履歴を管理するセッションステート
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# チャットの表示
for chat in st.session_state["chat_history"]:
    if chat["type"] == "user":
        st.markdown(f"<div style='text-align: right;'>{chat['message']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left;'>{chat['message']}</div>", unsafe_allow_html=True)

# ユーザーの入力
user_input = st.text_input("Type your message here...", key="input_text")

if st.button("Send"):
    if user_input:
        # ユーザーのメッセージを追加
        st.session_state["chat_history"].append({"type": "user", "message": user_input})

        # AIの応答を生成
        response = conversation.predict(input=user_input)
        st.session_state["chat_history"].append({"type": "ai", "message": response})

        # 入力フィールドをクリア
        st.session_state.input_text = ""

# 古いチャットメッセージが上に押し上げられるため、スクロールを維持
st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)