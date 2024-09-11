import uuid
from langchain.memory.buffer import ConversationBufferMemory

def generate_session_id():
    return str(uuid.uuid4())

# Usage
session_id = generate_session_id()


def start_new_chat():
    session_id = generate_session_id()
    # Optionally, clear memory here or assign a new memory object
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )
    return session_id, memory


def truncate_history(history, MAX_HISTORY_LENGTH):
    if len(history) > MAX_HISTORY_LENGTH:
        return history[-MAX_HISTORY_LENGTH:]  # Keep only the last `MAX_HISTORY_LENGTH` messages
    return history