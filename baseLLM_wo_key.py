# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:42:37 2024

@author: andreadesogus
"""

from openai import OpenAI
from typing import List

class openaiApis:
    
    def __init__(self):
        """
        Initializes the openaiApis class with the given API key.
        """
        self.api_key = "YOUR_OPENAI_API_KEY"
        self.client = OpenAI(api_key=self.api_key)

    def embeddings(self, text: str) -> list:
        """
        Retrieves embeddings for the given text using the specified OpenAI client.
    
        Args:
            text (str): The input text for which embeddings are to be retrieved.
    
        Returns:
            list: A list containing the embeddings for the input text.
        """
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-large",
            dimensions=3072
        )
        embeddings = response.data[0].embedding
        return embeddings

    def gptText(self, system: str, question: str, message: List[dict] = None, _format: str = "text") -> str:
        """
        Builds a response using the specified OpenAI client and parameters.
    
        Args:
            system (str): The system message to include in the conversation.
            question (str): The user's input text.
            message (List[dict], optional): Additional messages to include in the conversation.
            _format (str): The format of the response. Possible values are "json" or "text".
    
        Returns:
            str: The response message content.
        """
        messages = [{"role": "system", "content": system}]
        
        if question:
            messages.append({"role": "user", "content": question})
            
        if message:
            messages.extend(message)
        
        if _format == "json":
            completion = self.client.chat.completions.create(
                model="gpt-4o",  # "gpt-3.5-turbo-1106"
                response_format={"type": "json_object"},
                messages=messages
            )
        else:
            completion = self.client.chat.completions.create(
                model="gpt-4o",  # "gpt-3.5-turbo-1106"
                messages=messages,
                max_tokens=3000
            )

        return completion.choices[0].message.content
