import streamlit as st

# ドロップダウンリストのオプション
options = ['オプション1', 'オプション2', 'オプション3']

# ドロップダウンメニューに「その他」を追加
selected_option = st.selectbox('リストから選択するか、"その他"を選んで自由入力してください', options + ['その他'])

# 「その他」が選択された場合、自由入力用のテキストボックスを表示
if selected_option == 'その他':
    custom_input = st.text_input('自由入力:')
    selected_option = custom_input  # 入力された内容を選択されたオプションとして設定

# 選択されたオプションまたは自由入力された内容を表示
if selected_option:
    st.write(f'選択されたもの: {selected_option}')
