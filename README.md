# Overview

Agents used to solve prompt engineering problems as well as advanced/complex algorithms current AI using HITL have

HITL(Human In The Loop means you are chatting with ChatGPT or Gemini and controlling Prompt Engineering youself on the fly)

#### Libraries used:

* `pip3 install typing-extensions`
    
* `pip3 install tavily-python` (free basic plan)
    
* `pip3 install pyautogen`

* `pip3 install ollama`

#### Get Started    

Set .ENV variables in your project's terminal

* `export TAVILY_API_KEY=...` from [Tavily](https://tavily.com/)
    
* `export GROQ_API_KEY=...` from [Groq Cloud](https://console.groq.com/keys) for the best performance, note that this is a must have tool in your production as it gets real, real fast.
    

You may use paid LLMs of your choice, such as OpenAI / AWS Bedrock / Gemini , but I used Ollama to host local Meta's Llama3 for exploring AutoGen myself.

* Separately run research agent
* Separately run programming agent
* And then, lastly, run agent manager to see how the other 2 agents can be used to work together


