from llama_index.core import (
    SimpleDirectoryReader,
)

import streamlit as st
import pathlib
import re

from storage_utils import loadindex
from text_utils import get_node_name, get_doc_name
from models_utils import init_models

def file_delete_in_local(file, path):
    # 删除文件
    if file is not None:
        file_path = pathlib.Path(path).joinpath('dataFiles', file)
        if file_path.exists():
            file_path.unlink()
            st.success(f"文件 {file} 删除成功！")
        else:
            st.warning(f"文件 {file} 不存在！")

# 下载文件到本地
def file_download2local(file, path):
    if file is not None:
        st.info(f"文件名: {file.name}，文件大小: {file.size / (1024 * 1024):.2f} MB")
        save_path = pathlib.Path(path).joinpath('dataFiles', file.name)

        # 显示进度条
        progress_bar = st.sidebar.progress(value=0, text=f"{file.name} 上传进度 0%")

        # 50MB (1024 * 1024 为 1MB)
        chunk_size = 1024 * 1024 * 50

        # 已写入的字节数
        bytes_written = 0
        with open(save_path, "wb") as f:
            while True:
                # 从上传的文件中按块读取数据
                file_chunk = file.read(chunk_size)
                if not file_chunk:
                    break  # 读取完成

                # 写入到本地文件
                f.write(file_chunk)
                bytes_written += len(file_chunk)

                # 更新进度条
                progress_percent = bytes_written / file.size
                progress_bar.progress(value=progress_percent, text=f"{file.name} 上传进度 {progress_percent:.0%}")

            st.success(f"文件已成功保存，总写入字节数: {bytes_written}")




if __name__ == "__main__":
    st.set_page_config(page_title="kb_demo", page_icon="📖")

    # 初始化模型
    if 'init_models' not in st.session_state:
        init_models()
        st.session_state['init_models'] = True

    # 检查是否已经初始化StorageContext
    if 'index' not in st.session_state:
        st.session_state['index'] = loadindex("test_storage")

    # 知识库内容展示
    st.title("知识库")
    tmp_index = loadindex("test_storage")
    st.write(tmp_index.docstore.get_all_ref_doc_info())

    # 上传文件进入dataFiles和storage
    uploaded_files = st.sidebar.file_uploader("上传文件", accept_multiple_files=True)
    if st.sidebar.button("上传文件"):
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                file_download2local(uploaded_file, st.session_state["project_path"])
                input_file_path = pathlib.Path(st.session_state["project_path"]).joinpath('dataFiles', uploaded_file.name)
                tmp_docs = SimpleDirectoryReader(input_files=[input_file_path], filename_as_id=True).load_data(show_progress=True)
                for doc in tmp_docs:
                    tmp_index.insert(doc, allow_update=True)
                    print("doc:", doc)
                tmp_storage = pathlib.Path(st.session_state["project_path"]).joinpath('test_storage')
                tmp_index.storage_context.persist(persist_dir=tmp_storage)
                print(tmp_index.docstore.get_all_ref_doc_info())
        else:
            tmp_storage = pathlib.Path(st.session_state["project_path"]).joinpath('test_storage')
            tmp_index.storage_context.persist(persist_dir=tmp_storage)
            st.warning("请先上传文件！")
            print(tmp_index.docstore.get_all_ref_doc_info())

    # 展示知识库文件
    doc_options_b = []
    for doc in tmp_index.docstore.get_all_ref_doc_info():
        doc_options_b.append(doc)
    doc_options_a = get_doc_name(doc_options_b)
    # 去除重复的doc
    doc_options = list(set(doc_options_a))

    options = st.sidebar.multiselect(
        label="选择文件",
        options=doc_options,
    )

    # 删除文件
    if st.sidebar.button("删除文件"):
        if options:
            for option in options:
                # 使用正则表达式根据option获取对应文件的所有doc_id
                doc_ids = []
                for doc in doc_options_b:
                    print("doc:", get_node_name(doc))
                    if re.match(rf"{option}(_part_\d+)?", get_node_name(doc)):
                        doc_ids.append(doc)
                print("doc_ids:", doc_ids)
                for doc_id in doc_ids:
                    tmp_index.delete_ref_doc(doc_id, delete_from_docstore=True)
                tmp_storage = pathlib.Path(st.session_state["project_path"]).joinpath('test_storage')
                tmp_index.storage_context.persist(persist_dir=tmp_storage)
                file_delete_in_local(option, st.session_state["project_path"])
                st.success(f"文件 {option} 删除成功！")
        else:
            st.warning("请选择要删除的文件！")
