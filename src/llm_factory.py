from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.config import ModelConfig

_llm_instances = {}

VALID_CLAUDE_MODELS = [
    'claude-3-5-sonnet-latest',
    'claude-3-5-sonnet-20241022',
    'claude-3-5-haiku-latest',
    'claude-3-5-haiku-20241022',
    'claude-3-opus-20240229',
    'claude-3-sonnet-20240229',
    'claude-3-haiku-20240307'
]

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
        if config.model_name not in VALID_CLAUDE_MODELS:
            raise ValueError(f"Invalid Anthropic model name. Must be one of: {VALID_CLAUDE_MODELS}")

        if 'claude-3-5' in config.model_name:
            max_tokens = min(config.max_tokens, 8192)
        else:
            max_tokens = min(config.max_tokens, 4096)

        instance = ChatAnthropic(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=max_tokens,
            anthropic_api_key=config.api_key
        )
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")

    _llm_instances[cache_key] = instance
    return instance
