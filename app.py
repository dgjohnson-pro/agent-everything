# app.py
import os
import streamlit as st

from langchain_ollama.chat_models import ChatOllama 
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools import DuckDuckGoSearchRun

MODEL = os.getenv("MODEL", "llama3.2:latest")
SYSTEM = os.getenv(
    "SYSTEM_PROMPT",
    "You are a precise reasoning agent. Explain steps and prefer tool calls over guessing.",
)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

st.set_page_config(page_title="Agent Chat")
st.title("Agent Chat (Streamlit + LangChain v1 + Ollama)")

def build_agent():
    llm = ChatOllama(model=MODEL, temperature=0, base_url=OLLAMA_URL)
    tools = [PythonREPLTool(), DuckDuckGoSearchRun()]
    # In v1, prompt can be a plain system string or SystemMessage
    agent = create_agent(model=llm, tools=tools, prompt=SYSTEM)
    return agent

if "agent" not in st.session_state:
    st.session_state.agent = build_agent()
    st.session_state.messages = [SystemMessage(content=SYSTEM)]  # full chat state

# Render history
for m in st.session_state.messages:
    if isinstance(m, HumanMessage):
        with st.chat_message("user"):
            st.markdown(m.content)
    elif isinstance(m, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(m.content)

# Input -> agent -> output
if user_msg := st.chat_input("Ask something"):
    st.session_state.messages.append(HumanMessage(content=user_msg))
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # v1 agents expect the running conversation in `messages`
                result = st.session_state.agent.invoke({"messages": st.session_state.messages})
                # result["messages"] is the updated transcript including tool calls
                new_messages = result["messages"]
                # Append only the new AI turn(s); last item should be AIMessage
                ai_out = next((m for m in reversed(new_messages) if isinstance(m, AIMessage)), None)
                if ai_out is None:
                    st.error("No assistant message returned.")
                else:
                    st.markdown(ai_out.content)
                    st.session_state.messages = new_messages  # keep full state
            except Exception as e:
                st.error(f"Run failed: {e}")
