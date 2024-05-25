import os
import json
from typing_extensions import Annotated
import pprint
from tavily import TavilyClient
from autogen.agentchat import (
    ConversableAgent,
    register_function,
    initiate_chats,
    GroupChat,
    GroupChatManager,
)
from autogen.coding import LocalCommandLineCodeExecutor

# Tavily
# export TAVILY_API_KEY=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
# GROQ
# export GROQ_API_KEY=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

# Define the LLM configuration correctly
config_list = [
    {
        "model": os.environ.get("OPENAI_MODEL_NAME", "llama3-8b-8192"),
        "api_key": os.environ["GROQ_API_KEY"],
        "base_url": os.environ.get("OPENAI_API_BASE", "https://api.groq.com/openai/v1"),
    }
]

# Initialize the Researcher Assistant Agent
researcher_assistant_agent = ConversableAgent(
    name="Researcher_Agent",
    system_message=(
        "You are a research assistant capable of finding detailed answers to users' questions. "
        "You can use search_tool to find raw information on the web and use that information to come up with answers. "
        "If a question is too complex, break it down into smaller search queries. "
        "Try to provide the most accurate and detailed answer possible. "
        "Return 'TERMINATE' to end the conversation."
    ),
    llm_config={"config_list": config_list},
)

# Initialize the Research Tool Agent
researcher_tool_agent = ConversableAgent(
    name="Research_Tool",
    llm_config=False,
    default_auto_reply="Return 'TERMINATE' if you have found the answer. Otherwise, please continue.",
    human_input_mode="NEVER",
)

# Initialize the Tavily client
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


# Define the search tool function
def search_tool(
    query: Annotated[str, "The search query"]
) -> Annotated[str, "The search results"]:
    return tavily.get_search_context(query=query, search_depth="advanced")


# Register the search tool function
register_function(
    search_tool,
    name="search_tool",
    caller=researcher_assistant_agent,
    executor=researcher_tool_agent,
    description="Search for information on the web.",
)


# Define a function to parse the search results
def parse_search_results(results: str) -> str:
    try:
        results_list = json.loads(results)
        formatted_results = []
        for result in results_list:
            url = result.get("url", "No URL")
            content = result.get("content", "No Content")
            formatted_results.append(f"URL: {url}\nContent: {content}")
        return "\n\n".join(formatted_results)
    except json.JSONDecodeError:
        return "Failed to parse search results."


# Register the parsing function
def parse_text(
    text: Annotated[str, "The text to parse"]
) -> Annotated[str, "Parsed text"]:
    return parse_search_results(text)


register_function(
    parse_text,
    name="parse_text",
    caller=researcher_assistant_agent,
    executor=researcher_tool_agent,
    description="Parse the search results.",
)

# Start the chat and ask the question
result = researcher_tool_agent.initiate_chat(
    recipient=researcher_assistant_agent,
    message="What is the address of the building hosting Microsoft Research in Redmond first opened?",
    summary_method="reflection_with_llm",
)

# Print configurations for debugging (optional)
print("=== CONFIG === ")
pprint.pprint(config_list)
print("=== RESULTS === ")
pprint.pprint(result.summary)
