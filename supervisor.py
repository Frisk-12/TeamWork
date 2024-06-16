# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 15:54:44 2024

Author: andreadesogus
"""

import json
import time
from pydantic import BaseModel, ValidationError
from baseLLM import openaiApis
from agents_ini import SupervisorSystem, DefaultAgentSystem
from agents import Team
from typing import Union

# ANSI escape sequences for colored output
WHITE_NORMAL = "\033[0m"      # Bianco normale
YELLOW_BOLD = "\033[1;33m"    # Giallo in grassetto
GREEN_BOLD = "\033[1;32m"     # Verde in grassetto
RED_BOLD = "\033[1;31m"       # Rosso in grassetto

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
    
    def __init__(self, agents, ai):
        """
        Initializes the Supervisor with a list of agents and an OpenAI API client.
        
        Args:
            agents (list): A list of agents to supervise.
            ai (openaiApis): An instance of the OpenAI API client.
        """
        self.ai: openaiApis = ai
        self.agents = agents

    def ask_agent(self, question: str, agent_role: str) -> str:
        """
        Asks a specific agent a question based on their role.
        
        Args:
            question (str): The question to be asked.
            agent_role (str): The role of the agent to ask the question.
        
        Returns:
            str: The response from the agent.
        """
        for agent in self.agents:
            if agent.agent_role == agent_role:
                print(f"The {agent_role} now will start his job...")
                response = self.ai.gptText(DefaultAgentSystem().system(agent), question)
                return response

    def add_memory(self, output: str) -> list:
        """
        Adds a message to the memory log.
        
        Args:
            output (str): The output to be added to the memory log.
        
        Returns:
            list: A list containing the new memory message.
        """
        return [{'role': 'assistant', 'content': output}]

    def execution(self, question: str) -> list:
        """
        Executes the supervision process for the given question.
        
        Args:
            question (str): The initial question to start the supervision process.
        
        Returns:
            list: A list of messages generated during the supervision process.
        """
        message = []
        stop = False
        i = 0
        output = ""
        
        # Loop until the supervision process is stopped or the maximum iterations are reached
        while not stop and i < len(self.agents) * 2:
            max_retries = 3
            retry_count = 0
            success = False
            validated_resp = None
            
            # Attempt to get a valid response from the supervisor system
            while retry_count < max_retries and not success:
                resp = self.ai.gptText(SupervisorSystem(Team(self.agents)).system(), question, message=message, _format='json')
                print(f"{YELLOW_BOLD}{question}{WHITE_NORMAL}")
                
                try:
                    # Validate the response
                    validated_resp = SupervisionValidation.parse_obj(json.loads(resp))
                    print("---")
                    print(f"{validated_resp}")
                    print("---")
                    success = True
                except ValidationError as e:
                    # Handle validation error
                    print("---")
                    print(resp)
                    print("---")
                    print(f"{WHITE_NORMAL}\nQuesto errore è dovuto alla validazione dei dati, dettagli di seguito:\n")
                    print(f"{YELLOW_BOLD}{e}")
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"{RED_BOLD}Retrying... ({retry_count}/{max_retries}){WHITE_NORMAL}")
                        time.sleep(1)  # Attendere 1 secondo prima di riprovare
                    else:
                        print(f"{RED_BOLD}Maximum retries reached. Exiting...{WHITE_NORMAL}")
                        break
            
            # If the response indicates delegation, ask the specified agent
            if validated_resp and validated_resp.delegation:
                agent_role = validated_resp.agent_role
                question = validated_resp.question
                output = self.ask_agent(question, agent_role)

                # Debug output
                print(f"{RED_BOLD}{question}")
                print(f"{GREEN_BOLD}{output}")
                
                # Add the delegation action and response to the memory log
                message += self.add_memory(f"I'll ask {validated_resp.agent_role} to answer the following question: {question}")
                message += self.add_memory(f"The {validated_resp.agent_role} says: {output}")
            else:
                # Use the provided answer if no delegation is needed
                output = validated_resp.answer if validated_resp else "No valid response."

                # Debug output
                print(f"{GREEN_BOLD}{output}")
                
                # Add the answer to the memory log
                message += self.add_memory(output)
            
            # Check if the process should stop
            stop = validated_resp.stop if validated_resp else True
            i += 1
            print(f"{WHITE_NORMAL}\nIteration number: {i}")
            question = ""

        return message
