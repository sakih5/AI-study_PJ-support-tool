import streamlit as st

# ボタンのCSS
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

# 見出しのCSS
heading_css = f"""
<style>
  h1 {{
    font-weight  : bold               ;/* 文字：太字                       */
    font-size    : 24px               ;/* フォントサイズ：24ピクセル       */
    color        : #333333            ;/* 文字色：濃いグレー                */
    margin-bottom: 16px               ;/* 下余白：16ピクセル                */
    border-bottom: 2px solid #dddddd  ;/* 下線：薄いグレーで2ピクセルの実線 */
    padding-bottom: 8px               ;/* 下の内側余白：8ピクセル           */
  }}

  h2 {{
    font-weight  : 600                ;/* 文字：セミボールド                */
    font-size    : 20px               ;/* フォントサイズ：20ピクセル        */
    color        : #555555            ;/* 文字色：やや濃いグレー            */
    margin-bottom: 12px               ;/* 下余白：12ピクセル                */
  }}
</style>
"""

# 本文のCSS
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
