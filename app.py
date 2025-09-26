import os
import streamlit as st

from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import PythonREPLTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

MODEL = os.getenv("MODEL", "llama3.2:latest")
SYSTEM = os.getenv(
    "SYSTEM_PROMPT",
    "You are a precise reasoning agent. Explain steps and prefer tool calls over guessing.",
)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

st.set_page_config(page_title="Agent Chat")
st.title("Agent Chat (Streamlit + LangChain + Ollama)")

# Build once per session
if "executor" not in st.session_state:
    llm = ChatOllama(model=MODEL, temperature=0, base_url=OLLAMA_URL)

    tools = [
        PythonREPLTool(),
        DuckDuckGoSearchRun(),
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_react_agent(llm, tools, prompt)
    st.session_state.executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    st.session_state.history = []  # simple display history only

# Render history
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

# Input -> agent -> output
if user_msg := st.chat_input("Ask something"):
    st.session_state.history.append(("user", user_msg))
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.executor.invoke({"input": user_msg})
        st.markdown(result["output"])
    st.session_state.history.append(("assistant", result["output"]))
