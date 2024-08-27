from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.vectorstores import Chroma

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

import os

os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'


def initialize_model(model_name):
    if model_name == 'gpt-4o-mini':
        return ChatOpenAI(model=model_name)
    elif model_name == 'claude':
        return ChatAnthropic(model=model_name)
    else:
        raise ValueError("Unsupported model name. Choose either 'gpt-4o-mini' or 'claude'.")


def generate_todo_list(input_text, model_name='gpt-4o-mini'):
    # モデルの初期化
    model = initialize_model(model_name)

    # プロンプトテンプレートの定義
    prompt_template = "以下の文からメンバーやるべきタスクを箇条書きで出力せよ。\
                    箇条書き生成時の注意事項 \
                    1. タスクだけを箇条書きにすること。他の要素は箇条書きに加えないこと。\
                    2. 各タスクの末尾に、そのタスクを誰がやるのか分かれば()書きで記載すること\
                    :\n\n{input_text}"
    # メッセージの作成
    messages = [
        SystemMessage(content="あなたは優秀なプロジェクト管理者です。メンバーがクライアントから受け取ったメールや会議の議事録などからタスクを抽出できます。"),
        HumanMessage(content=prompt_template.format(input_text=input_text))
    ]

    # 生成AIモデルから返事を取得
    todo_list = model.invoke(messages)

    # AIMessageオブジェクトのcontentを抽出して出力
    return todo_list.content


def complete_todo_list(input_text, model_name='gpt-4o-mini'):
    # モデルの初期化
    model = initialize_model(model_name)

    # ベクトルデータベースの読み込み
    database = Chroma(
            persist_directory="./.data", 
            embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002")
        )
    
    # 文字列を1行ずつ分割
    lines = input_text.split('\n')

    # 結果を格納する変数
    concatenated_text = ""

    for line in lines:
        docs = database.similarity_search(line)
        print(docs)

        # プロンプトテンプレートの定義
        prompt_template = "タスクに業務マニュアルに沿った情報を補完せよ。\
                        補完時の注意事項 \
                        1. 「タスク名(氏名)」の下の行に、「※補足：」から始まる形で業務マニュアルに沿った補足を追記すること。\
                        :\n\n{line} \
                        \n\n関連業務マニュアル:{context}"
        # メッセージの作成
        messages = [
            SystemMessage(content="あなたはプロジェクトリーダーです。業務マニュアルに沿った補足情報を追加して、部下にわかりやすくタスクを振ることができます。"),
            HumanMessage(content=prompt_template.format(line=line, context=docs[0].content))
        ]

        # 生成AIモデルから返事を取得
        completed_todo = model.invoke(messages)
        concatenated_text += completed_todo.choices[0].text + "\n"

    return concatenated_text

def group_todo_list(input_text, model_name='gpt-4o-mini'):
    # モデルの初期化
    model = initialize_model(model_name)

    # プロンプトテンプレートの定義
    prompt_template = "以下のタスクのリストをグループ化して並び替えて出力せよ。\
                    グループ化時の注意事項 \
                    1. 類似するタスクを同じグループにまとめること。\
                    2. グループごとにタスクを整理し、系統立てて出力すること。\
                    3. グループのタイトルは、そのグループのタスクの内容を表すようにすること。\
                    4. タスクは抜け漏れなく分類すること。\
                    5. 各タスクの末尾に、そのタスクを誰がやるのか分かれば()書きで記載されているので、そのまま残しておくこと。\
                    6. グループのタイトルとタスクは、それぞれ改行で区切ること。\
                    7. グループのタイトルとタスクの間には、空行を入れること。\
                    8. タスクのリストは、箇条書きで出力すること。\
                    9. グループのタイトルとタスク以外には何も書かないこと。\
                    :\n\n{input_text}"
    # メッセージの作成
    messages = [
        SystemMessage(content="あなたは優秀なプロジェクト管理者です。タスクのリストをわかりやすく系統立てて整理することができます。"),
        HumanMessage(content=prompt_template.format(input_text=input_text))
    ]

    # 生成AIモデルから返事を取得
    todo_list = model.invoke(messages)

    # AIMessageオブジェクトのcontentを抽出して出力
    return todo_list.content