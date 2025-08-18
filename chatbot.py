from agents import Agent, Runner
from agentsdk_gemini_adapter import config


agent = Agent(
    name="Assistant",
    instructions="You are a helper assistant Tell the According to their Query",
    
)


result = Runner.run_sync(
    agent,
    "What is Love",
    run_config=config
)
print(result.final_output)