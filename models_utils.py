import streamlit as st
import pathlib
from decouple import config
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
from llama_index.legacy.callbacks import CallbackManager

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