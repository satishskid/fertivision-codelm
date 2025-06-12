"""
FertiVision powered by AI - Model Configuration System

This module provides flexible configuration for choosing between:
- Local models (Ollama, local APIs)
- Cloud APIs (OpenAI, Anthropic, Google, etc.)
- Hybrid configurations

© 2025 FertiVision powered by AI (made by greybrain.ai) - DeepSeek LLM Image Analysis
"""

import os
import json
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List, Any

class ModelProvider(Enum):
    """Available model providers"""
    # Local providers
    OLLAMA_LOCAL = "ollama_local"
    LOCAL_API = "local_api"

    # Free/Affordable APIs
    OPENROUTER = "openrouter"
    GROQ = "groq"
    TOGETHER_AI = "together_ai"
    PERPLEXITY = "perplexity"
    DEEPSEEK = "deepseek"

    # Premium Cloud providers
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE_OPENAI = "azure_openai"

    # Other providers
    HUGGINGFACE = "huggingface"
    REPLICATE = "replicate"
    COHERE = "cohere"

    # Specialized medical APIs
    MEDICAL_API = "medical_api"
    CUSTOM_API = "custom_api"

class AnalysisType(Enum):
    """Types of analysis that can be configured"""
    VISION_ANALYSIS = "vision_analysis"
    TEXT_GENERATION = "text_generation"
    MEDICAL_CLASSIFICATION = "medical_classification"
    SPERM_ANALYSIS = "sperm_analysis"
    EMBRYO_ANALYSIS = "embryo_analysis"
    FOLLICLE_ANALYSIS = "follicle_analysis"
    OOCYTE_ANALYSIS = "oocyte_analysis"
    HYSTEROSCOPY_ANALYSIS = "hysteroscopy_analysis"

@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    provider: ModelProvider
    model_name: str
    api_url: str
    api_key: Optional[str] = None
    timeout: int = 90
    max_tokens: Optional[int] = None
    temperature: float = 0.1
    enabled: bool = True
    cost_per_1k_tokens: float = 0.0
    notes: str = ""

@dataclass
class AnalysisConfig:
    """Configuration for a specific analysis type"""
    analysis_type: AnalysisType
    primary_model: ModelConfig
    fallback_models: List[ModelConfig]
    use_fallback: bool = True
    quality_threshold: float = 0.8
    max_retries: int = 2

