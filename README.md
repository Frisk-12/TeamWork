# TeamWork
Multi Agent System for Complex Tasks


With the content of all the provided files, here is a comprehensive README for the “TeamWork” repository:

TeamWork

TeamWork is a Multi-Agent System designed to handle complex tasks. This repository contains the implementation of various agents and supervisors required to coordinate and execute tasks effectively.

Table of Contents

	•	Installation
	•	Usage
	•	Modules
	•	Example
	•	License
	•	Contributing
	•	Authors

Installation

To install the necessary dependencies, run:

pip install -r requirements.txt

Usage

You can start the system by running the main supervisor script:

python supervisor.py

Modules

agents.py

Defines the Agent and Team classes.

	•	Agent: Represents an individual agent with specific attributes and capabilities.
	•	Attributes:
	•	agent_role: Role of the agent.
	•	backstory: Background story of the agent.
	•	tools: Tools available to the agent.
	•	resources: Resources available to the agent.
	•	task_description: Description of the task assigned to the agent.
	•	expected_output: Expected output from the agent.
	•	Team: Represents a team of agents.
	•	Methods:
	•	agent_mapping(): Creates a mapping of agent roles to their backstories and task descriptions.

agents_ini.py

Contains the system messages for agents and supervisors.

	•	DefaultAgentSystem: Generates a system message for a given agent.
	•	Methods:
	•	system(agent): Generates a system message for an agent based on their role and task description.
	•	SupervisorSystem: Generates a system message for the AI supervisor.
	•	Methods:
	•	system(): Generates a system message for the AI supervisor to manage and coordinate the team.

base.py

Initializes agents and sets up the supervisor.

	•	Initialization:
	•	Creates instances of Agent with specific attributes.
	•	Initializes the OpenAI API client.
	•	Creates an instance of Supervisor with the agents and OpenAI API client.
	•	Execution:
	•	Provides an example of executing a supervision process to obtain a translation.

baseLLM_wo_key.py

Contains the OpenAI API interactions.

	•	openaiApis: Handles OpenAI API requests.
	•	Methods:
	•	embeddings(text): Retrieves embeddings for the given text.
	•	gptText(system, question, message, _format): Generates a response using the OpenAI API.

supervisor.py

Manages the supervision process of agents.

	•	Supervisor: Manages the supervision of agents using OpenAI’s API.
	•	Methods:
	•	ask_agent(question, agent_role): Asks a specific agent a question based on their role.
	•	add_memory(output): Adds a message to the memory log.
	•	execution(question): Executes the supervision process for the given question.

Example

Here is an example of how to use the system to perform a translation task:

# Define the characteristics of the first agent
agent1_f = {
    'agent_role': 'Senior Translator',
    'backstory': ("You're a seasoned translator, known for an unwavering "
                  "commitment to precision, fluency and contextual accuracy, "
                  "ensuring each translation captures the original's true essence."),
    'tools': 'Your knowledge.',
    'resources': '',
    'task_description': 'Do the best translation you can.',
    'expected_output': 'A well done translation.'
}

# Create the first agent instance
agent1 = Agent(agent1_f)

# Define the characteristics of the second agent
agent2_f = {
    'agent_role': 'Senior Quality Check',
    'backstory': ("You're a seasoned translator, known for an unwavering "
                  "commitment to precision, fluency and contextual accuracy, "
                  "ensuring each translation captures the original's true essence. "
                  "You are severe and critical but always outcome focused."),
    'tools': 'Your knowledge.',
    'resources': '',
    'task_description': 'Make quality check on translations and give suggestions for improving.',
    'expected_output': 'A well done report for improving translations.'
}

# Create the second agent instance
agent2 = Agent(agent2_f)

# Initialize the OpenAI API
ai = openaiApis()

# Create the supervisor instance with the two agents
supervisor = Supervisor([agent1, agent2], ai)

# Text to be translated
text = ("Sotto il suo aspetto spaventoso, Draco il drago aiutava i villaggi, "
        "spegneva incendi boschivi con il suo respiro e guidava i viaggiatori smarriti "
        "a casa con i suoi occhi luminosi e gentili.")

# Formulate the question for translation
question = f"Traduci il seguente testo: {text}"

# Execute the supervision process to obtain the translation
response = supervisor.execution(question)

# Print the obtained response
print(response)

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contributing

Contributions are welcome! Please read the CONTRIBUTING file for guidelines on how to contribute to this project.

Authors

	•	andreadesogus
