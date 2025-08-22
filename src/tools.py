import math
from datetime import datetime, timezone
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def math_eval(expression: str) -> str:
    """Evaluates a simple mathematical expression"""
    allowed_names = {"sqrt": math.sqrt}
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"error: {type(e).__name__}: {e}"


@tool
def time_now() -> str:
    """Returns the datetime in UTC format"""
    return datetime.now(timezone.utc).isoformat()


@tool
def echo(input: str) -> str:
    """Echoes the user input"""
    return input
