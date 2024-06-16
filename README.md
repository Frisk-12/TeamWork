\# TeamWork
Multi Agent System for Complex Tasks

## Overview
This project implements a multi-agent system for managing complex tasks and processes. The system is designed to leverage the strengths of different specialized agents to perform and supervise a variety of tasks efficiently. Each agent has a specific role and expertise, and a supervising agent coordinates the overall workflow.

## Features
- **Task Delegation**: The supervisor agent delegates tasks to specialized agents based on their roles and expertise.
- **Collaboration**: Agents collaborate to complete tasks, ensuring high-quality outputs through a structured workflow.
- **Customization**: Easily define new agents with specific roles, backstories, tools, resources, and task descriptions.
- **Scalability**: The system can handle multiple agents and tasks, making it suitable for complex and large-scale operations.

## Installation
1. **Clone the repository**:
    ```sh
    git clone https://github.com/Frisk-12/multi-agent-task-management.git
    cd multi-agent-task-management
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. **Define the agents**:
    Define the features for each agent, including their role, backstory, tools, resources, task description, and expected output.

2. **Create agent instances**:
    Create instances of the `Agent` class using the defined features.

3. **Initialize the OpenAI API**:
    Initialize the `openaiApis` class with your API key.

4. **Create a supervisor instance**:
    Create an instance of the `Supervisor` class, passing in the list of agents and the OpenAI API instance.

5. **Execute a task**:
    Formulate a question or task for the system and use the `supervisor.execution` method to get the response.

    Example:
    ```python
    from agents import Agent
    from Supervisor import Supervisor
    from baseLLM import openaiApis

    # Define agents
    agent1_f = {
        'agent_role': 'Senior Translator',
        'backstory': "Experienced translator with expertise in contextual accuracy.",
        'tools': 'Your knowledge.',
        'resources': '',
        'task_description': 'Translate text accurately.',
        'expected_output': 'A high-quality translation.'
    }

    agent1 = Agent(agent1_f)

    agent2_f = {
        'agent_role': 'Senior Quality Check',
        'backstory': "Expert in ensuring translation quality and providing improvement suggestions.",
        'tools': 'Your knowledge.',
        'resources': '',
        'task_description': 'Review translations and suggest improvements.',
        'expected_output': 'A detailed quality report.'
    }

    agent2 = Agent(agent2_f)

    # Initialize OpenAI API
    ai = openaiApis()

    # Create supervisor instance
    supervisor = Supervisor([agent1, agent2], ai)

    # Define a task for the system
    text = ("Sotto il suo aspetto spaventoso, Draco il drago aiutava i villaggi, "
            "spegneva incendi boschivi con il suo respiro e guidava i viaggiatori smarriti "
            "a casa con i suoi occhi luminosi e gentili.")
    question = f"Translate the following text: {text}"

    # Execute the task
    response = supervisor.execution(question)
    print(response)
    ```

## Project Structure
multi-agent-task-management
├── agents.py # Defines the Agent and Team classes
├── baseLLM.py # Implements the openaiApis class for API interaction
├── supervisor.py # Implements the Supervisor class for task coordination
├── main.py # Main script to set up agents and execute tasks
├── requirements.txt # List of dependencies
└── README.md # This README file



## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, feel free to open an issue or contact the author at andesogus@gmail.com.



