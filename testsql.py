#!/usr/bin/env python
import os
import django
from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

# Get database settings from Django
from django.conf import settings

db_settings = settings.DATABASES['default']
database_url = f"postgresql://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings.get('PORT', '5432')}/{db_settings['NAME']}"


def test_text_to_sql():
    """Test the Text-to-SQL functionality"""

    print("Initializing Text-to-SQL engine...")

    try:
        # Create SQLAlchemy engine
        engine = create_engine(database_url)

        # Get tables from your Django app
        from django.apps import apps
        portfolio_tables = [
            model._meta.db_table
            for model in apps.get_app_config('portfolio_api').get_models()
        ]

        print(f"Tables to be queried: {', '.join(portfolio_tables)}")

        # Add table descriptions for better results
        table_descriptions = {
            'portfolio_api_portfolio': 'User investment portfolios with name, description and creation timestamp',
            'portfolio_api_instrument': 'Financial instruments like stocks and bonds in user portfolios with symbol, name, type, quantity and purchase details',
            'portfolio_api_portfoliometrics': 'Performance metrics for portfolios including total value, profit/loss and risk score'
        }

        # Create SQLDatabase instance
        sql_database = SQLDatabase(
            engine,
            include_tables=portfolio_tables,
            table_info=table_descriptions
        )

        # Initialize LLM
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            api_key = input("Enter your OpenAI API key: ")
            os.environ["OPENAI_API_KEY"] = api_key

        llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")

        # Create Text-to-SQL query engine
        query_engine = NLSQLTableQueryEngine(
            sql_database=sql_database,
            tables=portfolio_tables,
            llm=llm
        )

        # Test queries
        test_queries = [
            "List all portfolios",
            "What's the total value of all portfolios?",
            "Show me the top 5 instruments by quantity",
            "Which portfolio has the highest total value?",
            "How many stocks are in each portfolio?"
        ]

        # Run each test query
        for i, query in enumerate(test_queries):
            print(f"\nTest Query {i + 1}: {query}")

            try:
                # Execute the query
                response = query_engine.query(query)

                # Print response
                print(f"SQL Query: {response.metadata.get('sql_query', 'N/A')}")
                print(f"Response: {response}")

            except Exception as e:
                print(f"Error processing query: {str(e)}")
                import traceback
                traceback.print_exc()

        print("\nText-to-SQL testing completed")

    except Exception as e:
        print(f"Error initializing Text-to-SQL engine: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_text_to_sql()