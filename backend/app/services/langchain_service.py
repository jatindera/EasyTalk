from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
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
from langchain_postgres import PostgresChatMessageHistory

from app.utils.chat_utils import truncate_history
import os

from langchain.agents import Tool
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    DuckDuckGoSearchAPIWrapper,
)
import logging
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.services import chat_service
from sqlalchemy.orm import Session
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.crud.chat_crud import save_message


logging.basicConfig(level=logging.DEBUG)


# def get_session_history(session_id):
#     return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    print(session_id)
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Set up caching
set_llm_cache(InMemoryCache())
###################CHATOPENAI###################
# llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=200, temperature=0.7)

###################GOOGLE###################
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# def generate_company_names(product_name: str, target_audience: str) -> str:
#     print(product_name, target_audience)

#     prompt_template = PromptTemplate(template=company_name_crafter_template)

#     # Create the LLM chain
#     llm_chain = prompt_template | llm

#     # Invoke the chain with the given topic
#     suggestion = llm_chain.invoke(
#         {"product_name": product_name, "target_audience": target_audience}
#     )
#     return suggestion.content


def general_chat(db: Session, question: str, session_id: str, user_id: str):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an assistant designed to answer user questions",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    stroutput = StrOutputParser()
    chain = prompt | llm | stroutput
    runnable_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history"
    )
    answer = runnable_chain.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    )
    print("*" * 50)
    print(store)
    print("*" * 50)
    # Add the human message to the custom chat manager
    save_message(db, session_id, "human", question, user_id)
    # Add the AI response to the custom chat manager
    save_message(db, session_id, "ai", answer, user_id)

    return answer


def general_chat1(question: str, session_id: str):

    prompt = ChatPromptTemplate(
        [
            ("system", "You are a chatbot having a conversation with a human"),
            ("human", "{question}"),
        ]
    )

    # 1. Wikipedia Tool (for searching Wikipedia)
    api_wrapper = WikipediaAPIWrapper()
    wiki_tool = Tool(
        name="Wikipedia",
        func=api_wrapper.run,
        description="Useful when you need to look up a topic, country or person on Wikipedia",
    )

    # 2. DuckDuckGoSearch Tool (for general web searches)
    duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper()
    duckduckgo_tool = Tool(
        name="DuckDuckGo",
        func=duckduckgo_wrapper.run,
        description="Useful when you need to find information that another tool can't provide.",
    )

    stroutput = StrOutputParser()
    chain = prompt | llm | stroutput
    messages = prompt.format_messages(question=question)

    llm_tool = Tool(
        name="LLM",
        func=chain.invoke,
        description="Useful when you need to generate or interpret text using the LLM.",
    )

    tools = [duckduckgo_tool, llm_tool]
    agent_executor = create_react_agent(llm, tools)

    response = agent_executor.invoke({"messages": [HumanMessage(content=query)]})
    print(response["messages"])
    return {"": ""}
    # return response["messages"]

    # stroutput = StrOutputParser()
    # chain = prompt | llm | stroutput

    # messages = prompt.format_messages(query=query)
    # output = chain.invoke(messages)
    # return output
