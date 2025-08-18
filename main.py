import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
    prompt="You are a helpful assistant",
)

res = agent.invoke(
    {"messages": [{"role": "user", "content": "use your weather tool for SF"}]}
)

last = res["messages"][-1]
print(getattr(last, "content"))
