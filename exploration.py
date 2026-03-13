import pydantic_ai
import os
import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from dotenv import load_dotenv

load_dotenv()

class AssistantResponse(BaseModel):
    answer: str
    confidence: float

# 1. Your Key
MY_KEY = os.getenv("ANTHROPIC_API_KEY")
provider = AnthropicProvider(api_key=MY_KEY)
model = AnthropicModel('claude-sonnet-4-6', provider=provider)

# 2. Update result_type -> output_type
# In 2026, PydanticAI uses output_type for the generic response schema.
agent = Agent(model, output_type=AssistantResponse)

async def main():
    try:
        result = await agent.run("what is two times 100?")
        print(f"Success! Response: {result.output}")
        print(f"Confidence: {result.output.confidence}")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

