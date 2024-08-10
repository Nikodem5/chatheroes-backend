import asyncio
import logging
from typing import List, Dict, AsyncGenerator, Optional, Union
from dotenv import load_dotenv
from anthropic import AsyncAnthropic, APIError
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncAnthropicAssistant:
    def __init__(self, 
                 max_tokens: int = 1024, 
                 temperature: float = 0.2, 
                 system_prompt: str = "You are a helpful assistant.",
                 model: str = "claude-3-5-sonnet-20240620"):
        self.client: Optional[AsyncAnthropic] = None
        self.messages: List[Dict[str, str]] = []
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.model = model

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Clean up resources if needed
        pass

    async def initialize(self):
        try:
            api_key = config.ANTHROPIC_API_KEY
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self.client = AsyncAnthropic(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize AsyncAnthropic client: {e}")
            raise

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    async def get_response(self, stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        if not self.messages or self.messages[-1]["role"] == "assistant":
            raise ValueError("No user message to respond to")

        if not self.client:
            raise RuntimeError("AsyncAnthropic client not initialized. Call initialize() first.")

        try:
            if stream:
                return self._get_streamed_response()
            else:
                return await self._get_non_streamed_response()
        except APIError as e:
            logger.error(f"API error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise

    async def _get_non_streamed_response(self) -> str:
        response = await self.client.messages.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt
        )
        
        assistant_message = response.content[0].text
        self.add_message("assistant", assistant_message)
        return assistant_message

    async def _get_streamed_response(self) -> AsyncGenerator[str, None]:
        full_response = ""
        stream = await self.client.messages.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            stream=True
        )

        async for event in stream:
            if event.type == "content_block_delta" and event.delta.type == "text_delta":
                text = event.delta.text
                full_response += text
                yield text

        self.add_message("assistant", full_response)

    def clear_conversation(self) -> None:
        self.messages.clear()

    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.messages

    def set_system_prompt(self, prompt: str) -> None:
        self.system_prompt = prompt

    def set_model(self, model: str) -> None:
        self.model = model

    async def process_conversation(self, user_input: str) -> str:
        self.add_message("user", user_input)
        response = await self.get_response()
        return response

async def main():
    async with AsyncAnthropicAssistant() as assistant:
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            response = await assistant.process_conversation(user_input)
            print(f"Assistant: {response}")

if __name__ == "__main__":
    asyncio.run(main())