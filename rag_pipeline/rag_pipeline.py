import json
import logging

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.readers.json import JSONReader
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from .mongo_singleton_client import MongoDBClient

from .constants import (
    MONGO_ATLAS_VECTOR_INDEX_NAME,
    MONGO_DB_COLLECTION,
    MONGO_DB_NAME,
    MONGO_URI,
    OPEN_AI_API_KEY,
    OPEN_AI_MODEL,
)
from .ingestion_pipeline import RagIngestionPipeline
from .retriever import MongoVectorDBRetriever

logger = logging.getLogger(__name__)


class RagPipeline:
    def __init__(
        self,
        mongodb_name: str = None,
        mongodb_collection_name: str = None,
        openai_model: str = None,
    ):
        self.mongo_client = MongoDBClient.get_instance(MONGO_URI)
        if not mongodb_name:
            mongodb_name = MONGO_DB_NAME
        if not mongodb_collection_name:
            mongodb_collection_name = MONGO_DB_COLLECTION
        if not openai_model:
            openai_model = OPEN_AI_MODEL
        print(f"mongodb name is {mongodb_name}, collection name is {mongodb_collection_name}")
        print(f"client type is {type(self.mongo_client)}")
        tmpdb = self.mongo_client["ai_investment_db"]
        print(f"db type is {type(tmpdb)}")
        print(f"db is {tmpdb}")
        print(f"list collections {tmpdb.list_collection_names()}")

        self.vector_store = MongoDBAtlasVectorSearch(
            self.mongo_client,
            db_name=mongodb_name,
            collection_name=mongodb_collection_name,
            vector_index_name=MONGO_ATLAS_VECTOR_INDEX_NAME,
        )
        self.embedding_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            dimensions=256,
            api_key=OPEN_AI_API_KEY,
        )
        self.ingestion_pipeline = RagIngestionPipeline(
            self.embedding_model, self.vector_store
        )
        self.retriever = MongoVectorDBRetriever(self.vector_store, self.embedding_model)
        logger.info(f"Using open ai model {openai_model}")
        self.llm = OpenAI(api_key=OPEN_AI_API_KEY, model=openai_model)
        self.query_engine = RetrieverQueryEngine.from_args(
            self.retriever, llm=self.llm, response_mode=ResponseMode.REFINE
        )

    def ingest_documents_from_file(self, file_path):
        return self.ingestion_pipeline.ingest_documents_from_file(file_path)

    def ingest_documents_from_webpage(self, url: str, metadata: dict = None):
        return self.ingestion_pipeline.ingest_documents_from_webpage(
            url, metadata=metadata
        )

    def ingest_documents_from_website(self, url: str, metadata: dict = None):
        return self.ingestion_pipeline.ingest_documents_from_website(
            url, metadata=metadata
        )

    def ingest_documents_from_json_file(self, file_path):
        documents = JSONReader().load_data(file_path)
        return self.ingestion_pipeline.ingest_documents(documents)

    def query(self, query_str):
        response = self.query_engine.query(query_str)
        return response
