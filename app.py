__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st

from pathlib import Path
import shutil
import pandas as pd

import api_functions
import manual_data_process
import projectlog_data_process
import css_style as style

# Streamlitのページ設定
st.set_page_config(
    page_title="PJサポートツール",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSSをStreamlitに反映
st.markdown(style.button_css, unsafe_allow_html=True)
st.markdown(style.heading_css, unsafe_allow_html=True)
st.markdown(style.paragraph_css, unsafe_allow_html=True)

# サイドバーの一番上にタイトルを表示
st.sidebar.markdown("<h2>PJサポートツール</h2>", unsafe_allow_html=True)

# セレクトボックスのリストを作成
pages = ["1 マニュアル管理", "2 ToDo抽出", "3 関連マニュアル検索","4 PJチャットボット"]

# 空のページがないか確認し、空のページがあれば削除する
pages = [page for page in pages if page.strip()]

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
# 1 マニュアル管理ページ
if selected_page == pages[0]:
    st.title(pages[0])
    st.markdown("<p>こちらは、マニュアル管理ページです。\n\nマニュアルの追加・削除ができます。</p>", unsafe_allow_html=True)
    # データの読み込み
    input_dir = Path("Input")
    st.markdown("<h2>1. 確認 or 編集したいマニュアルファイルを選択してください。</h2>", unsafe_allow_html=True)
    
    file = st.selectbox('hogehoge',list(input_dir.glob("*.xlsx")),label_visibility = 'hidden')
    df = pd.read_excel(file)
    cols = df.columns

    st.markdown("<h2>2. 現在のマニュアルはこちらです。</h2>", unsafe_allow_html=True)
    st.table(df)

    # 入力フォーム
    st.markdown("<h2>3. 新しいマニュアルを入力してください。</h2>", unsafe_allow_html=True)
    st.markdown("<p>※カテゴリはリストから選択するか、'その他'を選んで自由入力してください。</p>", unsafe_allow_html=True)
    # テキストボックスを横に並べる
    col1, col2 = st.columns(2)
    with col1:
        options = df[cols[1]].unique().tolist()
        options.append('その他(新規作成)')
        new_value1 = st.selectbox(cols[1], options, label_visibility = 'hidden')
        # 「その他」が選択された場合、自由入力用のテキストボックスを表示
        if new_value1 == 'その他(新規作成)':
            custom_input = st.text_input('カテゴリ(自由記述):', label_visibility = 'hidden')
            new_value1 = custom_input  # 入力された内容を選択されたオプションとして設定
    with col2:
        new_value2 = st.text_input(f'{cols[2]}(自由記述)', label_visibility = 'hidden')
    
    # 更新ボタンを表示
    if st.button("マニュアルを追加・更新する"):
        if new_value1 and new_value2:
            # 新しい行を作成
            new_row = {cols[0]: int(df[cols[0]].max() + 1), # No.は自動採番
                       cols[1]: new_value1,
                       cols[2]: new_value2
                       }
            # 新しい行を追加するためにDataFrameを作成
            new_row_df = pd.DataFrame([new_row])
            # テーブルに新しい行を追加
            df = pd.concat([df, new_row_df], ignore_index=True)
            # カテゴリでソート
            df = df.sort_values(by=cols[1], ascending=True).reset_index(drop=True)

        # データを保存
        # 1. Inputフォルダ配下にoldフォルダを作成、すでにあれば無視
        backup_dir = input_dir / "_old"
        backup_dir.mkdir(exist_ok=True)
        # 2. Inputフォルダにある同名のファイルをoldフォルダに移動
        shutil.move(str(file), str(backup_dir / file.name))
        # 3. 新しいデータをInputフォルダに保存
        df.to_excel(file, index=False)
        st.success("マニュアルが更新されました！")

    # データフレームの表示
    st.markdown("<h2>4. 更新後のマニュアルはこちらです。</h2>", unsafe_allow_html=True)
    st.table(df)

    if st.button("マニュアルのベクトルデータベースを更新する"):
        manual_data_process.build_vector_database(input_dir)
        st.success("ベクトルデータベースが更新されました！")


# 2 ToDo抽出ページ
elif selected_page == pages[1]:
    st.title(pages[1])

    # テキストの入力の仕方を設定
    option = st.radio('1. テキストをどう入力しますか？', ('ベタ打ち', 'ファイルアップロード'), label_visibility = 'hidden')

    # テキストエリアを表示
    if option == 'ベタ打ち':
        # ユーザーが直接テキストを入力
        user_input = st.text_area("メールや議事録のテキストを入力してください。:", height=300)

        # user_inputをテキストファイルとして保存する
        save_path = projectlog_data_process.save_raw_data(user_input)

    elif option == 'ファイルアップロード':
        # ファイルアップロード
        uploaded_file = st.file_uploader("タスクを抽出したいファイル(.docx / .txt)を選択してください。", type=["txt", "docx"])
        if uploaded_file is not None:
            # txt ファイルの内容を読み取る
            if uploaded_file.name.endswith('.txt'):
                user_input, save_path = projectlog_data_process.save_uploaded_txt_data(uploaded_file)
            # docx ファイルの内容を読み取る
            elif uploaded_file.name.endswith('.docx'):
                user_input, save_path = projectlog_data_process.save_uploaded_docx_data(uploaded_file)

            # ファイルの内容を表示
            st.write("ファイルの内容:")
            st.text_area("", user_input, height=300)

    # ToDoリストを作成するボタンが押されたときの処理
    if st.button('ToDoリストを作成する'):
        response1 = api_functions.generate_todo_list(input_text=user_input, model_name='gpt-4o-mini')
        st.session_state.result1 = response1

    # ToDoリストを補完するボタンが押されたときの処理
    if st.button('ToDoリストに関連する業務マニュアルを補完する'):
        response2 = api_functions.complete_todo_list(input_text=str(st.session_state.result1), model_name='gpt-4o-mini')
        st.session_state.result2 = response2

    # ToDoリストを系統化するボタンが押されたときの処理
    if st.button('ToDoリストを系統化する'):
        response3 = api_functions.group_todo_list(input_text=str(st.session_state.result2), model_name='gpt-4o-mini')
        st.session_state.result3 = response3

    # 保存された結果を表示
    if 'result1' in st.session_state:
        st.text_area('2. ToDoリスト:', str(st.session_state.result1), height=300)

    if 'result2' in st.session_state:
        st.text_area('3. ToDoリスト(補完後):', str(st.session_state.result2), height=400)

    if 'result3' in st.session_state:
        st.text_area('4. ToDoリスト(系統化後):', str(st.session_state.result3), height=400)


# 関連マニュアル検索ページ
elif selected_page == pages[2]:
    st.title(pages[2])
    query = st.text_input('ToDoを入力してください:', '')
    if st.button('関連マニュアルを検索'):
        results = api_functions.search_relevant_manual(query)

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


# PJチャットボットページ
elif selected_page == pages[3]:
    st.title(pages[3])
    st.write("PJチャットボットページです。")

    st.markdown("<h2>Project logのベクトルデータベースを更新してください。</h2>", unsafe_allow_html=True)
    if st.button("Project logのベクトルデータベースを更新する"):
        projectlog_data_process.build_vector_database()

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
