from dataclasses import dataclass, field
from typing import TypedDict, Union, Literal, Generic, TypeVar

import numpy as np

from ._utils import EmbeddingFunc


@dataclass
class QueryParam:
    mode: int=5
    time: str="None"
    only_need_context: bool = False
    response_type: str = "Multiple Paragraphs"
    level: int = 2
    top_k: int = 10
    # naive search
    naive_max_token_for_text_unit = 12000
    # local search
    local_max_token_for_text_unit: int = 5200  # 12000 * 0.33
    local_max_token_for_local_context: int = 1000  # 12000 * 0.4
    local_community_single_one: bool = False



TextChunkSchema = TypedDict( #TypedDict 是 Python 中用于定义具有特定字段的字典类型的一种方式，通常用于类型检查和明确字典的结构。
    "TextChunkSchema",
    {"tokens": int, "content": str, "full_doc_id": str, "chunk_order_index": int},
)
'''
tokens: int：这个字段表示文本块的 token 数量。通常在 NLP 中，一个 token 可能是一个单词或一个符号，具体依赖于分词方式。
content: str：这个字段存储文本块的内容，即实际的文本字符串。这个内容通常是从一个较大的文档中分割出来的一部分。
full_doc_id: str：这个字段是一个字符串，表示原始文档的唯一标识符。它通常用于将文本块与其所属的完整文档关联起来。
chunk_order_index: int：这个字段是一个整数，用于表示文本块在原始文档中的顺序索引。它指示该文本块在文档中的位置或顺序。
'''
SingleCommunitySchema = TypedDict(
    "SingleCommunitySchema",
    {
        "level": int,
        "title": str,
        "edges": list[list[str, str]],
        "nodes": list[str],
        "chunk_ids": list[str],
        "occurrence": float,
        "sub_communities": list[str],
    },
)


class CommunitySchema(SingleCommunitySchema):
    report_string: str
    report_json: dict


T = TypeVar("T")


@dataclass
class StorageNameSpace:
    namespace: str
    global_config: dict

    async def index_start_callback(self):
        """commit the storage operations after indexing"""
        pass

    async def index_done_callback(self):
        """commit the storage operations after indexing"""
        pass

    async def query_done_callback(self):
        """commit the storage operations after querying"""
        pass


@dataclass
class BaseVectorStorage(StorageNameSpace):
    embedding_func: EmbeddingFunc
    meta_fields: set = field(default_factory=set)

    async def query(self, query: str, top_k: int) -> list[dict]:
        raise NotImplementedError

    async def upsert(self, data: dict[str, dict]):
        """Use 'content' field from value for embedding, use key as id.
        If embedding_func is None, use 'embedding' field from value
        """
        raise NotImplementedError


@dataclass
class BaseKVStorage(Generic[T], StorageNameSpace):
    async def all_keys(self) -> list[str]:
        raise NotImplementedError

    async def get_by_id(self, id: str) -> Union[T, None]:
        raise NotImplementedError

    async def get_by_ids(
        self, ids: list[str], fields: Union[set[str], None] = None
    ) -> list[Union[T, None]]:
        raise NotImplementedError

    async def filter_keys(self, data: list[str]) -> set[str]:
        """return un-exist keys"""
        raise NotImplementedError

    async def upsert(self, data: dict[str, T]):
        raise NotImplementedError

    async def drop(self):
        raise NotImplementedError


@dataclass
class BaseGraphStorage(StorageNameSpace):
    async def has_node(self, node_id: str) -> bool:
        raise NotImplementedError

    async def has_edge(self, source_node_id: str, target_node_id: str) -> bool:
        raise NotImplementedError

    async def node_degree(self, node_id: str) -> int:
        raise NotImplementedError

    async def edge_degree(self, src_id: str, tgt_id: str) -> int:
        raise NotImplementedError

    async def get_node(self, node_id: str) -> Union[dict, None]:
        raise NotImplementedError

    async def get_edge(
        self, source_node_id: str, target_node_id: str
    ) -> Union[dict, None]:
        raise NotImplementedError

    async def get_node_edges(
        self, source_node_id: str
    ) -> Union[list[tuple[str, str]], None]:
        raise NotImplementedError

    async def upsert_node(self, node_id: str, node_data: dict[str, str]):
        raise NotImplementedError

    async def upsert_edge(
        self, source_node_id: str, target_node_id: str, edge_data: dict[str, str]
    ):
        raise NotImplementedError

    async def clustering(self, algorithm: str):
        raise NotImplementedError

    async def community_schema(self) -> dict[str, SingleCommunitySchema]:
        """Return the community representation with report and nodes"""
        raise NotImplementedError

    async def embed_nodes(self, algorithm: str) -> tuple[np.ndarray, list[str]]:
        raise NotImplementedError("Node embedding is not used in nano-graphrag.")
