from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache  # allows caching the results
from app.prompts.custom_prompts import title_prompt
from langchain_core.output_parsers import StrOutputParser


# from langchain_core.messages.system import SystemMessage
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.utils.chat_utils import truncate_history
import os

from langchain.agents import Tool
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    DuckDuckGoSearchAPIWrapper,
)
import logging
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.crud.chat_crud import save_message


# logging.basicConfig(level=logging.DEBUG)


# def get_session_history(session_id):
#     return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

### Statefully manage chat history ###
store = {}


# Set up caching
# set_llm_cache(InMemoryCache())
###################CHATOPENAI###################
# llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=200, temperature=0.7, streaming=True)

###################GOOGLE###################
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest", temperature=0.7, disable_streaming=False
)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def clear_store():
    global store  # Declare that we are using the global 'store'
    store.clear()  # Modify the global dictionary


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        # print(f"Creating new session history for session_id: {session_id}")
        # print(store)
    else:
        print(f"Using existing session history for session_id: {session_id}")
    # print("Current store contents: ", store)  # Check the store content here
    return store[session_id]


def generate_title(question: str) -> str:

    prompt_template = PromptTemplate(template=title_prompt)

    # Create the LLM chain
    llm_chain = prompt_template | llm

    # Invoke the chain with the given topic
    title_suggestion = llm_chain.invoke({"question": question})
    return title_suggestion.content


async def generate_response_astream(
    db: Session, question: str, session_id: str, user_id: str
):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an assistant designed to answer user questions in markdown format.",
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
        history_messages_key="chat_history",
    )
    print("*****************")
    print(store)
    print("*****************")

    async for chunk in runnable_chain.astream(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    ):
        yield chunk
