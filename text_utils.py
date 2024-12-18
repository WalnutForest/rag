import pathlib
import re
from typing import Optional


def get_node_name(node_path: str | list[str]) -> str | list[str]:
    """
    Get the name of the node from the path.
    :param node_path:
    :return:
    Examples:
    >>> get_node_name("E:\python_project\\rag+streamlit\dataFiles\data.md_part_0")
    'data.md_part_0'
    >>> get_node_name("E:\python_project\\rag+streamlit\dataFiles\data.md_part_1")
    'data.md_part_1'
    >>> get_node_name(["E:\python_project\\rag+streamlit\dataFiles\data.md_part_0", "E:\python_project\\rag+streamlit\dataFiles\data.md_part_1"])
    ['data.md_part_0', 'data.md_part_1']
    """
    if isinstance(node_path, list):
        return [pathlib.Path(node).name for node in node_path]
    else:
        return pathlib.Path(node_path).name

def get_doc_name(doc_path: str | list[str]) -> str | list[str]:
    """
    Get the name of the document from the path.
    :param doc_path:
    :return:
    Examples:
    >>> get_doc_name("E:\python_project\\rag+streamlit\dataFiles\data.md_part_0")
    'data.md'
    >>> get_doc_name("E:\python_project\\rag+streamlit\dataFiles\data.md_part_1")
    'data.md'
    >>> get_doc_name(["E:\python_project\\rag+streamlit\dataFiles\data.md_part_0", "E:\python_project\\rag+streamlit\dataFiles\data.md_part_1"])
    ['data.md', 'data.md']
    """
    # 按照正则表达式去掉"_part_0"等后缀
    if isinstance(doc_path, list):
        return [re.sub(r"_part_\d+", "", pathlib.Path(doc).name) for doc in doc_path]
    else:
        return re.sub(r"_part_\d+", "", pathlib.Path(doc_path).name)