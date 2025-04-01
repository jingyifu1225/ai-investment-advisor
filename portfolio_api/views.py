from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, Instrument
from .serializers import PortfolioSerializer, InstrumentSerializer
import logging

logger = logging.getLogger(__name__)


class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        portfolio = self.get_object()
        return Response({
            'name': portfolio.name,
            'instruments_count': portfolio.instruments.count(),
            'total_value': getattr(portfolio.metrics, 'total_value', 0),
            'profit_loss': getattr(portfolio.metrics, 'profit_loss', 0),
        })

    @action(detail=True, methods=['post'])
    def ai_analysis(self, request, pk=None):
        portfolio = self.get_object()

        try:
            from rag_pipeline.query_router import QueryRouter
            query_router = QueryRouter()

            result = query_router.route_query(
                query="Analyze this portfolio and provide investment advice",
                user_id=request.user.id,
                portfolio_id=portfolio.id
            )

            return Response({"advice": str(result)})
        except Exception as e:
            logger.error(f"AI analysis failed: {e}", exc_info=True)
            return Response({"error": f"AI analysis failed: {str(e)}"}, status=500)

    @action(detail=False, methods=['post'])
    def query(self, request):
        query_text = request.data.get('query', '')

        try:
            from rag_pipeline.query_router import QueryRouter
            query_router = QueryRouter()

            result = query_router.route_query(query_text, user_id=request.user.id)
            result_str = str(result)

            # if empty
            if result_str.strip() == "Empty Response" or not result_str.strip():
                # return OpenAI response
                from llama_index.llms.openai import OpenAI
                from rag_pipeline.constants import OPEN_AI_API_KEY, OPEN_AI_MODEL

                llm = OpenAI(api_key=OPEN_AI_API_KEY, model=OPEN_AI_MODEL)
                direct_response = llm.complete(query_text)

                return Response({
                    "answer": str(direct_response),
                    "sources": [],
                    "source_type": "direct_llm"
                })

            return Response({
                "answer": result_str,
                "sources": []
            })
        except Exception as e:
            return Response({"error": f"Query failed: {str(e)}"}, status=500)


class InstrumentViewSet(viewsets.ModelViewSet):
    serializer_class = InstrumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Instrument.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        portfolio_id = self.kwargs.get('portfolio_pk')
        portfolio = Portfolio.objects.get(id=portfolio_id, user=self.request.user)
        serializer.save(portfolio=portfolio)