#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:40:47 2024

@author: andreadesogus
"""

import inspect
import logging
import json
import time
from typing import Callable, List, Union, Dict, Optional, get_type_hints
from error_handling import ToolInputHandler

logging.basicConfig(level=logging.INFO)

# Definizione della classe base (stub)
class BaseTool:
    def __init__(self, name: str, description: str, params: Union[List[str], None], param_type: Union[List[str], None], param_description: Union[List[str], None]):
        self.name = name
        self.description = description
        self.params = params
        self.param_type = param_type
        self.param_description = param_description

    def execution(self, *args, **kwargs):
        """
        Execute the tool with the provided arguments.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

class CustomTool(BaseTool):
    """
    A class that wraps a callable function and extracts its metadata for tool creation.

    Attributes:
        func (Callable): The function to be wrapped and executed.
        details (Dict[str, Union[str, List[str]]]): Metadata details of the function.
    """
    def __init__(self, func: Callable):
        """
        Initializes a CustomTool instance by extracting function details and setting up the base tool attributes.

        Args:
            func (Callable): The function to be wrapped and executed.
        """
        if not callable(func):
            raise TypeError("The provided argument must be a callable (function).")

        self.func = func
        func_details = self._extract_function_details()

        # Initialize the base class with the extracted function details
        super().__init__(
            name=func_details["name"],
            description=func_details["description"],
            params=func_details["params"],
            param_type=func_details["param_types"],
            param_description=func_details["param_descriptions"]
        )
        self.details = func_details
        logging.info(f"CustomTool for function '{self.func.__name__}' initialized successfully with details: {self.details}")

    def _extract_function_details(self) -> Dict[str, Union[str, List[str], List[Optional[type]]]]:
        """
        Extracts details from the function such as name, parameter types, and descriptions.

        Returns:
            Dict[str, Union[str, List[str], List[Optional[type]]]]: A dictionary containing the function details.
        """
        func_name = self.func.__name__
        func_params = list(inspect.signature(self.func).parameters.keys())
        func_param_types = [get_type_hints(self.func).get(param, None) for param in func_params]
        docstring = self.func.__doc__

        # Parse the docstring to get the description and parameter descriptions
        description, param_descriptions = self._parse_docstring(docstring)

        # Log a warning if the number of parameters and descriptions do not match
        if len(func_params) != len(param_descriptions):
            logging.warning(f"Number of parameters and descriptions do not match for function '{func_name}'.")

        return {
            "name": func_name,
            "description": description,
            "params": func_params,
            "param_types": func_param_types,
            "param_descriptions": param_descriptions
        }

    def _parse_docstring(self, docstring: Optional[str]) -> (str, List[str]):
        """
        Parses the docstring to extract the function description and parameter descriptions.

        Args:
            docstring (Optional[str]): The docstring to be parsed.

        Returns:
            tuple: A tuple containing the description and a list of parameter descriptions.
        """
        if not docstring:
            return "No description available.", ["No parameter descriptions available."]

        lines = docstring.strip().split("\n")
        # The first line of the docstring is considered as the description
        description = lines[0].strip() if lines else "No description available."

        param_descriptions = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith(":param"):
                # Extract parameter description from lines starting with ':param'
                param_descriptions.append(line.split(":param")[1].strip())
            elif line:
                # Append any other non-empty line as a parameter description
                param_descriptions.append(line)

        if not param_descriptions:
            param_descriptions = ["No parameter descriptions available."]

        return description, param_descriptions

    def execution(self, *args, **kwargs):
        """
        Executes the stored function with the provided arguments.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: The result of the function execution.
        """
        try:
            result = self.func(*args, **kwargs)
            logging.info(f"Function '{self.func.__name__}' executed successfully.")
            return result
        except Exception as e:
            logging.error(f"Error executing function '{self.func.__name__}': {e}")
            raise

    def get_details(self) -> Dict[str, Union[str, List[str], List[Optional[type]]]]:
        """
        Returns the details of the function.

        Returns:
            Dict[str, Union[str, List[str], List[Optional[type]]]]: A dictionary containing the function details.
        """
        return self.details


