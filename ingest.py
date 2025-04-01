import os
import django
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from rag_pipeline.query_router import QueryRouter


def test_rag_pipeline():
    print("Initializing...")

    try:
        router = QueryRouter()

        test_queries = [
            "What is value investing?",
            "Tell me about Warren Buffett's investment philosophy",
            "What are Nancy Pelosi's recent stock trades?",
            "How has the S&P 500 performed this year?"
            "Any investment advice?"
        ]

        # Run each test query
        for i, query in enumerate(test_queries):
            print(f"\nTest Query {i + 1}: {query}")

            try:
                response = router.route_query(query)

                response_str = str(response)
                print(f"Response: {response_str}")
                print("Query processed successfully")

            except Exception as e:
                print(f"Error processing query: {str(e)}")
                import traceback
                traceback.print_exc()

        print("\nRAG pipeline testing completed")

    except Exception as e:
        print(f"Error initializing RAG pipeline: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    logger.info("Starting RAG pipeline test")
    test_rag_pipeline()