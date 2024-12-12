import unittest
from unittest.mock import patch
from src.config import ModelConfig, AIConfig
from src.llm_factory import create_llm

class TestClaudeSingleton(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.default_claude_config = ModelConfig(
            provider='anthropic',
            model_name='claude-2',
            temperature=0.7,
            max_tokens=1000,
            api_key='test-key'
        )
        self.ai_config = AIConfig(default_model=self.default_claude_config)

    def test_claude_singleton_creation(self):
        """Test that the same config returns the same Claude instance"""
        # Create two instances with the same config
        llm1 = create_llm(self.default_claude_config)
        llm2 = create_llm(self.default_claude_config)

        # They should be the same instance
        self.assertIs(llm1, llm2)

    def test_different_claude_configs(self):
        """Test that different configs create different instances"""
        # Create a different config
        different_claude_config = ModelConfig(
            provider='anthropic',
            model_name='claude-2',
            temperature=0.9,
            max_tokens=1000,
            api_key='test-key'
        )

        llm1 = create_llm(self.default_claude_config)
        llm2 = create_llm(different_claude_config)

        # They should be different instances
        self.assertIsNot(llm1, llm2)

    def test_claude_agent_specific_config(self):
        """Test agent-specific Claude configuration"""
        # Create agent-specific config
        sentiment_claude_config = ModelConfig(
            provider='anthropic',
            model_name='claude-instant-1',
            temperature=0.5,
            max_tokens=1000,
            api_key='test-key'
        )

        ai_config = AIConfig(
            default_model=self.default_claude_config,
            agent_models={'sentiment_agent': sentiment_claude_config}
        )

        # Get models for different agents
        default_model = create_llm(ai_config.get_model_for_agent('default_agent'))
        sentiment_model = create_llm(ai_config.get_model_for_agent('sentiment_agent'))

        # Should be different instances due to different configs
        self.assertIsNot(default_model, sentiment_model)
        self.assertEqual(sentiment_model._model_name, 'claude-instant-1')

    def test_claude_error_handling(self):
        """Test error handling for invalid Claude configurations"""
        # Test invalid model name
        with self.assertRaises(ValueError):
            invalid_config = ModelConfig(
                provider='anthropic',
                model_name='invalid-model',
                temperature=0.7,
                max_tokens=1000,
                api_key='test-key'
            )
            create_llm(invalid_config)

    @patch('src.llm_factory.ChatAnthropic')
    def test_claude_parameters(self, mock_claude):
        """Test that Claude is created with correct parameters"""
        config = ModelConfig(
            provider='anthropic',
            model_name='claude-2',
            temperature=0.8,
            max_tokens=1000,
            api_key='test-key'
        )

        create_llm(config)

        # Verify Claude was created with correct parameters
        mock_claude.assert_called_once_with(
            model='claude-2',
            temperature=0.8,
            max_tokens=1000,
            anthropic_api_key='test-key'
        )

if __name__ == '__main__':
    unittest.main()
