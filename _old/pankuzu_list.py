import streamlit as st

# パンくずリストの作成
def breadcrumbs(breadcrumbs_list):
    st.markdown(" > ".join([f"[{item}](#{item.replace(' ', '-').lower()})" for item in breadcrumbs_list]), unsafe_allow_html=True)

# パンくずリストの表示例
st.title("My Application")

# 現在のページのパンくずリスト
breadcrumbs(["Home", "Section", "Subsection", "Current Page"])

st.header("Current Page Content")
st.write("This is the content of the current page.")
