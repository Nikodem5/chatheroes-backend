import asyncio
from typing import AsyncGenerator
from assistant import AsyncAnthropicAssistant

class MultistepPrompting:
    def __init__(self, 
                 teacher_system_prompt: str = "You are a knowledgeable teacher. Provide clear and concise explanations.",
                 character_system_prompt: str = "You are a friendly character. Respond in a casual and engaging manner.",
                 max_tokens: int = 1024,
                 temperature: float = 0.2,
                 model: str = "claude-3-5-sonnet-20240620"):
        self.teacher = AsyncAnthropicAssistant(
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=teacher_system_prompt,
            model=model
        )
        self.character = AsyncAnthropicAssistant(
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=character_system_prompt,
            model=model
        )
        

    async def initialize(self):
        await asyncio.gather(
            self.teacher.initialize(),
            self.character.initialize()
        )

    async def run(self, user_message: str) -> str:
        # Step 1: Get teacher's response
        self.teacher.add_message("user", user_message)
        teacher_response = await self.teacher.get_response()

        # Step 2: Get character's response based on teacher's response
        self.character.add_message("user", teacher_response)
        character_response = await self.character.get_response()

        return character_response

    async def run_stream(self, user_message: str) -> AsyncGenerator[str, None]:
        # Step 1: Get teacher's response
        self.teacher.add_message("user", user_message)
        teacher_response = await self.teacher.get_response()

        # Step 2: Get character's response based on teacher's response
        self.character.add_message("user", teacher_response)
        async for chunk in await self.character.get_response(stream=True):
            yield chunk

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Clean up resources if needed
        pass

async def main():
    async with MultistepPrompting() as multistep:
        # Example usage of run method
        response = await multistep.run("What is the capital of France?")
        print("Non-streamed response:", response)

        # Example usage of run_stream method
        print("\nStreamed response:")
        async for chunk in multistep.run_stream("Tell me about the solar system."):
            print(chunk, end='', flush=True)

if __name__ == "__main__":
    asyncio.run(main())