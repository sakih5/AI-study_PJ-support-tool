from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.callbacks.base import BaseCallbackHandler
from langchain_chroma import Chroma

from langchain_openai import ChatOpenAI

import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-3pSCJqVVn8lRccIMTfXFT3BlbkFJvB0pdZtI3qOHc4EmWKKV'

# ストリーミング表示
# class SimpleStreamlitCallbackHandler(BaseCallbackHandler):
#     """ Copied only streaming part from StreamlitCallbackHandler """
    
#     def __init__(self):
#         self.tokens_area = st.empty()
#         self.tokens_stream = ""
        
#     def on_llm_new_token(self, token: str, **kwargs: any):
#         """Run on new LLM token. Only available when streaming is enabled."""
#         self.tokens_stream += token
#         self.tokens_area.markdown(self.tokens_stream)
# handler = SimpleStreamlitCallbackHandler()

def initialize_model(model_name):
    if model_name == 'gpt-4o-mini':
        return ChatOpenAI(model=model_name)
    elif model_name == 'text-embedding-ada-002':
        return OpenAIEmbeddings(model='text-embedding-ada-002')
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
            collection_name='manual_collection', 
            embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
            persist_directory="./.data",
        )

    # 文字列を1行ずつ分割
    lines = input_text.split('\n')

    # 結果を格納する変数
    concatenated_text = ""

    for line in lines:
        # 類似チャンクを検索。結果はリスト型(リストの中は(result,score)のタプル)
        docs = database.similarity_search_with_relevance_scores(line, k=10)

        # スコアがMaxのコンテキストをまとめる
        contexts = ""
        init_score = 0
        for (result, score) in docs:
            if score >= init_score:
                contexts = f"{contexts}\n\n・{result.metadata['context']}"
                init_score = score

        # プロンプトテンプレートの定義
        prompt_template = "タスクに業務マニュアルに沿った情報を補完せよ。\
                        補完時の注意事項 \
                        1. 「タスク名(氏名)」の下の行に、「※補足：」から始まる形で業務マニュアルに沿った補足を追記すること。\
                        :\n\n{line} \
                        \n\n関連業務マニュアル:{context}"
        # メッセージの作成
        messages = [
            SystemMessage(content="あなたはプロジェクトリーダーです。業務マニュアルに沿った補足情報を追加して、部下にわかりやすくタスクを振ることができます。"),
            HumanMessage(content=prompt_template.format(line=line, context=contexts))
        ]

        # 生成AIモデルから返事を取得
        completed_todo = model.invoke(messages)
        concatenated_text += completed_todo.content + "\n\n"

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
                    6. タスクのリストは、箇条書きで出力すること。\
                    7. グループのタイトルとタスク以外には何も書かないこと。\
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

def search_relevant_manual(query, model_name='text-embedding-ada-002'):
    # モデルの初期化
    model = initialize_model(model_name)

    # ChromaDBへの接続
    chroma_db = Chroma(
        collection_name='text_collection',
        embedding_function=model,
        persist_directory='./.data_manual'
    )

    # クエリをベクトル化して検索
    results = chroma_db.similarity_search_with_relevance_scores(query, k=10)
    return results


def init_memory():
    # 会話履歴を初期化
    memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
            )
    return memory


def chat_with_memory_and_rag(user_input, memory, model_name='gpt-4o-mini'):
    # モデルの初期化
    model = initialize_model(model_name)

    # ChromaDBへの接続
    chroma_db = Chroma(
        collection_name='projectlog_collection',
        embedding_function=OpenAIEmbeddings(model='text-embedding-ada-002'),
        persist_directory='./.data_projectlog',
    )

    # ChromaDBをretrieverに変換
    retriever = chroma_db.as_retriever()

    # 質問の文脈化
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question which might reference context in the chat history,\
        formulate a standalone question which can be understood without the chat history.\
        Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        model, retriever, contextualize_q_prompt
    )

    # RAGを使って質問に回答するよう指示
    qa_system_prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.\
        If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\
        \n\n{context}"
    ) 

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(
        model, qa_prompt
    )

    rag_chain = create_retrieval_chain(
        history_aware_retriever, 
        question_answer_chain
    )

    # 生成AIモデルから返事を取得
    print(memory.load_memory_variables({}))
    chat_history = memory.load_memory_variables({})['chat_history'] # Collect chat history here
    
    response = rag_chain.invoke(
        {
        'input': user_input,
        'chat_history': chat_history
        }
    )

    memory.save_context(
        {"inputs":user_input},
        {"outputs":response['answer']}
    )
    return response['answer'], memory


