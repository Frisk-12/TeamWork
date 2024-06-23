#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 16:54:38 2024

@author: andreadesogus
"""

class ToolInputHandler():
    def solve(self, agent, tool, e):
        system = f"""
        You are one of the best Python developers and part of a team of AI agents whose task is to carry out specific duties to complete a complex task. Your specific role is to ensure that the tools available to each agent are functioning properly.

        The agent you need to assist has the following characteristics:
        Role: {agent.agent_role}
        Task Description: {agent.task_description}
        Resources: {agent.resources}

        The tool being used has the following characteristics:
        Tool Name: {tool.name}
        Tool Parameters: {tool.params}
        Tool Description: {tool.description}
        Tool Parameter Types: {tool.param_type}
        Tool Parameter Descriptions: {tool.param_description}

        The agent will provide you with the error they are encountering, and you must respond exclusively with the following format:
        {"parameter_name": "parameter_input"}"""

        question = f"I received the following error, could you help the agent?\nERROR: {e}"
        # Assuming ai.gptText is a placeholder for interacting with an AI service
        response = ai.gptText(system=system, question=question)
        return response.choices[0].message.content
