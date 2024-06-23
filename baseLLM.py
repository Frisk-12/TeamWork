# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:42:37 2024

@author: AGO6359
"""

from openai import OpenAI
import io
import requests
from typing import Union, List

file_path= "/Users/andreadesogus/Downloads/api_key.txt"
with open(file_path, 'r') as f:
        api_key = f.read()

class openaiApis:
    def __init__(self):
        self.api_key = api_key
        self.client = OpenAI(api_key = self.api_key)

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

    def gptText(self, system: str, question: str = None, message: List = None, tools = None, tool_choice = None, _format: str = "text") -> str:
        """
        Builds a response using the specified OpenAI client and parameters.
    
        Args:
            system (str): The system message to include in the conversation.
            text (str): The user's input text.
            format_ (str): The format of the response. Possible values are "json" or anything else for default.
    
        Returns:
            tuple: A tuple containing the response message and the total tokens used.
        """
        
        messages = [
            {"role": "system", "content": system},
        ]
        
        if question:
            user = [{"role": "user", "content": question}]
            messages = messages + user
            
        if message:
            messages = messages + message
        
        if _format == "json":
            completion = self.client.chat.completions.create(
                model="gpt-4o",# "gpt-3.5-turbo-1106" 
                response_format={"type": "json_object"},
                messages=messages,
                tools=tools,
                tool_choice=tool_choice
            )
        else:
            completion = self.client.chat.completions.create(
                model="gpt-4o",# "gpt-3.5-turbo-1106"
                messages=messages,
                max_tokens=3000,
                tools=tools,
                tool_choice=tool_choice
            )

        return completion#.choices[0].message.content


    