#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 18:53:16 2024

@author: andreadesogus
"""

from agents import Agent
from supervisor_v2 import Supervisor
from baseLLM import openaiApis
from basetool import CustomTool

def info_retriever(filepath: str):
    """
    Reads and returns the contents of a file specified by the given file path.
    
    :param filepath: A file's path
    """
    with open(filepath, 'r') as f:
        file = f.read()
    return file

info_retriever_tool = CustomTool(info_retriever)


def info_downloader(destination_path: str, content: str):
    """
    Writes the given content to a file specified by the destination path.
    
    :param destination_path: The path where the file will be saved.
    :param content: The content to be written to the file.
    """
    with open(destination_path, 'w') as f:
        f.write(content)

info_downloader_tool = CustomTool(info_downloader)

# Definizione delle caratteristiche del primo agente
agent1_f = {
    'agent_role': 'Senior Clause Precence Verifier',
    'backstory': ("You're a veteran legal analyst AI, renowned for your "
                  "meticulous attention to detail and unparalleled accuracy in "
                  "examining contractual documents. Your primary function is to "
                  "identify and verify the presence of fallback clauses related to "
                  "the cessation of benchmark indices, ensuring that every contract "
                  "is thoroughly vetted for compliance and risk mitigation."),
    'tools': [info_retriever_tool],
    'resources': 'Percorso per il file: /Users/andreadesogus/Downloads/contratto.txt',
    'context': [],
    'task_description': 'Verify the precence of a fallback clause following the termination of a benchmark index.',
    'expected_output': 'ONLY the fallback clause '
}

# Creazione dell'istanza del primo agente
agent1 = Agent(agent1_f)

# Definizione delle caratteristiche del secondo agente
agent2_f = {
    'agent_role': 'Senior Clause Robustness Check Analyst',
    'backstory': ("As a Senior Clause Robustness Check Analyst, you are a seasoned expert in the field of contractual analysis. "
                  "Your reputation is built on your ability to scrutinize complex legal documents with an exceptional level of precision. "
                  "Specializing in the verification of fallback clauses for benchmark cessation, you ensure that every contract you review "
                  "adheres to the highest standards of robustness and compliance, safeguarding against potential legal and financial risks."),
    'tools': [info_retriever_tool],
    'resources': '/Users/andreadesogus/Downloads/clausola.txt',
    'context': ['Senior Clause Precence Verifier',],
    'task_description': ("You have to read the guidelines provided in the path. "
                         "Then you should compare the text of this document with "
                         "the fallback clause previously extracted by the other agent. "
                         "Your role is to verify the robustness of the fallback clause "
                         "using the guidelines. "),
    'expected_output': 'A brief and concise report.'
}

# Creazione dell'istanza del secondo agente
agent2 = Agent(agent2_f)

# Definizione delle caratteristiche del terzo agente
agent3_f = {
    'agent_role': 'Senior Reporting Analyst',
    'backstory': ("You are a Senior Reporting Analyst known for your precision and reliability in "
                  "delivering accurate reports. Your main task is to present responses clearly and "
                  "concisely, ensuring all details are correctly conveyed."),
    'tools': [info_downloader_tool],
    'resources': '/Users/andreadesogus/Downloads/report.txt',
    'context': ['Senior Clause Precence Verifier', 'Senior Clause Robustness Check Analyst'],
    'task_description': 'Write the final brief response. Must be very concise. Then download this content using the tool with the specified filepath.',
    'expected_output': 'Only a brief summary with the findings. '
}

# Creazione dell'istanza del secondo agente
agent3 = Agent(agent3_f)

# Inizializzazione dell'API di OpenAI
ai = openaiApis()

# Creazione dell'istanza del supervisore con i due agenti
supervisor = Supervisor([agent1, agent2, agent3], ai)

# Testo da tradurre
text = ("Sotto il suo aspetto spaventoso, Draco il drago aiutava i villaggi, "
        "spegneva incendi boschivi con il suo respiro e guidava i viaggiatori smarriti "
        "a casa con i suoi occhi luminosi e gentili.")

# Formulazione della domanda per la traduzione
question = f"Puoi verificare la presenza e la robustezza della clausola di fallback?"

# Esecuzione del processo di supervisione per ottenere la traduzione
response = supervisor.execution(question)

# Stampa della risposta ottenuta
print(response)




#                 response = ai.gptText(system = ("Sei un programmatore esperto e il tuo obiettivo è "
#                                        "risolvere errori nel codice fornendo esclusivamente "
#                                        "gli elementi necessari per procedere"),
#                                       question = (f"Ho ricevuto il seguente errore: {e}. "
#                                                   "Il codice è il seguente: "
#                                                   "function_response = call_function_dynamically(function_to_call, function_args) "
#                                                   "dove: "
#                                                   "function_to_call = {function_to_call}"
#                                                   "function_args = {function_args}"
#                                                   "Riporta i function_args corretti. ").choices[0].message.content)