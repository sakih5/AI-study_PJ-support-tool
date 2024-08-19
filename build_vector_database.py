from langchain.text_splitter import SpacyTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

import pandas as pd
from pathlib import Path
import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'

def chank_texts(input_folder='Input/01_Common'):
    chanked_texts = []
    files = list(Path(input_folder).glob('*.xlsx'))
    files = [file for file in files if not str(file).startswith("~$")]
    print(files)
    for file in files:
        df = pd.read_excel(file)
        df = df.drop(0)
        df = df[['Unnamed: 2', 'Unnamed: 3']].dropna()
        df.columns = ['項目', '概要']
        chanked_texts = [f'{item["項目"]}:{item["概要"]}' for item in df.to_dict('records')]
    return chanked_texts

def main(input_folder):
    # ChromaDBにベクトルデータベースを構築
    chroma_db = Chroma(
        collection_name='text_collection',
        embedding_function=OpenAIEmbeddings(model='text-embedding-ada-002'),
        persist_directory='./.data',
                       )
    
    # ベクトル化させたいデータを作成
    chanked_texts = chank_texts(input_folder)

    # Document インスタンスのリストを作成
    documents = [Document(page_content=text) for text in chanked_texts]

    # ドキュメントを追加
    chroma_db.add_documents(documents=documents)

    print("ベクトルデータベースがChromaDBに構築されました。")

if __name__ == "__main__":
    input_folder='Input/01_Common'
    main(input_folder)
