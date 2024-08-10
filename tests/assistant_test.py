import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from bots.assistant import AsyncAnthropicAssistant

async def main():
    async with AsyncAnthropicAssistant as assistant:
        while True:
            user_input =  input("You: ")
            if user_input.lower() == 'exit':
                break
            response = await assistant.process_conversation(user_input)
            print(f"Assistant: {response}")

if __name__ == "__main__":
    asyncio.run(main())