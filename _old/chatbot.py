import streamlit as st
import api_functions


# (LLM)チャットメモリの初期化 ←if文に入れておくことでセッション間は1度しか実行されない
if "memory" not in st.session_state:
    memory = api_functions.init_memory()
    st.session_state.memory = memory

# (UI)会話履歴を初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# (UI)チャット入力ボックスを表示
user_input = st.chat_input("Ask something about the file.")
if user_input:
    if "memory" in st.session_state:
        # (LLM)メモリに基づく返答の作成
        response, st.session_state.memory = api_functions.chat_with_memory_and_rag(user_input, st.session_state.memory)
        # (UI)会話履歴に追加
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        # (UI)会話履歴に追加
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
        print(response)

# (UI)会話履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])