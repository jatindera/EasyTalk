from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache  # allows caching the results
from app.prompts.custom_prompts import company_name_crafter_template
from langchain_core.output_parsers import StrOutputParser

# from langchain_core.messages.system import SystemMessage
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory.buffer import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from app.utils.chat_utils import generate_session_id ,truncate_history



# store is a dictionary that maps session IDs to their corresponding chat histories.
# store = {}  # memory is maintained outside the chain
# # A function that returns the chat history for a given session ID.
# def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
#     print("*" * 50)
#     print(store)
#     print("*" * 50)

#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]

# Set up caching
set_llm_cache(InMemoryCache())
llm = ChatOpenAI(model="gpt-4o", max_tokens=200, temperature=0.7)


memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

session_id = generate_session_id()

def get_session_history(session_id):
    sql_chat_message_history = SQLChatMessageHistory(session_id, "sqlite:///memory.db")
    print("*" * 50)
    print(session_id)
    print(sql_chat_message_history)
    print("*" * 50)
    return sql_chat_message_history


def generate_company_names(product_name: str, target_audience: str) -> str:
    print(product_name, target_audience)
    
    prompt_template = PromptTemplate(template=company_name_crafter_template)

    # Create the LLM chain
    llm_chain = prompt_template | llm

    # Invoke the chain with the given topic
    suggestion = llm_chain.invoke(
        {"product_name": product_name, "target_audience": target_audience}
    )
    return suggestion.content


def general_chat(query: str, session_id: str):
    # Get session history
    sql_chat_message_history = get_session_history(session_id)

    # Truncate history if it exceeds the window limit
    # truncated_history = truncate_history(sql_chat_message_history.load())
    truncated_history = sql_chat_message_history # write this logic later.

    # print(f"Truncated History is: {truncate_history}")

    prompt = ChatPromptTemplate(
        [
            ("system", "You are a chatbot having a conversation with a human"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}"),
        ]
    )
    
    stroutput = StrOutputParser()
    chain = prompt | llm | stroutput
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )
    
    output = chain_with_history.invoke(
        {"query": query, "history": truncated_history},
        config={"configurable": {"session_id": session_id}},
    )
    return output



