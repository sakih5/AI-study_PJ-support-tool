import streamlit as st
import docx

from pathlib import Path
import shutil
import pandas as pd

import api_functions
import data_process

st.set_page_config(
    page_title="PJサポートツール",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
# 1 マニュアル管理ページ
if selected_page == pages[0]:
    st.title(pages[0])
    st.markdown(f'<p style="font-size:18px;">こちらは、マニュアル管理ページです。', unsafe_allow_html=True)

    # データの読み込み
    input_dir = Path("Input")
    st.markdown(f'<p style="font-size:18px;">1．確認 or 編集したいマニュアルファイルを選択してください', unsafe_allow_html=True)
    file = st.selectbox('',list(input_dir.glob("*.xlsx")))
    df = pd.read_excel(file)
    cols = df.columns

    st.markdown(f'<p style="font-size:18px;">2．現在のマニュアル:', unsafe_allow_html=True)
    st.table(df)

    # 入力フォーム
    st.markdown(f"<p style='font-size:18px;'>3．新しいマニュアルを入力してください。\
                \n\n<p style='font-size:18px;'>※カテゴリはリストから選択するか、'その他'を選んで自由入力してください。",
                unsafe_allow_html=True)
    # テキストボックスを横に並べる
    col1, col2 = st.columns(2)
    with col1:
        options = df[cols[1]].unique().tolist()
        options.append('その他(新規作成)')
        new_value1 = st.selectbox(cols[1], options)
        # 「その他」が選択された場合、自由入力用のテキストボックスを表示
        if new_value1 == 'その他(新規作成)':
            custom_input = st.text_input('カテゴリ(自由記述):')
            new_value1 = custom_input  # 入力された内容を選択されたオプションとして設定
    with col2:
        new_value2 = st.text_input(f'{cols[2]}(自由記述)')
    
    # 更新ボタンを表示
    if st.button("マニュアルを追加・更新する"):
        if new_value1 and new_value2:
            # 新しい行を作成
            new_row = {cols[0]: int(df[cols[0]].max() + 1), # No.は自動採番
                       cols[1]: new_value1,
                       cols[2]: new_value2
                       }
            # テーブルに新しい行を追加
            df = df.append(new_row, ignore_index=True)
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
    st.markdown(f'<p style="font-size:18px;">4．更新後のマニュアル:', unsafe_allow_html=True)
    st.table(df)

# 2 ToDo抽出ページ
elif selected_page == pages[1]:
    st.title(pages[1])

    # テキストの入力の仕方を設定
    st.markdown(f'<p style="font-size:18px;">1．テキストをどう入力しますか？', unsafe_allow_html=True)
    option = st.radio('', ('ベタ打ち', 'ファイルアップロード'))

    # テキストエリアを表示
    if option == 'ベタ打ち':
        # ユーザーが直接テキストを入力
        user_input = st.text_area("メールや議事録のテキストを入力して:", height=300)
    elif option == 'ファイルアップロード':
        # ファイルアップロード
        uploaded_file = st.file_uploader("タスクを抽出したいファイル(.docx / .txt)を選択してください", type=["txt", "docx"])
        if uploaded_file is not None:
            # txt ファイルの内容を読み取る
            if uploaded_file.name.endswith('.txt'):
                user_input = uploaded_file.getvalue().decode("utf-8")
                st.write("ファイルの内容:")
                st.text_area("", user_input, height=300)
            # docx ファイルの内容を読み取る
            elif uploaded_file.name.endswith('.docx'):
                doc = docx.Document(uploaded_file)
                user_input = "\n".join([para.text for para in doc.paragraphs])
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
        st.text_area('ToDoリスト:', str(st.session_state.result1), height=300)

    if 'result2' in st.session_state:
        st.text_area('ToDoリスト(補完後):', str(st.session_state.result2), height=400)

    if 'result3' in st.session_state:
        st.text_area('ToDoリスト(系統化後):', str(st.session_state.result3), height=400)

# PJチャットボットページ
elif selected_page == pages[2]:
    st.title(pages[2])
    st.write("PJチャットボットページです。")