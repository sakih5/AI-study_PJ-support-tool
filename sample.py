import streamlit as st

# ページの設定
st.set_page_config(page_title="マニュアル検索ツール", layout="centered")

# タイトル
st.title("マニュアル検索ツール")

# 検索ボックスと検索ボタン
search_query = st.text_input("マニュアルを検索...", "")
search_button = st.button("検索")

# ダミーの検索結果データ
manuals = [
    {"title": "マニュアル1", "description": "このマニュアルは、関連するトピックについて説明しています。"},
    {"title": "マニュアル2", "description": "このマニュアルは、関連するトピックについて詳細に説明しています。"},
    # 必要に応じて、検索結果を追加
]

# 検索ボタンが押されたときに検索結果を表示
if search_button:
    if search_query:
        st.write(f"検索結果: {search_query}")
        for manual in manuals:
            st.markdown(f"### {manual['title']}")
            st.write(manual['description'])
            st.write("---")
    else:
        st.warning("検索クエリを入力してください。")

# スタイルの調整
st.markdown(
    """
    <style>
    .stTextInput, .stButton {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border-radius: 4px;
    }
    
    .stButton button {
        background-color: #007bff;
        color: white;
        border: none;
    }
    
    .stButton button:hover {
        background-color: #0056b3;
    }

    .stMarkdown h3 {
        color: #007bff;
        margin-bottom: 5px;
    }
    
    .stMarkdown p {
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)
