import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Cloud SQL接続情報
user = 'your_user'
password = 'your_password'
host = 'your_host'
database = 'your_database'

# データベースへの接続
engine = create_engine(
    f'mysql+pymysql://{user}:{password}@{host}/{database}'
)

# テーブル名
table_name = 'your_table_name'

# データの取得
df = pd.read_sql_query(f'SELECT * FROM {table_name}', engine)

# Streamlit UI
st.title('Cloud SQL データ操作')

# データの表示
st.dataframe(df)

# 新しいデータの追加
with st.form('add_data'):
    new_data = {}
    for col in df.columns:
        new_data[col] = st.text_input(col)
    submitted = st.form_submit_button('追加')
    if submitted:
        # SQL文を組み立てて実行
        sql = f"INSERT INTO {table_name} ({', '.join(new_data.keys())}) VALUES ({', '.join(['%s'] * len(new_data))})"
        engine.execute(sql, list(new_data.values()))
        st.success('データを追加しました。')

# データの削除
with st.form('delete_data'):
    index = st.number_input('削除する行のインデックス', min_value=0, max_value=len(df)-1)
    submitted = st.form_submit_button('削除')
    if submitted:
        # 削除対象のデータを取得
        data_to_delete = df.iloc[index]
        # SQL文を組み立てて実行
        sql = f"DELETE FROM {table_name} WHERE {list(data_to_delete.index)[0]} = %s"
        engine.execute(sql, data_to_delete[list(data_to_delete.index)[0]])
        st.success('データを削除しました。')