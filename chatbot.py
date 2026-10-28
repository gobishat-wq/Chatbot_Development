
import csv
from datetime import datetime
from pathlib import Path

import ollama

# Project settings
MODEL_NAME = "llama3.2:1b"
DATASET_DIR = Path(__file__).parent / "dataset"

HISTORY_FILE = DATASET_DIR / "chat_history.csv"
RESPONSES_FILE = DATASET_DIR / "responses.csv"
LOG_FILE = DATASET_DIR / "chatbot_logs.txt"

DATASET_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """
You are EduBot, an educational AI chatbot.
Help students understand programming, Python, databases,
artificial intelligence, and computer science.
Explain concepts clearly with examples.
For coding questions, provide readable code and explanations.
If you are unsure about an answer, say so.
Keep answers helpful and appropriate for students.
"""

# Start a new conversation with system instructions.
conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


def initialize_csv(file_path):
    """Create a CSV file with headers if it does not exist."""
    if not file_path.exists() or file_path.stat().st_size == 0:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["timestamp", "user_question", "bot_response"]
            )


def save_conversation(question, answer):
    """Save one conversation record to both CSV files."""
    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    for file_path in [HISTORY_FILE, RESPONSES_FILE]:
        with open(
            file_path, "a", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, question, answer])

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}]\n")
        file.write(f"User: {question}\n")
        file.write(f"EduBot: {answer}\n")
        file.write("-" * 50 + "\n")


def main():
    initialize_csv(HISTORY_FILE)
    initialize_csv(RESPONSES_FILE)

    print("=" * 50)
    print("       EduBot - Educational AI Chatbot")
    print(f"       Model: {MODEL_NAME}")
    print("Type 'exit' to stop the chatbot.")
    print("=" * 50)

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChatbot stopped.")
            break

        if question.lower() == "exit":
            print("Thank you for using EduBot!")
            break

        if not question:
            print("Please enter a question.")
            continue

        # Add the new question to the conversation.
        conversation_history.append(
            {"role": "user", "content": question}
        )

        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=conversation_history,
            )

            answer = response.message.content.strip()

            # Keep the answer in history for future context.
            conversation_history.append(
                {"role": "assistant", "content": answer}
            )

            print(f"\nEduBot: {answer}")
            save_conversation(question, answer)
            print("[Conversation saved]")

        except ollama.ResponseError as error:
            # Remove the unanswered question from history.
            conversation_history.pop()
            print(f"Ollama error: {error}")
            print("Check the model name and Ollama installation.")

        except Exception as error:
            conversation_history.pop()
            print(f"Connection or runtime error: {error}")
            print("Check that Ollama is running and try again.")


if __name__ == "__main__":
    main()
