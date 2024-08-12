import streamlit as st
import requests

# GCPのCloud FunctionsのURLを設定
GCP_FUNCTION_URL1 = 'https://us-central1-silver-agility-431114-r0.cloudfunctions.net/PM-support'
GCP_FUNCTION_URL2 = 'https://us-central1-silver-agility-431114-r0.cloudfunctions.net/generate-task-grouping'

# Streamlitアプリのタイトルを設定
st.title('ToDoリスト作成アプリ')

# テキストボックスの高さを計算する関数
def calculate_height(text, min_height=100, max_height=400):
    lines = text.split('\n')
    num_lines = len(lines)
    height_per_line = 20  # 各行の高さ（ピクセル）
    height = min_height + num_lines * height_per_line
    return min(height, max_height)

# テキストエリアの初期値と高さをセッションステートで管理
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''
if 'text_area_height' not in st.session_state:
    st.session_state.text_area_height = calculate_height(st.session_state.user_input)

# テキストエリアを表示
user_input = st.text_area(
    'メールや議事録のテキストを入力して:',
    value=st.session_state.user_input,
    height=st.session_state.text_area_height,
    on_change=lambda: st.session_state.update({'text_area_height': calculate_height(st.session_state.user_input)})
    )

# テキストエリアの内容を更新
st.session_state.user_input = user_input
st.session_state.text_area_height = calculate_height(user_input)

# エンターボタンを配置
if st.button('ToDoリストを作成する'):
    # GCPクラウドファンクションを呼び出す
    response = requests.post(GCP_FUNCTION_URL1, json={'input_text': user_input})
    if response.status_code == 200:
        result = response.json().get('output', 'No result found')
        # 出力結果をテキストボックスに表示
        st.text_area('出力結果:', str(result), height=calculate_height(str(result)))
    else:
        result = 'No result found'
        st.text_area('出力結果:', f'Error calling the function: {response.status_code}')

# エンターボタンを配置
if st.button('ToDoリストを系統化・補完する'):
    # GCPクラウドファンクションを呼び出す
    response = requests.post(GCP_FUNCTION_URL2, json={'input_text': str(result)})
    if response.status_code == 200:
        result = response.json().get('output', 'No result found')
        # 出力結果をテキストボックスに表示
        st.text_area('出力結果:', str(result), height=calculate_height(str(result)))
    else:
        result = 'No result found'
        st.text_area('出力結果:', f'Error calling the function: {response.status_code}')

