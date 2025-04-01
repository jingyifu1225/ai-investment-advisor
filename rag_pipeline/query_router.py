from re import search

from rag_pipeline.rag_pipeline import RagPipeline


class QueryRouter:
    def __init__(self):
        self._rag_pipeline = RagPipeline()
        self._portfolio_llm = None

        self.portfolio_patterns = [
            r'(?i)my portfolio',
            r'(?i)my investment',
            r'(?i)portfolio performance',
            r'(?i)portfolio id',
            r'(?i)stock performance',
            r'(?i)holdings',
            r'(?i)my assets',
        ]

    @property
    def rag_pipeline(self):
        if self._rag_pipeline is None:
            from .rag_pipeline import RagPipeline
            self._rag_pipeline = RagPipeline()
        return self._rag_pipeline

    @property
    def portfolio_llm(self):
        if self._portfolio_llm is None:
            from .llm_service import PortfolioLLMService
            self._portfolio_llm = PortfolioLLMService()
        return self._portfolio_llm

    def is_portfolio_related(self, query):
        for pattern in self.portfolio_patterns:
            if search(pattern, query):
                return True
        return False

    def route_query(self, query, user_id=None, portfolio_id=None):
        try:
            # if portfolio_id:
            #     return self.portfolio_llm.generate_investment_advice(portfolio_id)
            #
            # if self.is_portfolio_related(query) and user_id:
            #     return self.portfolio_llm.query_portfolio(query, user_id)

            return self.rag_pipeline.query(query)
        except Exception as e:
            print(f"Failed: {e}")
            return f"Error: {str(e)}"