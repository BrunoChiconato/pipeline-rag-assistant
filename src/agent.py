import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from tools import math_eval, time_now, echo


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)
    agent = create_react_agent(model=llm, tools=[math_eval, time_now, echo])
    return agent


if __name__ == "__main__":
    agent = build_agent()
    out = agent.updates(
        {"messages": [{"role": "user", "content": "Repeat exactly: 'LangGraph S1-D2'"}]}
    )
    print(out["messages"][-1].content)
