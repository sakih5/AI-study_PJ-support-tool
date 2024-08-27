import streamlit as st
import pandas as pd
from pathlib import Path
import shutil

# Streamlitアプリケーションのタイトル
st.title("Excelファイルの編集と更新")

# データの読み込み
input_dir = Path("Input")
file = st.selectbox('選択してください', list(input_dir.glob("*.xlsx")))
df = pd.read_excel(file)
cols = df.columns

# データフレームを表示
st.write("編集前のデータ:")
st.table(df)

# テキストボックスを横に並べる
col1, col2, col3 = st.columns(3)

# 入力フォーム
with col1:
    new_value1 = st.text_input(cols[0])
with col2:
    new_value2 = st.text_input(cols[1])
with col3:
    new_value3 = st.text_input(cols[2])

# 更新ボタンを表示
if st.button("更新"):
    if new_value1 and new_value2 and new_value3:
        # 新しい行を作成
        new_row = {cols[0]: int(new_value1), 
                   cols[1]: new_value2, 
                   cols[2]: new_value3}
        # テーブルに新しい行を追加
        df = df.append(new_row, ignore_index=True)

    # データを保存
    # 1. Inputフォルダ配下にoldフォルダを作成、すでにあれば無視
    backup_dir = input_dir / "_old"
    backup_dir.mkdir(exist_ok=True)
    # 2. Inputフォルダにある同名のファイルをoldフォルダに移動
    shutil.move(str(file), str(backup_dir / file.name))
    # 3. 新しいデータをInputフォルダに保存
    df.to_excel(file, index=False)
    st.success("データが更新されました！")

# データフレームの表示
st.write("編集後のデータ:")
st.table(df)
