from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class ModelConfig:
    provider: str  # 'openai', 'anthropic', etc.
    model_name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None

class AIConfig:
    def __init__(self,
                 default_model: ModelConfig,
                 agent_models: Optional[Dict[str, ModelConfig]] = None):
        self.default_model = default_model
        self.agent_models = agent_models or {}

    def get_model_for_agent(self, agent_name: str) -> ModelConfig:
        return self.agent_models.get(agent_name, self.default_model)
