#!/usr/bin/env python

import uuid
import logging
from elastic_search_service import ElasticSearchService
from llm_service import LLMService

class DocuSenseService:
    """
    High-level service that handles or 'wraps' ES document storage, retrieval, and search.
    I could have inherited from ElasticSearchService, but I chose to use composition instead these things are usually up for debate.
    """
    def __init__(self, es_service: ElasticSearchService, llm_service: LLMService, logger: logging.Logger):
        self.es_service = es_service
        self.llm_service = llm_service
        self.logger = logger

    def create_document(self, text: str) -> dict:
        doc_id = str(uuid.uuid4())
        document = {"text": text}
        if not self.es_service.index_document(doc_id, document):
            self.logger.error("Failed to index document")
            return None
        return {"document_id": doc_id}

    def get_document(self, doc_id: str) -> dict:
        doc = self.es_service.get_document(doc_id)
        if doc is None:
            return None
        return {"document_id": doc_id, "text": doc.get("text", "")}
    
    def refresh_index(self, index_name) -> dict:
        self.es_service.es.indices.refresh(index=index_name)
        return {"message": "Elasticsearch index refreshed."}

    def search_documents(self, query: str, k: int, generate_answer_flag: bool) -> dict:
        hits = self.es_service.search_documents(query, k)
        documents = [{"document_id": hit["_id"], "text": hit["_source"]["text"]} for hit in hits]
        if generate_answer_flag:
            answer = self.llm_service.generate_answer(query)
            return {"answer": answer, "source_documents": documents}
        return {"results": documents}
