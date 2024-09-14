from pathlib import Path
import streamlit as st

# フォルダのパスを指定（Pythonファイルと同じ階層にある"Project logs"フォルダ）
folder_path = Path("Project logs")

# フォルダが存在するか確認
if folder_path.exists() and folder_path.is_dir():
    # txtファイルの一覧を取得
    txt_files = [f.name for f in folder_path.glob("*.txt")]
    
    if txt_files:
        st.header("Project Logs")
        # ファイル名を選択するセレクトボックス
        selected_file = st.selectbox("Select a file to view its content:", txt_files)
        
        if selected_file:
            # ファイルの内容を表示
            file_path = folder_path / selected_file
            with file_path.open("r", encoding="utf-8") as file:
                content = file.read()
                st.text_area(f"Content of {selected_file}", content, height=400)
    else:
        st.warning("No TXT files found in the 'Project logs' folder.")
else:
    st.error(f"Folder '{folder_path}' does not exist.")



