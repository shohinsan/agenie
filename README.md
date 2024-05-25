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
