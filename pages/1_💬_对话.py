from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
from llama_index.legacy.callbacks import CallbackManager

# for loading environment variables
from decouple import config
import pathlib

import streamlit as st

from storage_utils import loadindex

@st.cache_resource
def init_models():

    callback_manager = CallbackManager()

    # 读取参数
    api_key = config("API_KEY")
    base_url = config("BASE_URL")
    model_name = config("MODEL_NAME")

    # 加载embed_model
    print("Loading embed_model...")
    embed_model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    embed_model_path = pathlib.Path(st.session_state["project_path"]).joinpath(embed_model_name)
    embed_model = resolve_embed_model("local:" + str(embed_model_path))
    print("embed_model_path:", embed_model_path)
    Settings.embed_model = embed_model
    print("embed_model loaded.")

    # 初始化llm
    print("Initializing llm...")
    llm = OpenAILike(
        api_base=base_url, api_key=api_key, model=model_name, is_chat_model=True, callback_manager=callback_manager
    )
    Settings.llm = llm
    print("llm initialized.")

    return


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的助手，有什么我可以帮助你的吗？"}]


def greet2(question):
    rsp = st.session_state['query_engine'].query(question)
    return rsp


def generate_llama_index_response(prompt_input):
    return greet2(prompt_input)


if __name__ == "__main__":
    st.set_page_config(page_title="rag_demo", page_icon="💬")
    st.title("rag_demo")

    # 初始化模型
    if 'init_models' not in st.session_state:
        init_models()
        st.session_state['init_models'] = True

    # 检查是否已经初始化query_engine
    if 'query_engine' not in st.session_state:
        # init_models()
        st.session_state['query_engine'] = loadindex("test_storage").as_query_engine()

    # 初始化对话记录
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的助手，有什么我可以帮助你的吗？"}]

    # 展示聊天记录
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 清空聊天记录
    st.sidebar.button('清除对话记录', on_click=clear_chat_history)

    # 刷新知识库
    if st.sidebar.button("刷新知识库"):
        st.session_state['query_engine'] = loadindex("test_storage").as_query_engine()
        st.success("知识库已刷新！")

    # 输入对话
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # 生成回复
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama_index_response(prompt)
                placeholder = st.empty()
                placeholder.markdown(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
