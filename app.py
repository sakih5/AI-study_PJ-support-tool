import streamlit as st
import requests

# GCPのCloud FunctionsのURLを設定
GCP_FUNCTION_URL1 = 'https://us-central1-silver-agility-431114-r0.cloudfunctions.net/PM-support'
GCP_FUNCTION_URL2 = 'https://us-central1-silver-agility-431114-r0.cloudfunctions.net/generate-task-grouping'

# Streamlitアプリのタイトルを設定
st.title('ToDoリスト作成アプリ')

# テキストエリアを表示
user_input = st.text_area(
    'メールや議事録のテキストを入力して:',
    height=400,
)

# ToDoリストを作成するボタンが押されたときの処理
if st.button('ToDoリストを作成する'):
    response1 = requests.post(GCP_FUNCTION_URL1, json={'input_text': user_input})
    if response1.status_code == 200:
        st.session_state.result1 = response1.json().get('output', 'No result found')
    else:
        st.session_state.result1 = f'Error calling the function: {response1.status_code}'

# ToDoリストを系統化・補完するボタンが押されたときの処理
if st.button('ToDoリストを系統化・補完する'):
    response2 = requests.post(GCP_FUNCTION_URL2, json={'input_text': st.session_state.result1})
    if response2.status_code == 200:
        st.session_state.result2 = response2.json().get('output', 'No result found')
    else:
        st.session_state.result2 = f'Error calling the function: {response2.status_code}'

# 保存された結果を表示
if 'result1' in st.session_state:
    st.text_area('ToDoリスト:', str(st.session_state.result1), height=300)

if 'result2' in st.session_state:
    st.text_area('ToDoリスト(系統化・補完後):', str(st.session_state.result2), height=400)