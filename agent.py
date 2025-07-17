from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,RunConfig, SQLiteSession
import asyncio
from tools import get_meaning
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)

model =OpenAIChatCompletionsModel(
    model ="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
session = SQLiteSession("user_1","conversation.db")
async def main(user_input:str):
    agent =Agent(
        name = "Dictionary Agent",
        instructions="You are a dictionary agent who provides a word's definition, synonyms, antonyms, part of speech, example sentences, and pronunciation if available.",
        model =model,
        tools=[get_meaning]

    )
    result =  Runner.run_streamed(agent, user_input, run_config=config, session=session)
    return result