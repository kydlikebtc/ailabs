from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.config import ModelConfig

def create_llm(config: ModelConfig):
    if config.provider == 'openai':
        return ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            openai_api_key=config.api_key
        )
    elif config.provider == 'anthropic':
        return ChatAnthropic(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            anthropic_api_key=config.api_key
        )
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")
