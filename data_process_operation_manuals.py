from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv


# .envファイルを読み込む
load_dotenv()


# 環境変数を取得
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = 'text-embedding-ada-002'
DB_NAME = 'collection_operation_manuals'
DB_DIR = './.data_operation_manuals'
XLSX_DIR = Path('Operation manuals')

CONTEXT_COL = 'コンテキスト' # ベクトルデータベースに追加する際のコンテキストのカラム名


def initialize_model(model_name):
    if model_name == 'text-embedding-ada-002':
        return OpenAIEmbeddings(model = 'text-embedding-ada-002')
    else:
        raise ValueError("Unsupported model name. Choose either 'text-embedding-ada-002' or '-'.")


def _data_process(file):
    df = pd.read_excel(file)
    cols = df.columns.tolist()
    contexts = [f'{item[cols[1]]}:{item[cols[2]]}' for item in df.to_dict('records')] # cols[1]がカテゴリ、cols[2]がルール
    df[CONTEXT_COL] = contexts
    return df


def _build_vector_database(df, file, model_name = MODEL_NAME):
    # モデルの初期化
    model = initialize_model(model_name)

    # ChromaDBにベクトルデータベースを構築
    chroma_db = Chroma(
        collection_name = DB_NAME,
        embedding_function = model,
        persist_directory = DB_DIR,
    )

    # ベクトルデータベースにドキュメントを追加
    cols = df.columns.tolist()
    for index, row in df.iterrows():
        print(row[CONTEXT_COL]) # どのチャンクをベクトル化したか確認する用
        text = row[cols[1]] # cols[1]がカテゴリ
        document = Document(
            page_content=text, # カテゴリ名をベクトル化する
            metadata={'context': row[CONTEXT_COL], # LLMに伝えるコンテキストをメタデータとして追加
                      'file_path': str(file),
                      'file_index': index}
            )
        chroma_db.add_documents(documents=[document])
    print("ベクトルデータベースの更新が完了しました。")


def build_vector_database(files):
    # キャッシュファイルを除外
    files = [file for file in files if not str(file).startswith("~$")]
    print(files)

    # 1ファイルずつベクトルデータベースを構築
    for file in files:
        df = _data_process(file)
        _build_vector_database(df, file)
        print(f"{file}の処理が完了しました。")