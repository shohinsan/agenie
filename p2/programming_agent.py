import os
import json
from typing_extensions import Annotated
import pprint
from autogen.agentchat import (
    ConversableAgent,
    register_function,
    initiate_chats,
    GroupChat,
    GroupChatManager,
)
from autogen.coding import LocalCommandLineCodeExecutor

# Define the LLM configuration correctly
config_list = [
    {
        "model": os.environ.get("OPENAI_MODEL_NAME", "llama3-8b-8192"),
        "api_key": os.environ["GROQ_API_KEY"],
        "base_url": os.environ.get("OPENAI_API_BASE", "https://api.groq.com/openai/v1"),
    }
]

# Initialize the Programming Assistant Agent
programming_assistant_agent = ConversableAgent(
    name="Programming_Assistant",
    system_message="""
    You are a programming assistant. You can solve tasks using your coding skills.
    Write your code script in Markdown format. For example:
    ```python
    print("Hello, World!")
    ```
    Your code will be executed in the order it is written.
    If a code block fails to execute, try to fix the error and write the code block again.
    Once all code blocks are successfully executed, return 'TERMINATE' to end the conversation.
    """,
    llm_config={"config_list": config_list},
)

code_executor = LocalCommandLineCodeExecutor(work_dir=".coding")

programmer_executor_agent = ConversableAgent(
    name="Programmer_Executor",
    llm_config=False,
    code_execution_config={"executor": code_executor},
    default_auto_reply="Return 'TERMINATE' code blocks are successfully executed. Otherwise, please continue.",
    human_input_mode="NEVER",
)

result = programmer_executor_agent.initiate_chat(
    recipient=programming_assistant_agent,
    message="There are some rabbits and chickens in a barn. There are 532 legs and 170 heads. How many rabbits and chickens are there?",
    summary_method="reflection_with_llm",
)

# Print configurations for debugging (optional)
print("=== CONFIG === ")
pprint.pprint(config_list)

print("=== RESULTS === ")
pprint.pprint(result.summary)