class OpenaiFunctionCalling:
    """
    A class to manage and generate function definitions for a list of CustomTool instances.

    Attributes:
        tools (List[CustomTool]): List of CustomTool instances representing tools/functions.
    """
    def __init__(self, tools: List[CustomTool]):
        """
        Initializes the OpenaiFunctionCalling instance with a list of CustomTool instances.

        Args:
            tools (List[CustomTool]): List of CustomTool instances.
        """
        self.tools = tools

    def map_param_type(self, param_type: type) -> str:
        """
        Maps the given parameter type to a specific string value based on predefined mappings.

        Args:
            param_type (type): The type of the parameter to be mapped.

        Returns:
            str: The mapped string value representing the parameter type.
        """
        type_mapping = {
            int: 'integer',
            str: 'string',
            float: 'number',
            dict: 'object',
            list: 'array',
            bool: 'boolean',
            type(None): 'null'
        }
        return type_mapping.get(param_type, 'unknown')

    def generate_function_definitions(self) -> List[Dict[str, Union[str, Dict[str, Union[str, Dict[str, Dict[str, List[str]]]]]]]]:
        """
        Generates function definitions for the provided tools.

        Returns:
            List[Dict[str, Union[str, Dict[str, Union[str, Dict[str, Dict[str, List[str]]]]]]]]: List of function definitions.
        """
        function_definitions = []

        for tool in self.tools:
            properties = {}

            # Iterate through parameters, types, and descriptions of the tool
            for param, param_type, param_description in zip(tool.params, tool.param_type, tool.param_description):
                properties[param] = {
                    "type": self.map_param_type(param_type),
                    "description": param_description
                }

            # Construct the function definition object
            function_definitions.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": tool.params
                    }
                }
            })

        return function_definitions

class ToolResponseHandler:
    """
    A class to handle the tool response logic from the OpenAI API.

    Attributes:
        response (object): The response object from the OpenAI API.
        agent (object): The agent object containing the tools.
        ai (object): The OpenAI API client instance.
    """
    def __init__(self, response, agent, ai):
        """
        Initializes the ToolResponseHandler with necessary attributes.

        Args:
            response (object): The response object from the OpenAI API.
            agent (object): The agent object containing the tools.
            ai (object): The OpenAI API client instance.
        """
        self.response = response
        self.agent = agent
        self.ai = ai

    def process_tool_response(self) -> List[Dict[str, Union[str, Dict[str, Union[str, Dict[str, Union[str, str]]]]]]]:
        """
        Process the tool response from the OpenAI API.

        Returns:
            List[Dict[str, Union[str, Dict[str, Union[str, Dict[str, Union[str, str]]]]]]]: A list of messages including the function call responses.
        """
        response_message = self.response.choices[0].message
        tool_calls = response_message.tool_calls
        
        if tool_calls:
            available_functions = {tool.name: tool.func for tool in self.agent.tools}

            message = [response_message]  # Extend conversation with assistant's reply

            # Iterate through each tool call in the response and execute corresponding function dynamically
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions.get(function_name)

                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = self.call_function_dynamically(function_to_call, function_args)
                else:
                    function_response = f"Function '{function_name}' not found in available tools."

                message.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response if function_response is not None else "",
                })  # Extend conversation with function response

            return message

    def call_function_dynamically(self, function_to_call: Callable[..., Union[str, int, float, dict, list, None]], 
                                  function_args: Dict[str, Union[str, int, float, bool, dict, list, None]], 
                                  retries: int = 3) -> Union[str, int, float, dict, list, None]:
        """
        Dynamically call a function with retry logic.
    
        Args:
            function_to_call (Callable[..., Union[str, int, float, dict, list, None]]): The function to call.
            function_args (Dict[str, Union[str, int, float, bool, dict, list, None]]): The arguments for the function.
            retries (int, optional): Number of retry attempts. Default is 3.
    
        Returns:
            Union[str, int, float, dict, list, None]: The result of the function call, or None if all retries fail.
    
        Raises:
            Exception: Re-raises the last exception if all retries fail.
        """
        combined_args = {**function_args}
        attempt = 0
        last_exception = None
    
        while attempt < retries:
            try:
                # print("\n\n\n\n\n---------")
                # print(str(combined_args))
                # print("---------\n\n\n\n\n")
                return function_to_call(**combined_args)
            except FileNotFoundError as e:
                print(f"Attempt {attempt + 1} failed (FileNotFoundError): {e}")
                last_exception = e
            except TypeError as e:
                print(f"Attempt {attempt + 1} failed (TypeError): {e}")
                last_exception = e
            except Exception as e:
                print(f"Attempt {attempt + 1} failed (Exception): {e}")
                last_exception = e
            
            solver = ToolInputHandler()
            combined_args = solver.solve(self.agent, CustomTool(function_to_call), self.ai)
            attempt += 1
            time.sleep(1)  # Wait for a second before retrying
    
        # If all retries fail, re-raise the last exception
        if last_exception:
            raise last_exception
    
        # Return None if all retries fail
        return None