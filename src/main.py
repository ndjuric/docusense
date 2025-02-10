#!/usr/bin/env python
from fastapi import FastAPI
import uvicorn
from elastic_search_service import ElasticSearchService
from llm_service import LLMService
from docu_sense_service import DocuSenseService
from docu_sense_api import DocuSenseAPI
from squirro_types import Document

""" Logging! """
from logging_setup import AppLogger
app_logger = AppLogger().get_logger()


""" Services! """
ES_INDEX_NAME = "documents"
es_service = ElasticSearchService(ES_INDEX_NAME, logger=app_logger)
llm_service = LLMService(logger=app_logger)
docu_sense_service = DocuSenseService(es_service, llm_service, logger=app_logger)
docu_api = DocuSenseAPI(docu_sense_service, logger=app_logger)

""" 
FastAPI instance needs to be passed around in some cases and this aligns me favoring composition over inheritance.
I could have put everything in one file, however I like to have my entry point clean and simple
I branch out to various classes
If there is some complexity (ie running in prod/stage vs test/local) I use control flow to tie everything together
In my opinion this makes it easier to test, maintain, read (follow for project newcomers) etc.
I mean this is a small project, but these things actually matter and are, again, from experience a valid topic when designing services.
"""
app = FastAPI(
    title="DocuSense",
    description="Store, retrieve, and search natural language documents with optional LLM-generated answers.",
    version="0.1.6",
)
app.include_router(docu_api.router) #

# Optional: run the application.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
