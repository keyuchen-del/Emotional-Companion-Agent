from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from server.config import settings

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
    return _client


async def stream_chat(messages: list[dict]) -> AsyncGenerator[str, None]:
    client = get_client()
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        stream=True,
        temperature=0.85,
        max_tokens=1024,
    )
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content


async def chat(messages: list[dict]) -> str:
    client = get_client()
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )
    return response.choices[0].message.content or ""


async def get_embedding(text: str) -> list[float] | None:
    try:
        client = get_client()
        response = await client.embeddings.create(
            model=settings.embedding_model,
            input=text,
        )
        return response.data[0].embedding
    except Exception:
        return None
