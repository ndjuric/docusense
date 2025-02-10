#!/usr/bin/env python

import logging


class LLMService:
    """
    Provides LLM-generated answers.
    Currently uses a simulated response; can be extended to use OpenAI or Ollama.
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def generate_answer(self, query: str) -> str:
        # Simulated response. To integrate OpenAI for example, we need OPENAI_API_KEY (unavailable to me currently), etc.
        # then.. having a query, we can call openai.Completion.create(model="text-davinci-003", prompt=query) or so
        # I could try with ollama but I think I'm already past the deadline :)
        self.logger.info("Generating simulated answer for query")
        return f"This is a generated answer for your query: '{query}'. [Simulated LLM response]"