import asyncio
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from functools import partial
from typing import Callable, Dict, List, Optional, Type, Union, cast
import networkx as nx
import tiktoken,json


from ._llm import (
    gpt_4o_complete,
    gpt_4o_mini_complete,
    openai_embedding,
    azure_gpt_4o_complete,
    azure_openai_embedding,
    azure_gpt_4o_mini_complete,
)
from ._op import (
    chunking_by_token_size,
    extract_entities,
    generate_community_report,
    get_chunks,
    single_time_query,
    global_query,
    naive_query,
)
from ._storage import (
    JsonKVStorage,
    NanoVectorDBStorage,
    NetworkXStorage,
)
from ._utils import (
    EmbeddingFunc,
    compute_mdhash_id,
    limit_async_func_call,
    convert_response_to_json,
    always_get_an_event_loop,
    logger,
)
from .base import (
    BaseGraphStorage,
    BaseKVStorage,
    BaseVectorStorage,
    StorageNameSpace,
    QueryParam,
)


@dataclass
class GraphRAG:
    working_dir: str = field(
        default_factory=lambda: f"./nano_graphrag_cache_{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
    ) #每当你创建一个 GraphRAG 的实例时，working_dir 属性会自动被赋值为一个包含当前时间戳的文件夹路径。
    
    time:str="None"
    # graph mode
    enable_local: bool = True
    enable_naive_rag: bool = False

    # text chunking
    chunk_func: Callable[
        [
            list[list[int]],
            List[str],
            tiktoken.Encoding,
            Optional[int],
            Optional[int],
        ],
        List[Dict[str, Union[str, int]]],
    ] = chunking_by_token_size
    '''
    chunk_func 变量的默认值是 chunking_by_token_size 函数，这个函数接受一个标记列表、文本列表、编码对象以及可选的分块大小和重叠大小，返回一个包含字典（包含文本和标记）的列表。
    '''
    chunk_token_size: int = 1000
    chunk_overlap_token_size: int = 100 #这个属性表示相邻文本块之间的 token 重叠数。
    tiktoken_model_name: str = "gpt-4o"

    # entity extraction
    entity_extract_max_gleaning: int = 1 #循环补充提取（最多 entity_extract_max_gleaning 次）。
    entity_summary_to_max_tokens: int = 500 #该参数表示从实体提取中生成的摘要或描述文本最多可以包含多少个 token。

    # node embedding
    node_embedding_algorithm: str = "node2vec"
    node2vec_params: dict = field(
        default_factory=lambda: {
            "dimensions": 1536,
            "num_walks": 10,
            "walk_length": 40,
            "num_walks": 10,
            "window_size": 2,
            "iterations": 3, #训练过程中执行的迭代次数
            "random_seed": 3,
        }
    )

    # text embedding
    embedding_func: EmbeddingFunc = field(default_factory=lambda: openai_embedding) #lambda 使得我们能够以一种简洁的方式延迟函数的赋值，而不是立即调用它。
    embedding_batch_num: int = 32 #这个字段指定了每次批处理文本嵌入时的批量大小。设置为 32 表示每次处理 32 个文本样本。
    embedding_func_max_async: int = 16 #这个字段表示在异步执行文本嵌入时的最大并发数。设置为 16 表示最多可以同时发起 16 个并行的嵌入请求。
    query_better_than_threshold: float = 0.2 #这是一个浮动值，用于设置查询结果的相关性阈值。其值为 0.2 表示，查询的结果如果相似度大于 0.2，则认为它是“足够好的”。

    # LLM
    using_azure_openai: bool = False
    best_model_func: callable = gpt_4o_complete #gpt_4o_complete 很可能是一个调用 GPT-4 完整版本 API 的函数。
    best_model_max_token_size: int = 32768
    best_model_max_async: int = 16
    cheap_model_func: callable = gpt_4o_mini_complete
    cheap_model_max_token_size: int = 32768
    cheap_model_max_async: int = 16

    # entity extraction
    entity_extraction_func: callable = extract_entities

    # storage
    key_string_value_json_storage_cls: Type[BaseKVStorage] = JsonKVStorage #JsonKVStorage 是一个自定义的类，用于将数据存储为键值对（key-value）格式的 JSON 文件。BaseKVStorage 是它的父类
    vector_db_storage_cls: Type[BaseVectorStorage] = NanoVectorDBStorage #对于需要进行相似度搜索或检索的任务（如基于向量的检索任务），会使用这个存储类
    vector_db_storage_cls_kwargs: dict = field(default_factory=dict) #用于存储创建向量数据库存储实例时所需的额外参数（例如连接配置、索引设置等）
    graph_storage_cls: Type[BaseGraphStorage] = NetworkXStorage #NetworkXStorage 是一个用于存储图数据的类，继承自 BaseGraphStorage。它可以通过 NetworkX 库来管理和操作图形数据结构
    enable_llm_cache: bool = True

    # extension
    always_create_working_dir: bool = True
    addon_params: dict = field(default_factory=dict)
    convert_response_to_json_func: callable = convert_response_to_json

    def __post_init__(self):
        _print_config = ",\n  ".join([f"{k} = {v}" for k, v in asdict(self).items()]) #asdict(self) 会将当前类实例的属性转换为字典格式（即所有的类属性和它们的值）
        logger.debug(f"GraphRAG init with param:\n\n  {_print_config}\n")

        if self.using_azure_openai:
            # If there's no OpenAI API key, use Azure OpenAI
            if self.best_model_func == gpt_4o_complete:
                self.best_model_func = azure_gpt_4o_complete
            if self.cheap_model_func == gpt_4o_mini_complete:
                self.cheap_model_func = azure_gpt_4o_mini_complete
            if self.embedding_func == openai_embedding:
                self.embedding_func = azure_openai_embedding
            logger.info(
                "Switched the default openai funcs to Azure OpenAI if you didn't set any of it"
            )

        if not os.path.exists(self.working_dir) and self.always_create_working_dir:
            logger.info(f"Creating working directory {self.working_dir}")
            os.makedirs(self.working_dir)

        self.full_docs = self.key_string_value_json_storage_cls(
            namespace="full_docs", global_config=asdict(self)
        ) #具体来说，self.full_docs 存储的是原始文档数据。

        self.text_chunks = self.key_string_value_json_storage_cls(
            namespace="text_chunks", global_config=asdict(self)
        ) #这是另一个存储类，用于存储文档的分块数据（可能是分段或分词后的文本）

        self.llm_response_cache = (
            self.key_string_value_json_storage_cls(
                namespace="llm_response_cache", global_config=asdict(self)
            )
            if self.enable_llm_cache
            else None
        )


        self.chunk_entity_relation_graph = self.graph_storage_cls(
            namespace="chunk_entity_relation", global_config=asdict(self)
        )

        self.embedding_func = limit_async_func_call(self.embedding_func_max_async)(
            self.embedding_func
        )
        self.entities_vdb = (
            self.vector_db_storage_cls(
                namespace="entities",
                global_config=asdict(self),
                embedding_func=self.embedding_func,
                meta_fields={"entity_name"},
            )
            if self.enable_local
            else None
        )
        self.chunks_vdb = (
            self.vector_db_storage_cls(
                namespace="chunks",
                global_config=asdict(self),
                embedding_func=self.embedding_func,
            )
            if self.enable_naive_rag
            else None
        )

        self.best_model_func = limit_async_func_call(self.best_model_max_async)(
            partial(self.best_model_func, hashing_kv=self.llm_response_cache)
        )
    
    async def search_done(self):
        tasks = []
        for storage_inst in [
            self.entities_vdb,
            self.chunk_entity_relation_graph,
        ]:
            if storage_inst is None:
                continue
            tasks.append(cast(StorageNameSpace, storage_inst).index_done_callback())
        await asyncio.gather(*tasks)    

    def search_graph(self, param:QueryParam = QueryParam()):
        loop = always_get_an_event_loop()
        return loop.run_until_complete(self.asearch(param))

    async def asearch(self,param:QueryParam = QueryParam()):
        if param.mode == 1:
            '''
            提取单个时间点的节点图数据
            '''
            graph_path = os.path.join(self.working_dir, 'merged_graph.graphml')
            chunks_path=os.path.join(self.working_dir,'kv_store_text_chunks.json')
            with open(chunks_path, 'r', encoding='utf-8') as f:
                chunks_json = json.load(f)
            graph = nx.read_graphml(graph_path)
            nodes_data= list(graph.nodes(data=True))
            use_nodes_data=[]
            for node_name, node_data in nodes_data:
                timestap=node_data["timestamp"]
                if str(timestap)==param.time: #未增量的节点
                    use_nodes_data.append((node_name,node_data))
                    await self.chunk_entity_relation_graph.upsert_node(node_name,node_data)# 检索图中，插入节点数据
                else:        
                    time_list = str(timestap).split("<SEP>")
                    if param.time in time_list:
                        # 过滤时间点的描述
                        descriptions_list=node_data['description'].split('<SEP>')
                        descriptions_list = [desc.strip('"') for desc in descriptions_list]                       
                        time_str=f"-data from {param.time}-"
                        filtered_descriptions = [item for item in descriptions_list if time_str in item]
                        node_data['description'] = '<SEP>'.join(filtered_descriptions)
                        # 过滤chunks的描述
                        chunks_list=node_data['source_id'].split('<SEP>')
                        filtered_chunks = [chunk for chunk in chunks_list if chunks_json.get(chunk, {}).get('time') == f"data from {param.time}"]
                        node_data['source_id'] = '<SEP>'.join(filtered_chunks)
                        use_nodes_data.append((node_name,node_data))
                        await self.chunk_entity_relation_graph.upsert_node(node_name,node_data)# 检索图中，插入节点数据
            if len(use_nodes_data)==0:
                print("无数据")                       
            """
            生成节点嵌入
            """
            data_for_vdb = {
                compute_mdhash_id(node_name, prefix="ent-"): {
                    "content": node_name + node_data['description'],
                    "entity_name": node_name,
                }
                for node_name, node_data in use_nodes_data
            }
            await self.entities_vdb.upsert(data_for_vdb)
            '''
            提取单个时间点的边数据
            '''
            use_edges_data=[]
            for u, v, edge_data in graph.edges(data=True):
                timestap=edge_data["timestamp"]
                if str(timestap)==param.time:
                    use_edges_data.append((u, v, edge_data))
                    edge_data["weight"]=float(edge_data["weight"])
                    await self.chunk_entity_relation_graph.upsert_edge(u, v, edge_data)
                else:
                    time_list = str(timestap).split("<SEP>")
                    if param.time in time_list:
                        # 过滤时间点的描述
                        descriptions_list=edge_data['description'].split('<SEP>')
                        descriptions_list = [desc.strip('"') for desc in descriptions_list]
                        time_str=f"-data from {param.time}-"
                        filtered_descriptions = [item for item in descriptions_list if time_str in item]
                        edge_data['description'] = '<SEP>'.join(filtered_descriptions)
                        #print(node_data['description'])
                        # 过滤chunks的描述
                        chunks_list=edge_data['source_id'].split('<SEP>')
                        filtered_chunks = [chunk for chunk in chunks_list if chunks_json.get(chunk, {}).get('time') == f"data from {param.time}"]
                        edge_data['source_id'] = '<SEP>'.join(filtered_chunks)
                        use_edges_data.append((u, v, edge_data))
                        #更新权重
                        weight_list=edge_data['weight'].split('<SEP>')
                        int_weight=[float(num) for num in weight_list]
                        new_weight=max(int_weight)+len(weight_list)
                        edge_data["weight"]=float(new_weight)
                        await self.chunk_entity_relation_graph.upsert_edge(u, v, edge_data)
            
            #new_loop = asyncio.new_event_loop()
            #asyncio.set_event_loop(new_loop)

            #loop = asyncio.get_event_loop()
            #loop.run_until_complete(self.search_done())
            await self.chunk_entity_relation_graph.index_done_callback()
            await self.entities_vdb.index_done_callback() 
        
        
        if param.mode in [2, 3, 4]:
            '''
            提取多个时间点的节点图数据
            '''
            graph_path = os.path.join(self.working_dir, 'merged_graph.graphml')
            chunks_path=os.path.join(self.working_dir,'kv_store_text_chunks.json')
            with open(chunks_path, 'r', encoding='utf-8') as f:
                chunks_json = json.load(f)
            graph = nx.read_graphml(graph_path)
            nodes_data= list(graph.nodes(data=True))
            use_nodes_data=[]
            for node_name, node_data in nodes_data:
                timestap=node_data["timestamp"]
                if str(timestap) in param.time: #未增量的节点
                    use_nodes_data.append((node_name,node_data))
                    await self.chunk_entity_relation_graph.upsert_node(node_name,node_data)# 检索图中，插入节点数据
                else:        
                    time_list = str(timestap).split("<SEP>")
                    query_times = [year for year in time_list if year in param.time]
                    if len(query_times) > 0:
                        # 过滤时间点的描述
                        descriptions_list=node_data['description'].split('<SEP>')
                        descriptions_list = [desc.strip('"') for desc in descriptions_list]
                        filtered_descriptions=[]                       
                        for query_time in query_times:
                            time_str=f"-data from {query_time}-"
                            filtered_descriptions.extend([item for item in descriptions_list if time_str in item])
                        node_data['description'] = '<SEP>'.join(filtered_descriptions)
                        # 过滤chunks的描述
                        chunks_list=node_data['source_id'].split('<SEP>')
                        filtered_chunks=[]
                        for query_time in query_times:
                            time_str=f"-data from {query_time}-"
                            filtered_chunks.extend([chunk for chunk in chunks_list if chunks_json.get(chunk, {}).get('time') ==  f"data from {query_time}"])
                        node_data['source_id'] = '<SEP>'.join(filtered_chunks)
                        use_nodes_data.append((node_name,node_data))
                        await self.chunk_entity_relation_graph.upsert_node(node_name,node_data)# 检索图中，插入节点数据
            if len(use_nodes_data)==0:
                print("无数据")                       
            """
            生成节点嵌入
            """
            data_for_vdb = {
                compute_mdhash_id(node_name, prefix="ent-"): {
                    "content": node_name + node_data['description'],
                    "entity_name": node_name,
                }
                for node_name, node_data in use_nodes_data
            }
            await self.entities_vdb.upsert(data_for_vdb)
            '''
            提取单个时间点的边数据
            '''
            use_edges_data=[]
            for u, v, edge_data in graph.edges(data=True):
                timestap=edge_data["timestamp"]
                if str(timestap) in param.time:
                    use_edges_data.append((u, v, edge_data))
                    edge_data["weight"]=float(edge_data["weight"])
                    await self.chunk_entity_relation_graph.upsert_edge(u, v, edge_data)
                else:
                    time_list = str(timestap).split("<SEP>")
                    query_times = [year for year in time_list if year in param.time]
                    if len(query_times) > 0:
                        # 过滤时间点的描述
                        descriptions_list=edge_data['description'].split('<SEP>')
                        descriptions_list = [desc.strip('"') for desc in descriptions_list]
                        filtered_descriptions=[]                       
                        for query_time in query_times:
                            time_str=f"-data from {query_time}-"
                            filtered_descriptions.extend([item for item in descriptions_list if time_str in item])                       
                        edge_data['description'] = '<SEP>'.join(filtered_descriptions)
                        #print(node_data['description'])
                        # 过滤chunks的描述
                        chunks_list=edge_data['source_id'].split('<SEP>')
                        filtered_chunks=[]
                        for query_time in query_times:
                            time_str=f"-data from {query_time}-"
                            filtered_chunks.extend([chunk for chunk in chunks_list if chunks_json.get(chunk, {}).get('time') ==  f"data from {param.time}"])
                        node_data['source_id'] = '<SEP>'.join(filtered_chunks)
                        use_edges_data.append((u, v, edge_data))
                        #更新权重
                        weight_list=edge_data['weight'].split('<SEP>')
                        int_weight=[float(num) for num in weight_list]
                        new_weight=max(int_weight)+len(weight_list)
                        edge_data["weight"]=float(new_weight)
                        await self.chunk_entity_relation_graph.upsert_edge(u, v, edge_data)
            
            #new_loop = asyncio.new_event_loop()
            #asyncio.set_event_loop(new_loop)

            #loop = asyncio.get_event_loop()
            #loop.run_until_complete(self.search_done())
            await self.chunk_entity_relation_graph.index_done_callback()
            await self.entities_vdb.index_done_callback() 
        return     
    
    def insert(self, string_or_strings):
        loop = always_get_an_event_loop()
        return loop.run_until_complete(self.ainsert(string_or_strings))

    def query(self, query: str, param: QueryParam = QueryParam()):
        loop = always_get_an_event_loop()
        return loop.run_until_complete(self.aquery(query, param))



    async def aquery(self, query: str, param: QueryParam = QueryParam()):
        if param.mode in [1,2,3,4]:            
            response = await single_time_query(
                query,
                self.chunk_entity_relation_graph,
                self.entities_vdb,
                self.text_chunks,
                param,
                asdict(self),
            )
        elif param.mode == 10:
            response = await many_time_query(
                query,
                self.chunk_entity_relation_graph,
                self.entities_vdb,
                self.text_chunks,
                param,
                asdict(self),
            )
        elif param.mode == 11:
            response = await time_interval(
                query,
                self.chunks_vdb,
                self.text_chunks,
                param,
                asdict(self),
            )
        else:
            raise ValueError(f"Unknown mode {param.mode}")
        await self._query_done()
        return response

    async def ainsert(self, string_or_strings):
        await self._insert_start()
        try:
            if isinstance(string_or_strings, str):
                string_or_strings = [string_or_strings] #转化为列表
            # ---------- new docs
            new_docs = {
                compute_mdhash_id(c.strip(), prefix="doc-"): {"content": c.strip()}
                for c in string_or_strings
            }
            #对每个文档进行 compute_mdhash_id 操作，生成唯一的文档 ID（通过哈希计算），并将文档内容存储到 new_docs 字典中。这里使用 strip() 去除前后空白字符。
            _add_doc_keys = await self.full_docs.filter_keys(list(new_docs.keys()))
            new_docs = {k: v for k, v in new_docs.items() if k in _add_doc_keys}
            if not len(new_docs):
                logger.warning(f"All docs are already in the storage")
                return
            logger.info(f"[New Docs] inserting {len(new_docs)} docs")
            #使用 filter_keys 检查新文档是否已经存在于存储中，如果文档已经存在，则从 new_docs 中移除，确保只插入新的文档
            # ---------- chunking

            inserting_chunks = get_chunks(
                new_docs=new_docs,
                chunk_func=self.chunk_func,
                overlap_token_size=self.chunk_overlap_token_size,
                max_token_size=self.chunk_token_size,
            )
            #调用 get_chunks 方法对新文档进行分块
            _add_chunk_keys = await self.text_chunks.filter_keys(
                list(inserting_chunks.keys())
            )
            inserting_chunks = {
                k: v for k, v in inserting_chunks.items() if k in _add_chunk_keys
            }
            if not len(inserting_chunks):
                logger.warning(f"All chunks are already in the storage")
                return
            #检查新生成的文档块是否已经存在于存储中，如果存在，则跳过这些块，只插入新的块。
            logger.info(f"[New Chunks] inserting {len(inserting_chunks)} chunks")

            # TODO: no incremental update for communities now, so just drop all
            # ---------- extract/summary entity and upsert to graph
            logger.info("[Entity Extraction]...")
            maybe_new_kg = await self.entity_extraction_func(
                inserting_chunks,
                knwoledge_graph_inst=self.chunk_entity_relation_graph,
                entity_vdb=self.entities_vdb,
                global_config=asdict(self),
            ) #调用 entity_extraction_func 函数从文档块中提取实体，并将这些实体插入到知识图谱中。
            if maybe_new_kg is None:
                logger.warning("No new entities found")
                return
            self.chunk_entity_relation_graph = maybe_new_kg
            # ---------- commit upsertings and indexing
            await self.full_docs.upsert(new_docs)
            await self.text_chunks.upsert(inserting_chunks)
        finally:
            await self._insert_done()

    async def _insert_start(self):
        tasks = []
        for storage_inst in [
            self.chunk_entity_relation_graph,
        ]:
            if storage_inst is None:
                continue
            tasks.append(cast(StorageNameSpace, storage_inst).index_start_callback()) #cast 函数用于将存储实例转换为 StorageNameSpace 类型，以便调用其 index_start_callback 方法。
        await asyncio.gather(*tasks)

    async def _insert_done(self):
        tasks = []
        for storage_inst in [
            self.full_docs,
            self.text_chunks,
            self.llm_response_cache,
            self.entities_vdb,
            self.chunks_vdb,
            self.chunk_entity_relation_graph,
        ]:
            if storage_inst is None:
                continue
            tasks.append(cast(StorageNameSpace, storage_inst).index_done_callback())
        await asyncio.gather(*tasks)

    async def _query_done(self):
        tasks = []
        for storage_inst in [self.llm_response_cache]:
            if storage_inst is None:
                continue
            tasks.append(cast(StorageNameSpace, storage_inst).index_done_callback())
        await asyncio.gather(*tasks)
