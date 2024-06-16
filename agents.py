# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 16:39:22 2024

Author: andreadesogus
"""

from typing import List

class Agent:
    """
    A class representing an agent with specific attributes and capabilities.
    """
    
    def __init__(self, features: dict):
        """
        Initializes the Agent with the given features.
        
        Args:
            features (dict): A dictionary containing the agent's attributes.
        """
        self.agent_role = features.get('agent_role')
        self.backstory = features.get('backstory')
        self.tools = features.get('tools')
        self.resources = features.get('resources')
        self.task_description = features.get('task_description')
        self.expected_output = features.get('expected_output')

    # Uncomment and implement this method if task execution logic is needed
    # def execute_task(self):
    #     # Implement the logic for executing the task using the provided tools
    #     pass

class Team:
    """
    A class representing a team of agents.
    """
    
    def __init__(self, agents: List[Agent]):
        """
        Initializes the Team with a list of agents.
        
        Args:
            agents (List[Agent]): A list of Agent instances.
        """
        self.agents = agents

    def agent_mapping(self) -> dict:
        """
        Creates a mapping of agent roles to their backstories and task descriptions.
        
        Returns:
            dict: A dictionary mapping agent roles to their respective backstories and task descriptions.
        """
        agents_mapping = {}
        for agent in self.agents:
            agents_mapping[agent.agent_role] = {
                'backstory': agent.backstory,
                'task_description': agent.task_description
            }
        return agents_mapping
