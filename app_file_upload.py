import streamlit as st
from docx import Document
from io import BytesIO

# Streamlitアプリケーションのタイトル
st.title("Wordファイルのテキスト表示アプリ")

# Wordファイルのアップロード
uploaded_file = st.file_uploader("Wordファイルをアップロードしてください", type=["docx"])

if uploaded_file is not None:
    # アップロードされたファイルをDocumentオブジェクトとして読み込む
    doc = Document(BytesIO(uploaded_file.read()))

    # ドキュメント内のすべてのテキストを結合して表示する
    text = "\n".join([para.text for para in doc.paragraphs])
    
    # テキストを表示
    st.text_area("ファイルの内容", text, height=400)
