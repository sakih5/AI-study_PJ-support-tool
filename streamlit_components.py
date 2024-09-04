import shutil
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import docx

import data_process_operation_manuals
import data_process_project_logs
import api_functions


TODAY = datetime.now().strftime("%y%m%d")


class ManualProcess:
    # データ入力コンポーネント
    # 同じkeyのコンポーネントを複数回表示すると、エラーが発生するため、+0.1、+0.2などしてkeyを設定
    def input_data(self, cols, options, col1, col2, key):
        with col1: # カテゴリの選択
            user_input_category = st.selectbox(cols[1], options, key=key)
            # 「その他」が選択された場合、自由入力用のテキストボックスを表示
            if user_input_category == 'その他(新規作成)':
                custom_input = st.text_input('カテゴリ(自由記述):', key=str(float(key)+0.1))
                user_input_category = custom_input  # 入力された内容を選択されたオプションとして設定
        with col2: # ルールの入力
            rule_input = st.text_input(f'{cols[2]}(自由記述)', key=str(float(key)+0.2))
        return user_input_category, rule_input


    # 行追加コンポーネント
    def add_new_row(self, df, cols, category, rule):
        if category and rule:
            new_row = {
                cols[0]: int(df[cols[0]].max() + 1),  # No.は自動採番
                cols[1]: category,
                cols[2]: rule
            }
            new_row_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_row_df], ignore_index=True)
            return df
        return df # カテゴリとルールが入力されていない場合はそのまま返す


    # データ保存コンポーネント
    def save_data(self, df, OPERATION_MANUALS_PATH, file):
        # 1. OPERATION_MANUALSフォルダ配下にoldフォルダを作成、すでにあれば無視
        backup_dir = OPERATION_MANUALS_PATH / "_old"
        backup_dir.mkdir(exist_ok=True)
        # 2. OPERATION_MANUALSフォルダにある同名のファイルをoldフォルダに移動
        shutil.move(str(file), str(backup_dir / file.name))
        # 3. 新しいデータをOPERATION_MANUALSフォルダに保存
        df.to_excel(file, index=False)


class ProjectLogProcess:
    # ベタ打ちされたテキストデータのログフォルダへの保存
    def save_data(self, user_input, mode = "raw_txt", uploaded_file = None):
        save_dir = data_process_project_logs.TXT_DIR
        save_dir.mkdir(exist_ok=True)
        file_name = api_functions.generate_filename(user_input)
        if mode == "raw_txt":
            save_path = save_dir / f"{TODAY}_txt_{file_name}.txt" # TODO:user_inputをサマライズしてファイル名にする
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(user_input)
        elif mode == "uploaded_txt":
            save_path = save_dir / f"{TODAY}_txt_{uploaded_file.stem}.txt"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(user_input)
        elif mode == "docx":
            print(type(uploaded_file))
            print(uploaded_file.name)
            save_path = save_dir / f"{TODAY}_docx_{uploaded_file.stem}.txt"
            with open(save_path, "wb") as f:
                f.write(user_input)
        return save_path


    # アップロードされたWordファイルのログフォルダへの保存
    def read_docx_data(self, uploaded_file):
        doc = docx.Document(uploaded_file)
        user_input = "\n".join([para.text for para in doc.paragraphs])
        return user_input


    # アップロードされたtxtファイルのログフォルダへの保存
    def read_txt_data(self, uploaded_file):
        user_input = uploaded_file.getvalue().decode("utf-8")
        return user_input


# class CSSStyle:
#     def __init__(self):
# クラスにするとエラーが出るので、保留

# ボタンのCSSコンポーネント
button_css = f"""
<style>
  div.stButton > button:first-child {{
    font-weight  : 600                 ;/* 文字：セミボールド             */
    border       : 1px solid #cccccc   ;/* 枠線：薄いグレーで1ピクセルの実線 */
    border-radius: 5px                 ;/* 枠線：半径5ピクセルの角丸       */
    background   : #f7f7f7             ;/* 背景色：非常に薄いグレー       */
    padding      : 8px 16px            ;/* 内側の余白：上下8px、左右16px  */
    color        : #333333             ;/* 文字色：濃いグレー              */
    cursor       : pointer             ;/* カーソル：ポインター           */
  }}

  div.stButton > button:first-child:hover {{
    background   : #e6e6e6             ;/* ホバー時の背景色：薄いグレー  */
  }}

  div.stButton > button:first-child:active {{
    background   : #cccccc             ;/* アクティブ時の背景色：グレー  */
  }}
</style>
"""

# 見出しのCSSコンポーネント
heading_css = f"""
<style>
  h1 {{
    font-weight  : bold               ;/* 文字：太字                       */
    font-size    : 24px               ;/* フォントサイズ：24ピクセル       */
    color        : #333333            ;/* 文字色：濃いグレー                */
    margin-bottom: 16px               ;/* 下余白：16ピクセル                */
    border-bottom: 2px solid #dddddd  ;/* 下線：薄いグレーで2ピクセルの実線 */
    padding-bottom: 8px               ;/* 下の内側余白：8ピクセル           */
    # position      : fixed              ;/* 固定位置に設定                    */
    # top           : 0                  ;/* 上端からの距離                    */
    # left          : 0                  ;/* 左端からの距離                    */
    # width         : 100%               ;/* 幅を全幅に設定                    */
    # background-color: white            ;/* 背景色：白                       */
    # z-index       : 1000               ;/* 他の要素よりも前面に表示          */
  }}

  h2 {{
    font-weight  : 600                ;/* 文字：セミボールド                */
    font-size    : 20px               ;/* フォントサイズ：20ピクセル        */
    color        : #555555            ;/* 文字色：やや濃いグレー            */
    margin-bottom: 12px               ;/* 下余白：12ピクセル                */
  }}
</style>
"""

# 本文のCSSコンポーネント
paragraph_css = f"""
<style>
  p {{
    font-size    : 16px               ;/* フォントサイズ：16ピクセル        */
    line-height  : 1.6                ;/* 行間：1.6                         */
    color        : #666666            ;/* 文字色：中間のグレー              */
    margin-bottom: 16px               ;/* 下余白：16ピクセル                */
  }}

  p.lead {{
    font-size    : 18px               ;/* フォントサイズ：18ピクセル        */
    font-weight  : 500                ;/* 文字：セミボールド                */
    color        : #333333            ;/* 文字色：濃いグレー                */
    margin-bottom: 20px               ;/* 下余白：20ピクセル                */
  }}
</style>
"""

# 以下、CSSコンポーネントをStreamlitに反映するためのサンプルコード
# # CSSをStreamlitに反映
# st.markdown(button_css, unsafe_allow_html=True)
# st.markdown(heading_css, unsafe_allow_html=True)
# st.markdown(paragraph_css, unsafe_allow_html=True)

# # 見出しを表示
# st.markdown("<h1>ビジネス向け見出し</h1>", unsafe_allow_html=True)
# st.markdown("<h2>サブタイトル</h2>", unsafe_allow_html=True)

# # 本文を表示
# st.markdown("<p>これは通常の本文です。ビジネス文書に適したデザインになっています。</p>", unsafe_allow_html=True)
# st.markdown("<p class='lead'>これはリード文です。強調されたスタイルで表示されます。</p>", unsafe_allow_html=True)

# # ボタンを表示
# if st.button("クリック"):
#     st.write("ボタンがクリックされました！")

# st.markdown(button_css, unsafe_allow_html=True)
# action = st.button('このボタンを押してください')
