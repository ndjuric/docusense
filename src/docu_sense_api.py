#!/usr/bin/env python

from fastapi import APIRouter, HTTPException, Query, Form
import logging
from squirro_types import Document

class DocuSenseAPI:
    """
    I like to keep everything object oriented, even stuff like API endpoints.
    """
    def __init__(self, service, logger: logging.Logger):
        self.logger = logger
        self.service = service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        @self.router.post("/documents", summary="Store a document", response_model=dict)
        async def create_document_endpoint(text: str = Form(...)):
            result = self.service.create_document(text)
            if result is None:
                raise HTTPException(status_code=500, detail="Failed to index document")
            return result
        
        @self.router.post("/es_refresh")
        async def refresh_elasticsearch_index():
            """
            Endpoint to manually refresh the Elasticsearch index.
            Useful for testing to ensure data is immediately searchable.
            """
            self.service.refresh_index(self.service.es_service.index_name)
            return {"message": "Elasticsearch index refreshed"}

        @self.router.get("/documents/{document_id}", summary="Retrieve a document", response_model=Document)
        async def get_document_endpoint(document_id: str):
            result = self.service.get_document(document_id)
            if result is None:
                raise HTTPException(status_code=404, detail="Document not found")
            return result

        @self.router.get("/search", summary="Search documents", response_model=dict)
        async def search_documents_endpoint(
            query: str,
            k: int = Query(10, ge=1, description="Maximum number of results to return"),
            generate_answer_flag: bool = Query(
                False,
                alias="generate_answer",
                description="If true, generate a direct answer using LLM simulation"
            )
        ):
            result = self.service.search_documents(query, k, generate_answer_flag)
            return result
