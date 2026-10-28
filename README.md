
# Week 9 – Chatbot Development using Ollama

## Project Overview
EduBot is a command-line educational AI chatbot developed
using Python and a locally running Ollama language model.

## Objectives
- Build an interactive chatbot.
- Maintain conversation history.
- Save timestamped conversations in CSV files.
- Prepare the project for future LangChain integration.

## Technologies Used
- Python
- Ollama
- Llama 3.2 1B
- Pandas
- Jupyter Notebook
- Visual Studio Code

## Installation
1. Install Python and Ollama.
2. Download the model:
   ollama pull llama3.2:1b
3. Install dependencies:
   pip install -r requirements.txt

## Execution
Run the chatbot from the project root:
python chatbot.py

Type exit to stop the program.

## Output Files
- dataset/chat_history.csv
- dataset/sample_questions.csv
- dataset/chatbot_logs.txt
- dataset/responses.csv

## Limitations
Responses may be inaccurate, and generation speed depends
on the available hardware. Conversation context is maintained
during the current session.

## Future Enhancement
Integrate LangChain to manage prompts, conversation memory,
and additional LLM workflows.
