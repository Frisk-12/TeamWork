# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:31:45 2024

Author: andreadesogus
"""

from agents import Agent
from Supervisor import Supervisor
from baseLLM import openaiApis

# Definizione delle caratteristiche del primo agente
agent1_f = {
    'agent_role': 'Senior Translator',
    'backstory': ("You're a seasoned translator, known for an unwavering "
                  "commitment to precision, fluency and contextual "
                  "accuracy, ensuring each translation captures "
                  "the original's true essence."),
    'tools': 'Your knowledge. ',
    'resources': '',
    'task_description': 'Do the best translation you can. ',
    'expected_output': 'A well done translation. '
}

# Creazione dell'istanza del primo agente
agent1 = Agent(agent1_f)

# Definizione delle caratteristiche del secondo agente
agent2_f = {
    'agent_role': 'Senior Quality Check',
    'backstory': ("You're a seasoned translator, known for an unwavering "
                  "commitment to precision, fluency and contextual "
                  "accuracy, ensuring each translation captures "
                  "the original's true essence. You are severe and critical "
                  "but always outcome focused."),
    'tools': 'Your knowledge. ',
    'resources': '',
    'task_description': 'Make quality check on translations and give suggestions for improving. ',
    'expected_output': 'A well done report for improving translations. '
}

# Creazione dell'istanza del secondo agente
agent2 = Agent(agent2_f)

# Inizializzazione dell'API di OpenAI
ai = openaiApis()

# Creazione dell'istanza del supervisore con i due agenti
supervisor = Supervisor([agent1, agent2], ai)

# Testo da tradurre
text = ("Sotto il suo aspetto spaventoso, Draco il drago aiutava i villaggi, "
        "spegneva incendi boschivi con il suo respiro e guidava i viaggiatori smarriti "
        "a casa con i suoi occhi luminosi e gentili.")

# Formulazione della domanda per la traduzione
question = f"Traduci il seguente testo: {text}"

# Esecuzione del processo di supervisione per ottenere la traduzione
response = supervisor.execution(question)

# Stampa della risposta ottenuta
print(response)
