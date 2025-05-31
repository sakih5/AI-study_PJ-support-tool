# デプロイ時には以下の3行を有効化すること
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st

from pathlib import Path
import pandas as pd

import api_functions
import data_process_operation_manuals
import data_process_project_logs
import streamlit_components


# グローバル変数の設定
TOOL_NAME = "タスク設計サポートツール"
OPERATION_MANUALS_PATH = Path('Operation manuals')
PROJECT_LOGS_PATH = Path('Project logs')

# クラスをインスタンス化
manual_process = streamlit_components.ManualProcess()
project_log_process = streamlit_components.ProjectLogProcess()
css_style = streamlit_components.CSSStyle()

# Streamlitのページ設定
st.set_page_config(
    page_title=TOOL_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSSをStreamlitに反映
st.markdown(css_style.button_css, unsafe_allow_html=True)
st.markdown(css_style.heading_css, unsafe_allow_html=True)
st.markdown(css_style.paragraph_css, unsafe_allow_html=True)

# サイドバーの一番上にタイトルを表示
st.sidebar.markdown(f"<h2>{TOOL_NAME}</h2>", unsafe_allow_html=True)

# ボタンのリストを作成
pages = ["1 マニュアル管理(規定フォーマット)",
         "2 マニュアル管理(フリーフォーマット)",
         "3 ToDo抽出",
         "4 関連マニュアル検索(規定フォーマットのみ)",
         "5 PJチャットボット"]

# 初期化 - セッションステートでページを管理
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = pages[0]

# サイドバーにリンクを表示
for page in pages:
    if st.sidebar.button(label=page):
        st.session_state.selected_page = page

# 現在選択されているページを取得
selected_page = st.session_state.selected_page


# 選択されたページに応じてコンテンツを表示
# 1 マニュアル管理(規定フォーマット)ページ
if selected_page == pages[0]:
    st.title(pages[0])
    st.markdown("<p>こちらは、マニュアル管理ページです。マニュアルの追加・削除ができます。</p>", unsafe_allow_html=True)
    
    # データの読み込み
    files = OPERATION_MANUALS_PATH.glob("*.xlsx")
    files = [file.name for file in files] # ファイル名のみ取得

    st.markdown("<h2>1. 確認 or 編集したいマニュアルファイルを選択してください。</h2>", unsafe_allow_html=True)
    file = st.selectbox('hogehoge', files, label_visibility = 'hidden') # label_visibility = 'hidden'を入れているのでhogehogeは表示されない
    
    file = OPERATION_MANUALS_PATH / file # ファイルパスを取得
    df = pd.read_excel(file)
    cols = df.columns

    # データフレームの表示
    st.markdown("<h2>2. 現在のマニュアルはこちらです。</h2>", unsafe_allow_html=True)
    st.table(df)

    # マニュアル追加・削除のための入力フォーム
    st.markdown("<h2>3. 新しいマニュアルを入力してください。</h2>", unsafe_allow_html=True)
    st.markdown("<p>※カテゴリはリストから選択するか、'その他'を選んで自由入力してください。</p>", unsafe_allow_html=True)
    st.markdown("<p>※1つの箱にルールは１つだけ書くこと。</p>", unsafe_allow_html=True)

    # No、カテゴリ、それぞれのリストを取得
    cols = df.columns
    numbers = df[cols[0]].tolist()
    categories = df[cols[1]].unique().tolist()
    categories.append('その他(新規作成)')

    # マニュアル追加のためのコンポーネントを表示
    col1_1, col2_1 = st.columns([1,2])
    new_category1, new_rule1 = manual_process.input_data(cols, categories, col1_1, col2_1, key='1')
    col1_2, col2_2 = st.columns([1,2])
    new_category2, new_rule2 = manual_process.input_data(cols, categories, col1_2, col2_2, key='2')
    col1_3, col2_3 = st.columns([1,2])
    new_category3, new_rule3 = manual_process.input_data(cols, categories, col1_3, col2_3, key='3')

    if st.button("マニュアルを追加して更新する"):
        df = manual_process.add_new_row(df, cols, new_category1, new_rule1)
        df = manual_process.add_new_row(df, cols, new_category2, new_rule2)
        df = manual_process.add_new_row(df, cols, new_category3, new_rule3)
        # カテゴリでソート
        df = df.sort_values(by=cols[1], ascending=True).reset_index(drop=True)

        # データを保存
        manual_process.save_data(df, OPERATION_MANUALS_PATH, file)
        st.success("マニュアルが追加されて更新されました！")

    # マニュアル削除のためのコンポーネントを表示
    st.markdown("<p>削除したいマニュアルのNo.を選択してください(複数選択可)。</p>", unsafe_allow_html=True)
    selected_number = st.multiselect('hogehoge', numbers, label_visibility = 'hidden') # label_visibility = 'hidden'を入れているのでhogehogeは表示されない

    if st.button("マニュアルを削除して更新する"):
        # テーブルからNo.に一致する行を削除
        for number in selected_number:
            df = df[df[cols[0]] != number]

        # データを保存
        manual_process.save_data(df, OPERATION_MANUALS_PATH, file)
        st.success("マニュアルが削除されて更新されました！")

    # データフレームの表示
    st.markdown("<h2>4. 更新後のマニュアルはこちらです。</h2>", unsafe_allow_html=True)
    st.table(df)

    st.markdown("<h2>5. ベクトルデータベースの更新を行います。</h2>", unsafe_allow_html=True)
    st.markdown("<p>ベクトルデータベースの更新をしたいマニュアルファイルを選択してください(複数選択可)。</p>", unsafe_allow_html=True)
    selected_files = st.multiselect('hogehoge', files, label_visibility = 'hidden') # label_visibility = 'hidden'を入れているのでhogehogeは表示されない
    selected_files = [OPERATION_MANUALS_PATH / file for file in selected_files]
    if st.button("マニュアルのベクトルデータベースを更新する"):
        data_process_operation_manuals.build_vector_database(selected_files)
        st.success("ベクトルデータベースが更新されました！")

# 2 マニュアル管理(フリーフォーマット)ページ
elif selected_page == pages[1]:
    st.title(pages[1])
    st.markdown("<p>こちらは、マニュアル管理(フリーフォーマット)ページです。フリーフォーマット(docx、PDFのみ対応)で書かれたマニュアルの追加・削除ができます。</p>", unsafe_allow_html=True)

    
# 3 ToDo抽出ページ
elif selected_page == pages[2]:
    st.title(pages[2])

    # テキストの入力の仕方を設定
    option = st.radio('1. テキストをどう入力しますか？', ('ベタ打ち', 'ファイルアップロード'))

    # テキストエリアを表示
    if option == 'ベタ打ち':
        # ユーザーが直接テキストを入力
        user_input = st.text_area("メールや議事録のテキストを入力してください。:", height=300)
    elif option == 'ファイルアップロード':
        # ファイルアップロード
        uploaded_file = st.file_uploader("タスクを抽出したいファイル(.docx / .txt)を選択してください。", type=["txt", "docx"])
        if uploaded_file is not None:
            # txt ファイルの内容を読み取る
            if uploaded_file.name.endswith('.txt'):
                user_input = project_log_process.read_txt_data(uploaded_file)
            # docx ファイルの内容を読み取る
            elif uploaded_file.name.endswith('.docx'):
                user_input = project_log_process.read_docx_data(uploaded_file)

            # ファイルの内容を表示
            st.markdown("<p>ファイルの中身はこちらです。</p>", unsafe_allow_html=True)
            st.text_area("", user_input, height=300)
    st.session_state.user_input = user_input

    # ToDoリストを作成するボタンが押されたときの処理
    if st.button('ToDoリストを作成する'):
        response1 = api_functions.generate_todo_list(input_text=user_input, model_name='gpt-4o-mini')
        st.session_state.result1 = response1
        # ユーザーが入力したテキストは、「ToDoリストを作成する」ボタンを押した後にProject logsフォルダに保存する
        save_path = project_log_process.save_data(user_input)
    # 保存された結果を表示
    if 'result1' in st.session_state:
        st.text_area('2. ToDoリスト:', str(st.session_state.result1), height=300)

    # ToDoリストを補完するボタンが押されたときの処理
    if st.button('ToDoリストに関連する業務マニュアルを補完する'):
        response2 = api_functions.complete_todo_list(input_text=str(st.session_state.result1))
        st.session_state.result2 = response2
    # 保存された結果を表示
    if 'result2' in st.session_state:
        st.text_area('3. ToDoリスト(補完後):', str(st.session_state.result2), height=400)

    # ToDoリストを系統化するボタンが押されたときの処理
    if st.button('ToDoリストを系統化する'):
        response3 = api_functions.group_todo_list(input_text=str(st.session_state.result2), model_name='gpt-4o-mini')
        st.session_state.result3 = response3
    # 保存された結果を表示
    if 'result3' in st.session_state:
        st.text_area('4. ToDoリスト(系統化後):', str(st.session_state.result3), height=400)


# 4 関連マニュアル検索ページ
elif selected_page == pages[3]:
    st.title(pages[3])
    query = st.text_input('ToDoを入力してください:', '')
    if st.button('関連マニュアルを検索'):
        results = api_functions.search_relevant_manual(query)
        st.session_state.results = results

        # 結果の表示
        if results:
            st.write(f'検索結果 ({len(results)}件):')
            for i, (result,score) in enumerate(results):
                st.write(f'### 結果 {i+1}')
                st.write(f"**ページ内容**: {result.page_content}")
                st.write(f"**コンテキスト**: {result.metadata['context']}")
                st.write(f"**ファイルパス**: {result.metadata['file_path']}")
                # st.write(f"**ファイルインデックス**: {result.metadata['file_index']}")
                st.write(f"**類似度スコア**: {score:.4f}")
        else:
            st.write('結果が見つかりませんでした。')


# 5 PJチャットボットページ
elif selected_page == pages[4]:
    st.title(pages[4])
    st.write("PJチャットボットページです。")

    st.markdown("<h2>1. Project logのベクトルデータベースを更新してください。</h2>", unsafe_allow_html=True)

    if PROJECT_LOGS_PATH.exists() and PROJECT_LOGS_PATH.is_dir():
        # txtファイルの一覧を取得
        txt_files = [f.name for f in PROJECT_LOGS_PATH.glob("*.txt")]
        
        if txt_files:
            # ファイル名を選択するセレクトボックス
            st.markdown("<p>中身を見たいファイルを選んでください。</p>", unsafe_allow_html=True)
            selected_file = st.selectbox("hogehoge", txt_files, label_visibility = 'hidden') # label_visibility = 'hidden'を入れているのでhogehogeは表示されない
            
            if selected_file:
                # ファイルの内容を表示
                file_path = PROJECT_LOGS_PATH / selected_file
                with file_path.open("r", encoding="utf-8") as file:
                    content = file.read()
                    st.text_area(f"「{selected_file}」はこちらです。", content, height=200)
        else:
            st.warning(f"「{PROJECT_LOGS_PATH}」フォルダにtxtファイルがありません。")
    else:
        st.error(f"「{PROJECT_LOGS_PATH}」フォルダが存在しません。")

    st.markdown("<p>削除したいテキストファイルがあれば選択してください(複数選択可)。</p>", unsafe_allow_html=True)
    selected_txt_files = st.multiselect('hogehoge', txt_files, label_visibility = 'hidden') # label_visibility = 'hidden'を入れているのでhogehogeは表示されない
    if st.button("削除"):
        for txt_file in selected_txt_files:
            file_path = PROJECT_LOGS_PATH / txt_file
            file_path.unlink()
        st.success("選択したテキストファイルが削除されました！")

    if st.button("Project logのベクトルデータベースを更新する"):
        data_process_project_logs.build_vector_database()
        st.success("ベクトルデータベースが更新されました！")

    st.markdown("<h2>2. こちらでProject logのベクトルデータベースに基づいた回答が得られます。</h2>", unsafe_allow_html=True)
    # (LLM)チャットメモリの初期化 ←if文に入れておくことでセッション間は1度しか実行されない
    if "memory" not in st.session_state:
        memory = api_functions.init_memory()
        st.session_state.memory = memory

    # (UI)会話履歴を初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # (UI)チャット入力ボックスを表示
    user_input = st.chat_input("メッセージを入力してください。例)○○の資料作成について、背景情報を教えてください。")
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
