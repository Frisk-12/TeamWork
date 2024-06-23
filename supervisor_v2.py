# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 15:54:44 2024

Author: andreadesogus
"""

import json
import time
import logging
import os
from typing import Union, List, Dict, Optional
from pydantic import BaseModel, ValidationError
from baseLLM import openaiApis
from agents_ini import SupervisorSystem, DefaultAgentSystem
from agents import Team
from basetool import OpenaiFunctionCalling, ToolResponseHandler

# ANSI escape sequences for colored output
WHITE_NORMAL = "\033[0m"
YELLOW_BOLD = "\033[1;33m"
GREEN_BOLD = "\033[1;32m"
RED_BOLD = "\033[1;31m"
BLUE_BOLD = "\033[1;34m"

# Define the log path
LOG_DIR = "/Users/andreadesogus/Downloads/TeamWork/"
LOG_FILE = "supervision.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SupervisionValidation(BaseModel):
    """
    A class for validating the supervision response.

    Attributes:
        delegation (bool): Whether to delegate the question to an agent.
        agent_role (Union[None, str]): The role of the agent to delegate the question.
        question (Union[None, str]): The question to be answered by the agent.
        answer (Union[None, str]): The answer to the question.
        stop (bool): Whether to stop the supervision process.
    """
    delegation: bool
    agent_role: Union[None, str]
    question: Union[None, str]
    answer: Union[None, str]
    stop: bool

class Supervisor:
    """
    A class to manage the supervision of agents using OpenAI's API.

    Attributes:
        ai (openaiApis): An instance of the OpenAI API client.
        agents (list): A list of agents to supervise.
    """
    
    def __init__(self, agents: List[Team], ai: openaiApis):
        """
        Initializes the Supervisor with a list of agents and an OpenAI API client.

        Args:
            agents (list): A list of agents to supervise.
            ai (openaiApis): An instance of the OpenAI API client.
        """
        self.ai = ai
        self.agents = agents
        logging.info("Supervisor initialized with agents and OpenAI API client.")

    def ask_agent(self, question: str, agent_role: str, context: Dict) -> str:
        """
        Asks a specific agent a question based on their role.

        Args:
            question (str): The question to be asked.
            agent_role (str): The role of the agent to ask the question.
            context (dict): Contextual information for the agent.

        Returns:
            str: The response from the agent.
        """
        for agent in self.agents:
            if agent.agent_role == agent_role:
                logging.info(f"Asking {agent_role} the question: {question}")

                # Generate the previous context response for the agent
                prev_resp = self._generate_context_response(agent, context)
                
                # Set up the function call parameters for the agent
                functions, function_call = self._setup_function_call(agent)
                
                # Get response from the agent
                response = self.ai.gptText(
                    system=DefaultAgentSystem(agent).system(prev_resp),
                    question=question,
                    tools=functions,
                    tool_choice=function_call
                )

                # Process the response if the agent uses tools
                if agent.tools:
                    tool_response_handler = ToolResponseHandler(response, agent, self.ai)
                    messages = tool_response_handler.process_tool_response()
                    # for msg in messages:
                    #     logging.info(f"Tool Response: {msg}")
                    iteration = 0
                    stop = False
                    
                    while not stop and iteration < 3:
                        try:
                            response = self.ai.gptText(
                                system=DefaultAgentSystem(agent).system(prev_resp),
                                message=messages)
                            stop = True
                        except Exception as e:
                            iteration +=1
                return response.choices[0].message.content

    def _generate_context_response(self, agent, context: Dict) -> str:
        """
        Generates a context response for the agent.

        Args:
            agent: The agent instance.
            context (dict): The context dictionary.

        Returns:
            str: The context response string.
        """
        prev_resp = ""
        if agent.context:
            # Display the context in yellow bold
            #print(f"{YELLOW_BOLD}\n\n\nCONTEXT\n\n\n{WHITE_NORMAL}")
            for agent_context in agent.context:
                if agent_context in context:
                    # Append context information to the response
                    prev_resp += f"- {agent_context} said: {context[agent_context]}\n"
        # else:
        #     # Display "NO CONTEXT" in red bold if no context is provided
        #     print(f"{RED_BOLD}\n\n\nNO CONTEXT\n\n\n{WHITE_NORMAL}")
        return prev_resp

    def _setup_function_call(self, agent):
        """
        Sets up the function call parameters.

        Args:
            agent: The agent instance.

        Returns:
            tuple: A tuple containing functions and function_call.
        """
        functions = None
        function_call = None
        if agent.tools:
            # Generate function definitions for the agent's tools
            functions = OpenaiFunctionCalling(agent.tools).generate_function_definitions()
            function_call = 'auto'
        return functions, function_call

    def add_memory(self, output: str) -> List[Dict]:
        """
        Adds a message to the memory log.

        Args:
            output (str): The output to be added to the memory log.

        Returns:
            list: A list containing the new memory message.
        """
        #logging.info(f"Adding memory: {output}")
        return [{'role': 'assistant', 'content': output}]

    def execution(self, question: str) -> List[Dict]:
        """
        Executes the supervision process for the given question.

        Args:
            question (str): The initial question to start the supervision process.

        Returns:
            list: A list of messages generated during the supervision process.
        """
        messages = []
        stop = False
        iteration = 0
        context = {}

        logging.info(f"Starting execution with question: {question}")

        while not stop and iteration < len(self.agents) * 2:
            # Get a valid response from the supervisor system
            success, validated_resp = self._get_valid_response(question, messages)
            
            if validated_resp and validated_resp.delegation:
                agent_role = validated_resp.agent_role
                question = validated_resp.question
                # Ask the agent the delegated question
                output = self.ask_agent(question, agent_role, context)

                # Update context with the agent's response
                context[agent_role] = output

                # Log and store memory messages
                messages += self.add_memory(f"I'll ask {agent_role} to answer the following question: {question}")
                messages += self.add_memory(f"The {agent_role} says: {output}")
                logging.info(f"{YELLOW_BOLD}{agent_role}: {GREEN_BOLD}{output}{WHITE_NORMAL}")
            else:
                output = validated_resp.answer if validated_resp else "No valid response."
                messages += self.add_memory(output)
                logging.info(f"{YELLOW_BOLD}SUPERVISOR: {GREEN_BOLD}{output}{WHITE_NORMAL}")
            
            stop = validated_resp.stop if validated_resp else True
            iteration += 1
            
            
            logging.info(f"Iteration number: {iteration}")

            # Clear the question for the next iteration
            question = ""

        logging.info("Execution completed.")
        return output

    def _get_valid_response(self, question: str, messages: List[Dict]) -> (bool, Union[SupervisionValidation, None]):
        """
        Attempts to get a valid response from the supervisor system.

        Args:
            question (str): The question to be asked.
            messages (list): The list of messages exchanged.

        Returns:
            tuple: A tuple containing success status and validated response.
        """
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            # Get response from the supervisor system
            response = self.ai.gptText(
                SupervisorSystem(Team(self.agents)).system(),
                question,
                message=messages,
                _format='json'
            ).choices[0].message.content
            try:
                # Validate the response
                validated_resp = SupervisionValidation.parse_obj(json.loads(response))
                #logging.info(f"Validated response: {validated_resp}")
                return True, validated_resp
            except ValidationError as e:
                logging.error(f"Validation error: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    logging.warning(f"Retrying... ({retry_count}/{max_retries})")
                    time.sleep(1)  # Wait before retrying
                else:
                    logging.critical("Maximum retries reached. Exiting...")
                    break
        return False, None
