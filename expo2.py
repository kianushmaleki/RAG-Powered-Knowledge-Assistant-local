import pydantic_ai
import os
import pathlib
import asyncio
import anthropic
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from dotenv import load_dotenv
from transformers import pipeline

from schema import AssistantResponse



load_dotenv()
MY_KEY = os.getenv("ANTHROPIC_API_KEY")
provider = AnthropicProvider(api_key=MY_KEY)
model = AnthropicModel('claude-sonnet-4-6', provider=provider)


agent = Agent(model
              , model_settings={"temperature": 0.8}
              , output_type=AssistantResponse)

async def main():
    try:
        result = await agent.run("Hello, this is a test run?")
        print(f"Success! Response: {result.output.answer}")
        print(f"Confidence: {result.output.confidence}")
        
    except Exception as e:
        print(f"Error occurred: {e}")




print('-'*50)
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

com = client.messages.create(
    model="claude-sonnet-4-6",
    system="Complete the sentence",
    max_tokens=1024,
    temperature=0.8,
    messages=[
        {
            "role": "user",
            "content": [
               {
                  "type": "text",
                  "text": "An electron walks into a bar."
               }
            ]
        }
    ]
)   

print(com.content[0].text)




print('-'*50)



if __name__ == "__main__":
    asyncio.run(main())