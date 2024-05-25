import os
from autogen.agentchat import ConversableAgent, GroupChat, GroupChatManager
from typing import List
import pprint

# Define the LLM configuration correctly
config_list = [
    {
        "model": os.environ.get("OPENAI_MODEL_NAME", "llama3-8b-8192"),
        "api_key": os.environ.get("GROQ_API_KEY", ""),
        "base_url": os.environ.get("OPENAI_API_BASE", "https://api.groq.com/openai/v1")
    }
]

# Create agents with appropriate configurations
admin_agent = ConversableAgent(
    name="Admin",
    llm_config=False,
    human_input_mode="ALWAYS",
    description="Admin for the group chat."
)

planner_agent = ConversableAgent(
    name="Planner",
    llm_config={"config_list": config_list},
    system_message="""You are a planner for complex tasks.
    You come up with a plan and assign subtasks to different agents.
    You also check for the completion of the tasks and provide feedback to the agents.
    When the task is completed, return 'TERMINATE' to end the conversation.
    """,
    description="Planner, called before and after each subtask to provide specific guidance."
)

researcher_assistant_agent = ConversableAgent(
    name="ResearcherAssistant",
    llm_config={"config_list": config_list},
    description="Researcher, finding detailed answers to user's questions."
)

programmer_assistant_agent = ConversableAgent(
    name="ProgrammerAssistant",
    llm_config={"config_list": config_list},
    description="Programmer, writing code given data and requirements."
)

programmer_executor_agent = ConversableAgent(
    name="ProgrammerExecutor",
    llm_config={"config_list": config_list},
    description="Code executor, called after programmer suggested."
)

# Create a group chat instance with appropriate agents
group_chat = GroupChat(
    messages=[],
    agents=[admin_agent, planner_agent, researcher_assistant_agent, programmer_assistant_agent, programmer_executor_agent],
    admin_name="Admin",
    speaker_transitions_type="allowed",
    send_introductions=True,
    allowed_or_disallowed_speaker_transitions={
        admin_agent: [planner_agent],
        planner_agent: [planner_agent, researcher_assistant_agent, programmer_assistant_agent],
        researcher_assistant_agent: [planner_agent, researcher_assistant_agent, programmer_assistant_agent],
        programmer_assistant_agent: [planner_agent, researcher_assistant_agent, programmer_assistant_agent],
        programmer_executor_agent: [planner_agent, programmer_executor_agent]
    },
    max_round=100
)

# Create a group chat manager instance
group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": config_list}
)

result = admin_agent.initiate_chat(
    recipient=group_chat_manager,
    message="Find the top 5 countries GDP per captia, create a plot save to a file.",
)

# Print configurations for debugging (optional)
print("=== CONFIG === ")
pprint.pprint(config_list)

print("=== RESULTS === ")
pprint.pprint(result.summary)