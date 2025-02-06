#!/usr/bin/env python
from pydantic import BaseModel

# Pydantic model for document responses.. I mean I would go for something 'strongly typed' whenever possible
class Document(BaseModel):
    document_id: str
    text: str