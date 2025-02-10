#!/usr/bin/env python

import os
import time
import logging
from elasticsearch import NotFoundError, Elasticsearch, exceptions as es_exceptions

class ElasticSearchService:
    def __init__(self, index_name: str, logger: logging.Logger):
        self.logger = logger
        self.index_name = index_name
        self.es = self.get_es_client()
        if self.es is None:
            self.logger.error("Elasticsearch client not available.")
            raise RuntimeError("Elasticsearch client not available.")
        self.create_index_if_not_exists()

    def create_index_if_not_exists(self) -> bool:
        try:
            if self.es.indices.exists(index=self.index_name):
                self.logger.info(f"Elasticsearch index '{self.index_name}' already exists")
                return True
            mapping = {
                "mappings": {
                    "properties": {
                        "text": {"type": "text"}
                    }
                }
            }
            # updated parameters for index creation
            self.es.indices.create(
                index=self.index_name,
                mappings=mapping.get("mappings", {}),
                settings=mapping.get("settings", {})
            )
            self.logger.info(f"Created Elasticsearch index: {self.index_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create Elasticsearch index: {e}")
            return False

    def index_document(self, doc_id: str, document: dict) -> bool:
        try:
            res = self.es.index(index=self.index_name, id=doc_id, document=document)
            if res.get("result") in ["created", "updated"]:
                self.logger.info(f"Indexed document {doc_id}")
                return True
            self.logger.error(f"Indexing document {doc_id} returned unexpected result: {res.get('result')}")
            return False
        except Exception as e:
            self.logger.error(f"Exception indexing document {doc_id}: {e}")
            return False

    def get_document(self, doc_id: str):
        try:
            res = self.es.get(index=self.index_name, id=doc_id)
            self.logger.info(f"Retrieved document {doc_id}")
            return res["_source"]
        except NotFoundError:
            self.logger.warning(f"Document not found: {doc_id}")
            return None
        except Exception as e:
            self.logger.error(f"Exception retrieving document {doc_id}: {e}")
            return None

    def search_documents(self, query: str, size: int):
        try:
            res = self.es.search(index=self.index_name, query={"match": {"text": query}}, size=size)
            hits = res["hits"]["hits"]
            self.logger.info(f"Search for query '{query}' returned {len(hits)} results")
            return hits
        except Exception as e:
            self.logger.error(f"Search failed for query '{query}': {e}")
            return []

    # I really dont like doing this...
    def running_in_docker(self) -> bool:
        return os.path.exists("/.env_docker")

    def get_es_client(self):
        es_host = "http://elasticsearch:9200" if self.running_in_docker() else "http://localhost:9200"
        RETRY_INTERVAL = 5
        MAX_RETRIES = 5

        for attempt in range(MAX_RETRIES):
            try:
                es_client = Elasticsearch(es_host)
                if es_client.ping():
                    self.logger.info(f"Connected to Elasticsearch at {es_host}")
                    return es_client
                self.logger.warning(f"Elasticsearch at {es_host} not responsive. Attempt {attempt + 1}/{MAX_RETRIES}")
            except es_exceptions.ConnectionError as e:
                self.logger.warning(f"Connection failed: {e}. Retrying in {RETRY_INTERVAL}s...")
            time.sleep(RETRY_INTERVAL)
        
        self.logger.error("Failed to connect to Elasticsearch after several retries.")
        return None
