from openai import AsyncAzureOpenAI
from flask import current_app
from typing import List, Dict, Optional

class AzureOpenAI(object):
    _api_key: str
    _azure_endpoint: str
    _api_version: str
    _deployment_name: str
    _client: AsyncAzureOpenAI | None
    def __init__(self):
        self._api_key = current_app.config["AZURE_OPENAI_API_KEY"] 
        self._azure_endpoint = current_app.config["AZURE_OPENAI_ENDPOINT"] 
        self._api_version = current_app.config["AZURE_OPENAI_API_VERSION"] 
        self._deployment_name = current_app.config["AZURE_OPENAI_DEPLOYMENT_NAME"] 
        self._client = None # Initialize client to None

    async def _connect(self):
        if not all([self._api_key, self._azure_endpoint, self._api_version, self._deployment_name]):
            raise ValueError("Azure OpenAI credentials or deployment name are not set in environment variables.")
        try:
            self._client = AsyncAzureOpenAI(
                api_key=self._api_key,
                api_version=self._api_version,
                azure_endpoint=self._azure_endpoint
            ) 
            
            return self._client
        except Exception as e:
            print(f"Error connecting to Azure OpenAI: {e}")
            raise
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 150,
        stream: bool = False,
        **kwargs
    ) -> str:
        """
        Perform a chat completion using Azure OpenAI.
        :param messages: List of messages in OpenAI chat format.
        :param temperature: Sampling temperature.
        :param max_tokens: Maximum number of tokens to generate.
        :param stream: Whether to stream the response.
        :param kwargs: Additional parameters for OpenAI API.
        :return: Response text or streamed chunks.
        """
        client = await self.get_client()
        response = await client.chat.completions.create(
            model=self._deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            **kwargs
        )
        if stream:
            # Return generator for streamed response
            async def stream_text():
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return stream_text()
        return response.choices[0].message.content.strip()

    async def get_client(self):
        if self._client is None:
            await self._connect() # Await the async connection method 
            
        return self._client
    
    