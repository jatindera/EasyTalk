import uuid
from langchain.memory.buffer import ConversationBufferMemory


def truncate_history(history, MAX_HISTORY_LENGTH):
    if len(history) > MAX_HISTORY_LENGTH:
        return history[
            -MAX_HISTORY_LENGTH:
        ]  # Keep only the last `MAX_HISTORY_LENGTH` messages
    return history