class FertiVisionModelManager:
    """Manages model configurations for FertiVision"""
    
    def __init__(self, config_file: str = "fertivision_models.json"):
        self.config_file = config_file
        self.configurations: Dict[AnalysisType, AnalysisConfig] = {}
        self.load_configurations()
    
    def get_default_configurations(self) -> Dict[AnalysisType, AnalysisConfig]:
        """Get default model configurations"""
        
        # Local LLaVA for vision analysis
        llava_local = ModelConfig(
            provider=ModelProvider.OLLAMA_LOCAL,
            model_name="llava:7b",
            api_url="http://localhost:11434/api/generate",
            timeout=90,
            temperature=0.1,
            cost_per_1k_tokens=0.0,
            notes="Local LLaVA model via Ollama"
        )
        
        # OpenRouter - Free tier with multiple models
        openrouter_vision = ModelConfig(
            provider=ModelProvider.OPENROUTER,
            model_name="google/gemini-pro-vision",
            api_url="https://openrouter.ai/api/v1/chat/completions",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            timeout=60,
            max_tokens=4000,
            temperature=0.1,
            cost_per_1k_tokens=0.000375,  # Very affordable
            enabled=bool(os.getenv("OPENROUTER_API_KEY")),
            notes="OpenRouter - Access to multiple models with free tier"
        )

        # Groq - Super fast inference, free tier
        groq_vision = ModelConfig(
            provider=ModelProvider.GROQ,
            model_name="llava-v1.5-7b-4096-preview",
            api_url="https://api.groq.com/openai/v1/chat/completions",
            api_key=os.getenv("GROQ_API_KEY"),
            timeout=30,
            max_tokens=4000,
            temperature=0.1,
            cost_per_1k_tokens=0.0,  # Free tier
            enabled=bool(os.getenv("GROQ_API_KEY")),
            notes="Groq - Ultra-fast inference with generous free tier"
        )

        # Together AI - Affordable open source models
        together_vision = ModelConfig(
            provider=ModelProvider.TOGETHER_AI,
            model_name="meta-llama/Llama-Vision-Free",
            api_url="https://api.together.xyz/v1/chat/completions",
            api_key=os.getenv("TOGETHER_API_KEY"),
            timeout=60,
            max_tokens=4000,
            temperature=0.1,
            cost_per_1k_tokens=0.0002,  # Very cheap
            enabled=bool(os.getenv("TOGETHER_API_KEY")),
            notes="Together AI - Affordable open source models"
        )

        # OpenAI GPT-4 Vision as premium fallback
        gpt4_vision = ModelConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-4-vision-preview",
            api_url="https://api.openai.com/v1/chat/completions",
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=60,
            max_tokens=4000,
            temperature=0.1,
            cost_per_1k_tokens=0.01,
            enabled=bool(os.getenv("OPENAI_API_KEY")),
            notes="OpenAI GPT-4 Vision for premium high-accuracy analysis"
        )
        
        # Google Gemini Vision
        gemini_vision = ModelConfig(
            provider=ModelProvider.GOOGLE,
            model_name="gemini-pro-vision",
            api_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent",
            api_key=os.getenv("GOOGLE_API_KEY"),
            timeout=60,
            temperature=0.1,
            cost_per_1k_tokens=0.0025,
            enabled=bool(os.getenv("GOOGLE_API_KEY")),
            notes="Google Gemini Pro Vision"
        )
        
        # Anthropic Claude for text analysis
        claude_text = ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-sonnet-20240229",
            api_url="https://api.anthropic.com/v1/messages",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            timeout=60,
            max_tokens=4000,
            temperature=0.1,
            cost_per_1k_tokens=0.003,
            enabled=bool(os.getenv("ANTHROPIC_API_KEY")),
            notes="Anthropic Claude for medical text analysis"
        )
        
        # Groq for fast text generation
        groq_text = ModelConfig(
            provider=ModelProvider.GROQ,
            model_name="mixtral-8x7b-32768",
            api_url="https://api.groq.com/openai/v1/chat/completions",
            api_key=os.getenv("GROQ_API_KEY"),
            timeout=30,
            max_tokens=4000,
            temperature=0.1,
            cost_per_1k_tokens=0.0,  # Free tier
            enabled=bool(os.getenv("GROQ_API_KEY")),
            notes="Groq Mixtral - Ultra-fast text generation, free tier"
        )

        # DeepSeek - Very affordable API
        deepseek_text = ModelConfig(
            provider=ModelProvider.DEEPSEEK,
            model_name="deepseek-chat",
            api_url="https://api.deepseek.com/v1/chat/completions",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            timeout=60,
            max_tokens=4000,
            temperature=0.1,
            cost_per_1k_tokens=0.00014,  # Very cheap
            enabled=bool(os.getenv("DEEPSEEK_API_KEY")),
            notes="DeepSeek - Very affordable high-quality text generation"
        )

        # Local Ollama for text generation
        ollama_text = ModelConfig(
            provider=ModelProvider.OLLAMA_LOCAL,
            model_name="llama2:7b",
            api_url="http://localhost:11434/api/generate",
            timeout=60,
            temperature=0.1,
            cost_per_1k_tokens=0.0,
            notes="Local Llama2 via Ollama"
        )
        
        return {
            AnalysisType.VISION_ANALYSIS: AnalysisConfig(
                analysis_type=AnalysisType.VISION_ANALYSIS,
                primary_model=llava_local,
                fallback_models=[groq_vision, openrouter_vision, together_vision, gpt4_vision],
                use_fallback=True,
                quality_threshold=0.8
            ),

            AnalysisType.FOLLICLE_ANALYSIS: AnalysisConfig(
                analysis_type=AnalysisType.FOLLICLE_ANALYSIS,
                primary_model=llava_local,
                fallback_models=[groq_vision, openrouter_vision, gpt4_vision],
                use_fallback=True,
                quality_threshold=0.9  # Higher threshold for medical analysis
            ),
            
            AnalysisType.SPERM_ANALYSIS: AnalysisConfig(
                analysis_type=AnalysisType.SPERM_ANALYSIS,
                primary_model=llava_local,
                fallback_models=[gpt4_vision],
                use_fallback=True,
                quality_threshold=0.85
            ),
            
            AnalysisType.EMBRYO_ANALYSIS: AnalysisConfig(
                analysis_type=AnalysisType.EMBRYO_ANALYSIS,
                primary_model=llava_local,
                fallback_models=[gpt4_vision],
                use_fallback=True,
                quality_threshold=0.9
            ),
            
            AnalysisType.OOCYTE_ANALYSIS: AnalysisConfig(
                analysis_type=AnalysisType.OOCYTE_ANALYSIS,
                primary_model=llava_local,
                fallback_models=[gpt4_vision],
                use_fallback=True,
                quality_threshold=0.85
            ),
            
            AnalysisType.HYSTEROSCOPY_ANALYSIS: AnalysisConfig(
                analysis_type=AnalysisType.HYSTEROSCOPY_ANALYSIS,
                primary_model=llava_local,
                fallback_models=[gpt4_vision],
                use_fallback=True,
                quality_threshold=0.8
            ),
            
            AnalysisType.TEXT_GENERATION: AnalysisConfig(
                analysis_type=AnalysisType.TEXT_GENERATION,
                primary_model=groq_text,  # Start with free Groq
                fallback_models=[deepseek_text, ollama_text, claude_text],
                use_fallback=True,
                quality_threshold=0.7
            ),
            
            AnalysisType.MEDICAL_CLASSIFICATION: AnalysisConfig(
                analysis_type=AnalysisType.MEDICAL_CLASSIFICATION,
                primary_model=claude_text,
                fallback_models=[ollama_text],
                use_fallback=True,
                quality_threshold=0.85
            )
        }
    
    def load_configurations(self):
        """Load configurations from file or create defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                
                # Convert loaded data back to objects
                for analysis_type_str, config_data in data.items():
                    analysis_type = AnalysisType(analysis_type_str)
                    
                    # Convert primary model
                    primary_data = config_data['primary_model']
                    primary_model = ModelConfig(
                        provider=ModelProvider(primary_data['provider']),
                        **{k: v for k, v in primary_data.items() if k != 'provider'}
                    )
                    
                    # Convert fallback models
                    fallback_models = []
                    for fallback_data in config_data['fallback_models']:
                        fallback_model = ModelConfig(
                            provider=ModelProvider(fallback_data['provider']),
                            **{k: v for k, v in fallback_data.items() if k != 'provider'}
                        )
                        fallback_models.append(fallback_model)
                    
                    # Create analysis config
                    analysis_config = AnalysisConfig(
                        analysis_type=analysis_type,
                        primary_model=primary_model,
                        fallback_models=fallback_models,
                        use_fallback=config_data.get('use_fallback', True),
                        quality_threshold=config_data.get('quality_threshold', 0.8),
                        max_retries=config_data.get('max_retries', 2)
                    )
                    
                    self.configurations[analysis_type] = analysis_config
                    
                print(f"✅ Loaded configurations from {self.config_file}")
                
            except Exception as e:
                print(f"❌ Error loading configurations: {e}")
                print("🔄 Using default configurations")
                self.configurations = self.get_default_configurations()
        else:
            print(f"📝 Creating default configurations in {self.config_file}")
            self.configurations = self.get_default_configurations()
            self.save_configurations()
    
    def save_configurations(self):
        """Save configurations to file"""
        try:
            # Convert to serializable format
            data = {}
            for analysis_type, config in self.configurations.items():
                data[analysis_type.value] = {
                    'primary_model': asdict(config.primary_model),
                    'fallback_models': [asdict(model) for model in config.fallback_models],
                    'use_fallback': config.use_fallback,
                    'quality_threshold': config.quality_threshold,
                    'max_retries': config.max_retries
                }
                
                # Convert enums to strings
                data[analysis_type.value]['primary_model']['provider'] = config.primary_model.provider.value
                for fallback_data in data[analysis_type.value]['fallback_models']:
                    fallback_data['provider'] = ModelProvider(fallback_data['provider']).value
            
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"💾 Configurations saved to {self.config_file}")
            
        except Exception as e:
            print(f"❌ Error saving configurations: {e}")
    
    def get_config(self, analysis_type: AnalysisType) -> Optional[AnalysisConfig]:
        """Get configuration for specific analysis type"""
        return self.configurations.get(analysis_type)
    
    def update_config(self, analysis_type: AnalysisType, config: AnalysisConfig):
        """Update configuration for specific analysis type"""
        self.configurations[analysis_type] = config
        self.save_configurations()
    
    def set_primary_model(self, analysis_type: AnalysisType, model_config: ModelConfig):
        """Set primary model for analysis type"""
        if analysis_type in self.configurations:
            self.configurations[analysis_type].primary_model = model_config
            self.save_configurations()
    
    def add_fallback_model(self, analysis_type: AnalysisType, model_config: ModelConfig):
        """Add fallback model for analysis type"""
        if analysis_type in self.configurations:
            self.configurations[analysis_type].fallback_models.append(model_config)
            self.save_configurations()
    
    def list_available_models(self) -> Dict[ModelProvider, List[str]]:
        """List available models by provider"""
        return {
            # Local models
            ModelProvider.OLLAMA_LOCAL: ["llava:7b", "llama2:7b", "codellama:7b", "mistral:7b", "llama3:8b"],

            # Free/Affordable APIs
            ModelProvider.OPENROUTER: [
                "google/gemini-pro-vision", "meta-llama/llama-3-8b-instruct:free",
                "microsoft/wizardlm-2-8x22b", "anthropic/claude-3-haiku"
            ],
            ModelProvider.GROQ: [
                "llava-v1.5-7b-4096-preview", "mixtral-8x7b-32768",
                "llama3-8b-8192", "llama3-70b-8192", "gemma-7b-it"
            ],
            ModelProvider.TOGETHER_AI: [
                "meta-llama/Llama-Vision-Free", "meta-llama/Llama-3-8b-chat-hf",
                "mistralai/Mixtral-8x7B-Instruct-v0.1", "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
            ],
            ModelProvider.DEEPSEEK: ["deepseek-chat", "deepseek-coder"],

            # Premium APIs
            ModelProvider.OPENAI: ["gpt-4-vision-preview", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
            ModelProvider.ANTHROPIC: ["claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-3-opus-20240229"],
            ModelProvider.GOOGLE: ["gemini-pro-vision", "gemini-pro", "gemini-1.5-pro"],

            # Other providers
            ModelProvider.HUGGINGFACE: ["microsoft/DialoGPT-medium", "microsoft/BioGPT-Large"],
            ModelProvider.PERPLEXITY: ["llama-3-sonar-large-32k-online", "llama-3-sonar-small-32k-online"]
        }
    
    def get_cost_estimate(self, analysis_type: AnalysisType, token_count: int) -> float:
        """Estimate cost for analysis"""
        config = self.get_config(analysis_type)
        if config and config.primary_model.cost_per_1k_tokens > 0:
            return (token_count / 1000) * config.primary_model.cost_per_1k_tokens
        return 0.0
    
    def print_configuration_summary(self):
        """Print current configuration summary"""
        print("\n🔧 FertiVision powered by AI - Model Configuration Summary")
        print("=" * 65)
        
        for analysis_type, config in self.configurations.items():
            print(f"\n📊 {analysis_type.value.upper()}:")
            print(f"  Primary: {config.primary_model.provider.value} - {config.primary_model.model_name}")
            print(f"  Enabled: {'✅' if config.primary_model.enabled else '❌'}")
            print(f"  Cost/1K tokens: ${config.primary_model.cost_per_1k_tokens}")
            
            if config.fallback_models:
                print(f"  Fallbacks: {len(config.fallback_models)} models")
                for i, fallback in enumerate(config.fallback_models, 1):
                    status = "✅" if fallback.enabled else "❌"
                    print(f"    {i}. {fallback.provider.value} - {fallback.model_name} {status}")
        
        print("\n" + "=" * 65)
        print("© 2025 FertiVision powered by AI (made by greybrain.ai)")

# Global model manager instance
model_manager = FertiVisionModelManager()
