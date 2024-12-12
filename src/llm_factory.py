from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.config import ModelConfig

_llm_instances = {}

def create_llm(config: ModelConfig):
    cache_key = (config.provider, config.model_name, config.temperature, config.max_tokens, config.api_key)

    if cache_key in _llm_instances:
        return _llm_instances[cache_key]

    if config.provider == 'openai':
        instance = ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            openai_api_key=config.api_key
        )
    elif config.provider == 'anthropic':
        if config.model_name not in ['claude-2', 'claude-instant-1']:
            raise ValueError(f"Invalid Anthropic model name. Must be one of: ['claude-2', 'claude-instant-1']")
        instance = ChatAnthropic(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            anthropic_api_key=config.api_key
        )
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")

    _llm_instances[cache_key] = instance
    return instance
