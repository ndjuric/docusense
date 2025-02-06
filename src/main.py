#!/usr/bin/env python
import os
import time
import logging
from fastapi import FastAPI
import uvicorn
from elastic_search_service import ElasticSearchService
from llm_service import LLMService
from docu_sense_service import DocuSenseService
from docu_sense_api import DocuSenseAPI
from squirro_types import Document

# --- Setup Filesystem and Logging ---
from logging_setup import AppLogger
app_logger = AppLogger().get_logger()
ES_INDEX_NAME = "documents"
# --- Service Setup ---
es_service = ElasticSearchService(ES_INDEX_NAME, logger=app_logger)  # Adjust constructor parameters as needed
llm_service = LLMService(logger=app_logger)
docu_sense_service = DocuSenseService(es_service, llm_service, logger=app_logger)

# --- FastAPI Application Setup ---
app = FastAPI(
    title="DocuSense",
    description="Store, retrieve, and search natural language documents with optional LLM-generated answers.",
    version="0.1.6",
)

# Instantiate your API controller and include its router.
docu_api = DocuSenseAPI(docu_sense_service)
app.include_router(docu_api.router)

# Optional: run the application.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
