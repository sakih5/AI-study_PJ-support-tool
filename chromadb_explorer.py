import streamlit as st
import chromadb
from chromadb.config import Settings

# client = chromadb.Client(
#     Settings(
#     chroma_db_impl="duckdb+parquet",
#     persist_directory="./chroma_db"
#     )
# )
client = chromadb.HttpClient(host='localhost', port=8000)

# ChromaDBクライアントの初期化
# client = chromadb.Client()
collection = client.get_collection(name="text_collection")

# Streamlitのタイトル
st.title("ChromaDB Explorer")

# サイドバーに検索ボックスを追加
search_query = st.sidebar.text_input("検索クエリを入力")

# 検索ボタンを押下時
if st.sidebar.button("検索"):
    # ChromaDBで検索
    results = collection.query(
        query_texts=[search_query],
        n_results=10
    )

    # 検索結果を表示
    for result in results['matches']:
        st.write(f"ID: {result['id']}")
        st.write(f"スコア: {result['score']}")