import streamlit as st
import os
import pathlib

# 获得nltk文件夹路径, 用于设置NLTK_DATA环境变量
project_path = pathlib.Path(__file__).absolute().parent
nltk_data_path = pathlib.Path(project_path).joinpath("nltk_data")
print("nltk_data_path:", nltk_data_path)

# 设置NLTK_DATA环境变量
os.environ["NLTK_DATA"] = str(nltk_data_path)

st.set_page_config(
    page_title="你好",
    page_icon="👋",
)

st.session_state["project_path"] = project_path

st.sidebar.success("在上方选择一个演示。")
