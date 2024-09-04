from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from pathlib import Path
import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'


MODEL_NAME = 'text-embedding-ada-002'
DB_NAME = 'collection_project_logs'
DB_DIR = './.data_project_logs'
TXT_DIR = Path('Project logs')

def initialize_model(model_name):
    if model_name == 'text-embedding-ada-002':
        return OpenAIEmbeddings(model='text-embedding-ada-002')
    else:
        raise ValueError("Unsupported model name. Choose either 'text-embedding-ada-002' or '-'.")


# いずれも1行空きのあるところでチャンク分け
def _data_process(user_input):
    chunks = user_input.split("\n\n")
    return chunks


def _build_vector_database(chunks, save_path, model_name = MODEL_NAME):
    # モデルの初期化
    model = initialize_model(model_name)

    # ChromaDBにベクトルデータベースを構築
    chroma_db = Chroma(
        collection_name = DB_NAME,
        embedding_function = model,
        persist_directory = DB_DIR,
    )

    # ベクトルデータベースにドキュメントを追加)
    for idx, chunk in enumerate(chunks):
        print(chunk) # どのチャンクをベクトル化したか確認する用
        document = Document(
            page_content = chunk, # チャンクをベクトル化する
            metadata={
                'file_path': str(save_path),
                'idx': idx}
            )
        chroma_db.add_documents(documents=[document])
    print("ベクトルデータベースの更新が完了しました。")


def build_vector_database(input_folder=TXT_DIR):
    # ベクトル化したいファイルを読み込む
    files = list(input_folder.glob('*.txt'))
    files = [file for file in files if not str(file).startswith("~$")]
    print(files)

    # 1ファイルずつベクトルデータベースを構築
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        user_input = _data_process(content)
        _build_vector_database(user_input, file)
        print(f"{file}の処理が完了しました。")