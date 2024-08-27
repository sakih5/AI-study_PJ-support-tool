from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

import pandas as pd
from pathlib import Path
import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'


def _data_process(file):
    df = pd.read_excel(file)
    contexts = [f'{item["カテゴリ"]}:{item["ルール"]}' for item in df.to_dict('records')]
    df['コンテキスト'] = contexts
    return df


def _build_vector_database(df, file):
    # ChromaDBにベクトルデータベースを構築
    chroma_db = Chroma(
        collection_name='text_collection',
        embedding_function=OpenAIEmbeddings(model='text-embedding-ada-002'),
        persist_directory='./.data',
        )
    
    # ベクトルデータベースにドキュメントを追加)
    for index, row in df.iterrows():
        print(row['コンテキスト']) # どのチャンクをベクトル化したか確認する用
        text = row['カテゴリ']
        document = Document(
            page_content=text, # カテゴリ名をベクトル化する
            metadata={'context': row['コンテキスト'], # LLMに伝えるコンテキストをメタデータとして追加
                      'file_path': str(file),
                      'file_index': index}
            )
        chroma_db.add_documents(documents=[document])
    print("ベクトルデータベースの更新が完了しました。")


def main(input_folder=Path('Input')):
    # ベクトル化したいファイルを読み込む
    files = list(input_folder.glob('*.xlsx'))
    files = [file for file in files if not str(file).startswith("~$")]
    print(files)

    # 1ファイルずつベクトルデータベースを構築
    for file in files:
        df = _data_process(file)
        _build_vector_database(df, file)
        print(f"{file}の処理が完了しました。")


if __name__ == "__main__":
    input_folder=Path('Input')
    main(input_folder)
