from agents import Agent, Runner
from agentsdk_gemini_adapter import config
import os
from typing import cast
import chainlit as cl
from agents.run import RunConfig

@cl.on_chat_start
async def start():
    cl.user_session.set("chat history", [])
    cl.user_session.set("config", config) 

    agent = Agent(
        name="Assistant",
        instructions="You are a helper assistant Tell the According to their Query",
        
    )

    cl.user_session.set("agent", agent)
    await cl.Message(content="WellCome To Blue-Shark World! Ask Anything You Want.").send()
    
@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()
    
    agent: Agent = cast(Agent, cl.user_session.get("agent" ))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))    
    history = cl.user_session.get("chat history") or []
    history.append({"role": "user", "content": message.content})
    
    try:
        print("\n [CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        

        result = Runner.run_sync(
            starting_agent=agent,
            input=history,
            run_config=config
        )
    
    
        
        response_content = result.final_output
        msg.content = response_content
        await msg.update()
        
        
        cl.user_session.set("chat history", result.to_input_list())
        
        print(f"User: { message.content}")
        print(f"Assistant: {response_content}")
    
        
    except Exception as e:
        msg.content = f"Error : {str(e)}"
        await msg.update()
        print(f"Error: str(e)")
        # print(result.final_output)