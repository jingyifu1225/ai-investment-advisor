import json
import logging
from typing import List, Sequence

import nest_asyncio
from llama_index.core import Document, SimpleDirectoryReader, StorageContext
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import JSONNodeParser, SentenceSplitter
from llama_index.core.schema import BaseNode
from llama_index.core.vector_stores.types import BasePydanticVectorStore

nest_asyncio.apply()

logger = logging.getLogger(__name__)


class RagIngestionPipeline:

    def __init__(
            self, embedding_model: BaseEmbedding, vector_store: BasePydanticVectorStore
    ):
        self.__vector_store = vector_store
        self.pipeline = IngestionPipeline(
            transformations=[
                # JSONNodeParser(include_metadata=True),
                SentenceSplitter(chunk_size=1024, chunk_overlap=256),
                # TitleExtractor(),
                embedding_model,
            ],
            vector_store=vector_store,
            # cache=IngestionCache(
            #     cache=RedisCache(redis_uri=REDIS_URI),
            #     collection="ingestion_pipeline_cache"
            # ),
        )
        '''
        self.scrape_spider_reader = SpiderWebReader(
            api_key=os.getenv("SPIDER_CRAWLER_API"),
            mode="scrape",
        )
        self.crawl_spider_reader = SpiderWebReader(
            api_key=os.getenv("SPIDER_CRAWLER_API"),
            mode="crawl",
        '''

    def ingest_documents(self, documents: List[Document]) -> Sequence[BaseNode]:
        logger.info(f"ingesting {len(documents)} documents...")
        nest_asyncio.apply()
        nodes = self.pipeline.run(documents=documents, num_workers=2)
        return nodes

    def ingest_documents_from_file(self, file_path: str) -> Sequence[BaseNode]:
        logger.info(f"ingesting documents from file: {file_path}")
        documents = self.file_to_document(file_path)
        return self.ingest_documents(documents)

    def ingest_documents_from_directory(
            self, directory_path: str
    ) -> Sequence[BaseNode]:
        logger.info(f"ingesting documents from directory: {directory_path}")
        documents = self.load_data_from_directory(directory_path)
        return self.ingest_documents(documents)

    def ingest_documents_from_webpage(
            self, url: str, metadata: dict = None
    ) -> Sequence[BaseNode]:
        documents = self.scrape_spider_reader.load_data(url=url)
        logger.info(f"loaded {len(documents)} documents from webpage {url}")
        if metadata:
            for doc in documents:
                doc.metadata = metadata
        return self.ingest_documents(documents)

    def ingest_documents_from_website(
            self, url: str, metadata: dict = None
    ) -> Sequence[BaseNode]:
        logger.info(f"ingesting documents from website: {url}")
        documents = self.crawl_spider_reader.load_data(url=url)
        logger.info(f"loaded {len(documents)} documents from website {url}")
        if metadata:
            for doc in documents:
                doc.metadata = metadata
        return self.ingest_documents(documents)

    @staticmethod
    def file_to_document(file_path: str) -> List[Document]:
        reader = SimpleDirectoryReader(input_files=[file_path])
        return reader.load_data(show_progress=True)

    @staticmethod
    def load_data_from_directory(directory_path: str) -> List[Document]:
        reader = SimpleDirectoryReader(input_files=[directory_path])
        return reader.load_data(show_progress=True)
