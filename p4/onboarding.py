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

config_list = [
    {
        "model": os.environ.get("OPENAI_MODEL_NAME", "llama3-8b-8192"),
        "api_key": os.environ["GROQ_API_KEY"],
        "base_url": os.environ.get("OPENAI_API_BASE", "https://api.groq.com/openai/v1"),
    }
]

agent = ConversableAgent(
    name="chatbot",
    llm_config=config_list,
    human_input_mode="NEVER"
)

reply = agent.generate_reply(
    messages=[{"content": "Tell me a joke.", "role": "user"}]
)
print(reply)

cathy = ConversableAgent(
    name="cathy",
    system_message=
    "Your name is Cathy and you are a stand-up comedian.",
    llm_config=config_list,
    human_input_mode="NEVER",
)

joe = ConversableAgent(
    name="joe",
    system_message=
    "Your name is Joe and you are a stand-up comedian. "
    "Start the next joke from the punchline of the previous joke.",
    llm_config=config_list,
    human_input_mode="NEVER",
)

chat_result = joe.initiate_chat(
    recipient=cathy, 
    message="I'm Joe. Cathy, let's keep the jokes rolling.",
    max_turns=2,
)

import pprint

pprint.pprint(chat_result.chat_history)

pprint.pprint(chat_result.cost)

pprint.pprint(chat_result.summary)

chat_result = joe.initiate_chat(
    cathy, 
    message="I'm Joe. Cathy, let's keep the jokes rolling.", 
    max_turns=2, 
    summary_method="reflection_with_llm",
    summary_prompt="Summarize the conversation",
)

pprint.pprint(chat_result.summary)

cathy = ConversableAgent(
    name="cathy",
    system_message=
    "Your name is Cathy and you are a stand-up comedian. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    llm_config=config_list,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
)

joe = ConversableAgent(
    name="joe",
    system_message=
    "Your name is Joe and you are a stand-up comedian. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    llm_config=config_list,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"] or "Goodbye" in msg["content"],
)

chat_result = joe.initiate_chat(
    recipient=cathy,
    message="I'm Joe. Cathy, let's keep the jokes rolling."
)

cathy.send(message="What's last joke we talked about?", recipient=joe)