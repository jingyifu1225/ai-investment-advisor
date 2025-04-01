from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import logging
from .query_router import QueryRouter

logger = logging.getLogger(__name__)
query_router = QueryRouter()


# test api
def index(request):
    return HttpResponse("Hello, this is the RAG pipeline!")


@csrf_exempt
def query(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query_text = data.get("query", "")
            user_id = data.get("user_id")
            portfolio_id = data.get("portfolio_id")

            if not query_text:
                return JsonResponse({"error": "Empty query text"}, status=400)

            logger.info(f"Processing query: {query_text} for user: {user_id}")

            result = query_router.route_query(
                query_text,
                user_id=user_id,
                portfolio_id=portfolio_id
            )
            result_str = str(result).strip()

            # check result
            if result_str.strip() == "Empty Response" or not result_str.strip():
                logger.info(f"Empty response detected, transferring to direct LLM")

                try:
                    from llama_index.llms.openai import OpenAI
                    from rag_pipeline.constants import OPEN_AI_API_KEY, OPEN_AI_MODEL
                    llm = OpenAI(api_key=OPEN_AI_API_KEY, model=OPEN_AI_MODEL)
                    direct_response = llm.complete(query_text)

                    result_str = str(direct_response)
                    logger.info(f"Direct LLM response: {result_str[:100]}...")

                    return JsonResponse({
                        "result": result_str,
                        "source": "direct_llm"
                    })
                except Exception as e:
                    logger.error(f"Error with direct LLM: {str(e)}")
                    return JsonResponse({
                        "result": "No information found about your query",
                        "source": "fallback"
                    })

            return JsonResponse({
                "result": result_str,
                "source": "portfolio_sql" if query_router.is_portfolio_related(query_text) and user_id else "rag"
            })
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def ingest_document(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("file")
            try:
                metadata = json.loads(request.POST.get("metadata", "{}") or "{}")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid metadata JSON format"}, status=400)

            if not file:
                return JsonResponse({"error": "No file provided"}, status=400)

            # tmp location
            file_path = f"/tmp/{file.name}"
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            if file.name.endswith(".json"):
                nodes = query_router.rag_pipeline.ingest_documents_from_json_file(file_path)
            else:
                nodes = query_router.rag_pipeline.ingest_documents_from_file(file_path)

            os.remove(file_path)

            return JsonResponse({
                "success": True,
                "message": f"Document ingested successfully",
                "nodes_count": len(nodes)
            })
        except Exception as e:
            logger.error(f"Error ingesting document: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)
