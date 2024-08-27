import streamlit as st
import requests
import docx

from langchain.vectorstores import Chroma

st.set_page_config(
    page_title="PJサポートツール",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

# GCPのCloud FunctionsのURLを設定
GCP_FUNCTION_URL1 = 'https://us-central1-silver-agility-431114-r0.cloudfunctions.net/PM-support'
GCP_FUNCTION_URL2 = 'https://us-central1-silver-agility-431114-r0.cloudfunctions.net/generate-task-grouping'

# ワイド表示
st.set_page_config(layout="wide")

# サイドバーの一番上にタイトルを表示
st.sidebar.title("PJサポートツール")

# セレクトボックスのリストを作成
pages = ["1 マニュアル管理", "2 ToDo抽出", "3 PJチャットボット"]

# サイドバーにリンクを表示
for page in pages:
    if st.sidebar.button(page):
        st.experimental_set_query_params(page=page)

# クエリパラメータを取得
query_params = st.experimental_get_query_params()
selected_page = query_params.get("page", [pages[0]])[0]

# 選択されたページに応じてコンテンツを表示
if selected_page == pages[0]:
    st.title(pages[0])
    st.write("マニュアル管理ページです。")
elif selected_page == pages[1]:
    st.title(pages[1])

    # テキストの入力の仕方を設定
    option = st.radio("テキストをどう入力しますか？", ('ベタ打ち', 'ファイルアップロード'))

    # テキストエリアを表示
    if option == 'ベタ打ち':
        # ユーザーが直接テキストを入力
        user_input = st.text_area("メールや議事録のテキストを入力して:", height=300)
    elif option == 'ファイルアップロード':
        # ファイルアップロード
        uploaded_file = st.file_uploader("タスクを抽出したいファイル(.docx / .txt)を選択してください", type=["txt", "docx"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.txt'):
                # txt ファイルの内容を読み取る
                user_input = uploaded_file.getvalue().decode("utf-8")
                st.write("ファイルの内容:")
                st.text_area("", user_input, height=300)
            elif uploaded_file.name.endswith('.docx'):
                # docx ファイルの内容を読み取る
                doc = docx.Document(uploaded_file)
                user_input = "\n".join([para.text for para in doc.paragraphs])
                st.write("ファイルの内容:")
                st.text_area("", user_input, height=300)

    # ToDoリストを作成するボタンが押されたときの処理
    if st.button('ToDoリストを作成する'):
        response1 = requests.post(GCP_FUNCTION_URL1, json={'input_text': user_input})
        if response1.status_code == 200:
            st.session_state.result1 = response1.json().get('output', 'No result found')
        else:
            st.session_state.result1 = f'Error calling the function: {response1.status_code}'

    # ToDoリストを系統化・補完するボタンが押されたときの処理
    if st.button('ToDoリストを系統化・補完する'):
        response2 = requests.post(GCP_FUNCTION_URL2, json={'input_text': user_input})
        if response2.status_code == 200:
            st.session_state.result2 = response2.json().get('output', 'No result found')
        else:
            st.session_state.result2 = f'Error calling the function: {response2.status_code}'

    # 保存された結果を表示
    if 'result1' in st.session_state:
        st.text_area('ToDoリスト:', str(st.session_state.result1), height=300)

    if 'result2' in st.session_state:
        st.text_area('ToDoリスト(系統化・補完後):', str(st.session_state.result2), height=400)
elif selected_page == pages[2]:
    st.title(pages[2])
    st.write("PJチャットボットページです。")