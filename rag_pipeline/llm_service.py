'''
import os
from sqlalchemy import create_engine
from django.conf import settings
from llama_index.core import SQLDatabase
from llama_index.core.indices.struct_store import SQLStructStoreIndex
from llama_index.llms.openai import OpenAI


class PortfolioLLMService:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        engine = create_engine(
            f"postgresql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}@{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/{settings.DATABASES['default']['NAME']}"
        )

        self.sql_database = SQLDatabase(engine)
        self.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        self.index = SQLStructStoreIndex.from_documents(
            [],
            sql_database=self.sql_database,
            table_name="portfolio_api_portfolio",
            llm=self.llm
        )

    def query_portfolio(self, user_query, user_id=None):
        if user_id:
            query_str = f"For user_id={user_id}: {user_query}"
        else:
            query_str = user_query

        query_engine = self.index.as_query_engine(synthesize_response=True)
        response = query_engine.query(query_str)
        return response.response

    def generate_investment_advice(self, portfolio_id):
        query_str = f"Analyze portfolio with id={portfolio_id} and provide investment recommendations."
        query_engine = self.index.as_query_engine(synthesize_response=True)
        response = query_engine.query(query_str)
        return response.response
'''