from typing import Optional

from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage
)
from llama_index.core.node_parser import SimpleNodeParser
import os


def loadindex(name: str = "storage") -> VectorStoreIndex:
    # check if data indexes already exists
    if not os.path.exists(name):
        # load data
        documents = SimpleDirectoryReader(
            input_dir="dataFiles", filename_as_id=True).load_data(show_progress=True)

        # create nodes parser
        node_parser = SimpleNodeParser.from_defaults(chunk_size=1024)

        # split into nodes
        base_nodes = node_parser.get_nodes_from_documents(documents=documents)

        # creating index
        index = VectorStoreIndex(nodes=base_nodes)
        # index = VectorStoreIndex(nodes=base_nodes, service_context=service_context)

        # store index
        index.storage_context.persist(persist_dir=name)
    else:
        # load existing index
        storage_context = StorageContext.from_defaults(persist_dir=name)
        index = load_index_from_storage(storage_context=storage_context)
    return index



def load_storage_context():
    # load existing index
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    return storage_context
