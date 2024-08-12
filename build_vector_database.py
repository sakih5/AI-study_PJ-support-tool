from langchain.text_splitter import SpacyTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import spacy
import openai
import pandas as pd
from pathlib import Path
import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'

def chank_texts(input_folder='input'):
    chanked_texts = []
    files = list(Path(input_folder).glob('*.xlsx'))
    for file in files:
        df = pd.read_excel(file)
        df = df.drop(0)
        df = df[['Unnamed: 2', 'Unnamed: 3']].dropna()
        df.columns = ['項目', '概要']
        chanked_texts.extend([f"{item['項目']}: {item['概要']}" for item in df.to_dict('records')])
    return chanked_texts

def main(input_folder='input'):
    # ベクトル化させたいデータを作成
    chanked_texts = chank_texts(input_folder='input')

    # OpenAI Embeddingsを使用してテキストをベクトル化
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
    vectors = [embeddings.embed_query(text) for text in chanked_texts]

    # ChromaDBにベクトルデータベースを構築
    chroma_db = Chroma(persist_directory='./.data',
                       embedding_function=embeddings,
                       # collection_name='text_collection'
                       )
    # chroma_db.add_documents(chanked_texts)
    # コレクションを追加するための修正
    for text, vector in zip(chanked_texts, vectors):
        chroma_db.add_document({"content": text, "embedding": vector})

    print("ベクトルデータベースがChromaDBに構築されました。")

if __name__ == "__main__":
    input_folder='input'
    main(input_folder)
