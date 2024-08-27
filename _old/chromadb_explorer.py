import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'

# ChromaDBへの接続
chroma_db = Chroma(
    collection_name='text_collection',
    embedding_function=OpenAIEmbeddings(model='text-embedding-ada-002'),
    persist_directory='./.data'
)

# Streamlitアプリケーション
st.title('ベクトルデータベース検索ツール')

# ユーザーのクエリ入力
query = st.text_input('検索クエリを入力してください:', '')

if query:
    # クエリをベクトル化して検索
    results = chroma_db.similarity_search_with_relevance_scores(query, k=10)
    
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