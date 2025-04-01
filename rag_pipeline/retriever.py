import logging
from typing import List, Optional

from llama_index.core import QueryBundle, StorageContext, VectorStoreIndex
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch


class MongoVectorDBRetriever(BaseRetriever):
    def __init__(
        self,
        vector_store: MongoDBAtlasVectorSearch,
        embed_model: BaseEmbedding,
        query_mode: VectorStoreQueryMode = VectorStoreQueryMode.HYBRID,
        similarity_top_k: int = 3,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self._vector_store = vector_store
        self._embed_model = embed_model
        self._query_mode = query_mode
        self._similarity_top_k = similarity_top_k

        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        self.logger.info(f"Retrieving for query: {query_bundle.query_str}")
        query_embedding = self._embed_model.get_query_embedding(query_bundle.query_str)
        vector_store_query = VectorStoreQuery(
            query_embedding=query_embedding,
            embedding_field="embedding",
            similarity_top_k=self._similarity_top_k,
            mode=self._query_mode,
        )
        self.logger.info(f"Vector store query: {vector_store_query}")
        query_result = self._vector_store.query(vector_store_query)
        self.logger.info(f"Query result: {query_result}")
        # print(f"query result {query_result}")

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
            nodes_with_scores.append(NodeWithScore(node=node, score=score))
        self.logger.info(f"Nodes with scores: {nodes_with_scores}")
        return nodes_with_scores
