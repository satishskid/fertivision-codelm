#!/usr/bin/env python3
"""
FertiVision powered by AI - Model Configuration Manager

Interactive CLI for managing model configurations and API settings.

© 2025 FertiVision powered by AI (made by greybrain.ai) - DeepSeek LLM Image Analysis
"""

import os
import json
from typing import Dict, List, Optional
from model_config import (
    ModelProvider, AnalysisType, ModelConfig, AnalysisConfig,
    model_manager
)
from model_service import service_manager

class ModelConfigManager:
    """Interactive manager for model configurations"""
    
    def __init__(self):
        self.manager = model_manager
    
    def run_interactive_setup(self):
        """Run interactive configuration setup"""
        print("🔧 FertiVision powered by AI - Model Configuration")
        print("=" * 65)
        print("Configure your DeepSeek LLM and API settings for optimal performance")
        print("© 2025 FertiVision powered by AI (made by greybrain.ai)")
        print("=" * 65)
        
        while True:
            print("\n📋 Configuration Options:")
            print("1. 📊 View current configuration")
            print("2. 🔧 Configure API keys")
            print("3. 🎯 Set primary models for analysis types")
            print("4. 🔄 Configure fallback models")
            print("5. 🧪 Test model connections")
            print("6. 💰 View cost estimates")
            print("7. 📁 Import/Export configurations")
            print("8. 🔄 Reset to defaults")
            print("9. ❌ Exit")
            
            try:
                choice = input("\nSelect an option (1-9): ").strip()
                
                if choice == "1":
                    self.view_configuration()
                elif choice == "2":
                    self.configure_api_keys()
                elif choice == "3":
                    self.configure_primary_models()
                elif choice == "4":
                    self.configure_fallback_models()
                elif choice == "5":
                    self.test_model_connections()
                elif choice == "6":
                    self.view_cost_estimates()
                elif choice == "7":
                    self.import_export_config()
                elif choice == "8":
                    self.reset_to_defaults()
                elif choice == "9":
                    print("\n👋 Configuration saved! Thank you for using FertiVision powered by AI.")
                    break
                else:
                    print("❌ Invalid option. Please select 1-9.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Configuration saved! Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def view_configuration(self):
        """Display current configuration"""
        print("\n📊 Current Model Configuration")
        print("-" * 50)
        
        self.manager.print_configuration_summary()
        
        # Show API key status
        print("\n🔑 API Key Status:")
        api_keys = {
            "OpenAI": os.getenv("OPENAI_API_KEY"),
            "Anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "Google": os.getenv("GOOGLE_API_KEY"),
            "Azure": os.getenv("AZURE_OPENAI_API_KEY")
        }
        
        for provider, key in api_keys.items():
            status = "✅ Configured" if key else "❌ Not set"
            print(f"  {provider}: {status}")
    
    def configure_api_keys(self):
        """Configure API keys"""
        print("\n🔑 API Key Configuration")
        print("-" * 30)
        print("Note: API keys are stored as environment variables")
        print("You can set them in your .env file or system environment")
        
        api_providers = {
            "1": ("OpenRouter (Free Tier)", "OPENROUTER_API_KEY", "sk-or-..."),
            "2": ("Groq (Free Tier)", "GROQ_API_KEY", "gsk_..."),
            "3": ("Together AI", "TOGETHER_API_KEY", "..."),
            "4": ("DeepSeek (Cheap)", "DEEPSEEK_API_KEY", "sk-..."),
            "5": ("OpenAI", "OPENAI_API_KEY", "sk-..."),
            "6": ("Anthropic", "ANTHROPIC_API_KEY", "sk-ant-..."),
            "7": ("Google", "GOOGLE_API_KEY", "AIza..."),
            "8": ("Azure OpenAI", "AZURE_OPENAI_API_KEY", "...")
        }
        
        print("\nAvailable providers:")
        for key, (name, env_var, example) in api_providers.items():
            current = os.getenv(env_var)
            status = "✅" if current else "❌"
            print(f"{key}. {name} ({env_var}) {status}")
        
        choice = input("\nSelect provider to configure (1-8) or Enter to skip: ").strip()
        
        if choice in api_providers:
            name, env_var, example = api_providers[choice]
            print(f"\nConfiguring {name}")
            print(f"Environment variable: {env_var}")
            print(f"Example format: {example}")
            
            current = os.getenv(env_var)
            if current:
                print(f"Current value: {current[:10]}...")
            
            new_key = input("Enter new API key (or Enter to keep current): ").strip()
            
            if new_key:
                print(f"\n💡 To set this permanently, add to your .env file:")
                print(f"   {env_var}={new_key}")
                print(f"\nOr set as environment variable:")
                print(f"   export {env_var}={new_key}")
                
                # Temporarily set for this session
                os.environ[env_var] = new_key
                print("✅ API key set for this session")
    
    def configure_primary_models(self):
        """Configure primary models for each analysis type"""
        print("\n🎯 Primary Model Configuration")
        print("-" * 35)
        
        analysis_types = list(AnalysisType)
        
        print("Analysis types:")
        for i, analysis_type in enumerate(analysis_types, 1):
            config = self.manager.get_config(analysis_type)
            current_model = config.primary_model.model_name if config else "Not configured"
            print(f"{i}. {analysis_type.value}: {current_model}")
        
        choice = input(f"\nSelect analysis type to configure (1-{len(analysis_types)}) or Enter to skip: ").strip()
        
        try:
            if choice and 1 <= int(choice) <= len(analysis_types):
                analysis_type = analysis_types[int(choice) - 1]
                self.configure_model_for_analysis(analysis_type)
        except ValueError:
            print("❌ Invalid selection")
    
    def configure_model_for_analysis(self, analysis_type: AnalysisType):
        """Configure model for specific analysis type"""
        print(f"\n🔧 Configuring {analysis_type.value}")
        
        # Show available providers
        providers = list(ModelProvider)
        print("\nAvailable providers:")
        for i, provider in enumerate(providers, 1):
            print(f"{i}. {provider.value}")
        
        provider_choice = input(f"Select provider (1-{len(providers)}): ").strip()
        
        try:
            provider = providers[int(provider_choice) - 1]
            
            # Show available models for provider
            available_models = self.manager.list_available_models().get(provider, [])
            if available_models:
                print(f"\nAvailable models for {provider.value}:")
                for i, model in enumerate(available_models, 1):
                    print(f"{i}. {model}")
                
                model_choice = input(f"Select model (1-{len(available_models)}) or enter custom: ").strip()
                
                if model_choice.isdigit() and 1 <= int(model_choice) <= len(available_models):
                    model_name = available_models[int(model_choice) - 1]
                else:
                    model_name = input("Enter custom model name: ").strip()
            else:
                model_name = input("Enter model name: ").strip()
            
            # Get API URL
            if provider == ModelProvider.OLLAMA_LOCAL:
                api_url = "http://localhost:11434/api/generate"
            elif provider == ModelProvider.OPENAI:
                api_url = "https://api.openai.com/v1/chat/completions"
            elif provider == ModelProvider.ANTHROPIC:
                api_url = "https://api.anthropic.com/v1/messages"
            elif provider == ModelProvider.GOOGLE:
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
            else:
                api_url = input("Enter API URL: ").strip()
            
            # Create model config
            model_config = ModelConfig(
                provider=provider,
                model_name=model_name,
                api_url=api_url,
                api_key=self.get_api_key_for_provider(provider),
                enabled=True
            )
            
            # Update configuration
            self.manager.set_primary_model(analysis_type, model_config)
            print(f"✅ Primary model for {analysis_type.value} set to {provider.value}/{model_name}")
            
        except (ValueError, IndexError):
            print("❌ Invalid selection")
    
    def get_api_key_for_provider(self, provider: ModelProvider) -> Optional[str]:
        """Get API key for provider"""
        key_mapping = {
            ModelProvider.OPENROUTER: "OPENROUTER_API_KEY",
            ModelProvider.GROQ: "GROQ_API_KEY",
            ModelProvider.TOGETHER_AI: "TOGETHER_API_KEY",
            ModelProvider.DEEPSEEK: "DEEPSEEK_API_KEY",
            ModelProvider.OPENAI: "OPENAI_API_KEY",
            ModelProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            ModelProvider.GOOGLE: "GOOGLE_API_KEY",
            ModelProvider.AZURE_OPENAI: "AZURE_OPENAI_API_KEY",
            ModelProvider.PERPLEXITY: "PERPLEXITY_API_KEY"
        }

        env_var = key_mapping.get(provider)
        return os.getenv(env_var) if env_var else None
    
    def test_model_connections(self):
        """Test connections to configured models"""
        print("\n🧪 Testing Model Connections")
        print("-" * 30)
        
        test_prompt = "Hello, this is a connection test."
        
        for analysis_type, config in self.manager.configurations.items():
            print(f"\n📊 Testing {analysis_type.value}:")
            print(f"  Primary: {config.primary_model.provider.value}/{config.primary_model.model_name}")
            
            if not config.primary_model.enabled:
                print("  ⏭️  Skipped (disabled)")
                continue
            
            try:
                response = service_manager._call_model(
                    config.primary_model,
                    test_prompt
                )
                
                if response.success:
                    print(f"  ✅ Success ({response.processing_time:.2f}s)")
                else:
                    print(f"  ❌ Failed: {response.error}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
    
    def view_cost_estimates(self):
        """View cost estimates for different models"""
        print("\n💰 Cost Estimates (per 1K tokens)")
        print("-" * 35)
        
        for analysis_type, config in self.manager.configurations.items():
            cost = config.primary_model.cost_per_1k_tokens
            if cost > 0:
                print(f"{analysis_type.value}: ${cost:.4f}")
            else:
                print(f"{analysis_type.value}: Free (local)")
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        confirm = input("\n⚠️  Reset all configurations to defaults? (y/N): ").strip().lower()
        
        if confirm == 'y':
            self.manager.configurations = self.manager.get_default_configurations()
            self.manager.save_configurations()
            print("✅ Configuration reset to defaults")
        else:
            print("❌ Reset cancelled")
    
    def import_export_config(self):
        """Import or export configuration"""
        print("\n📁 Import/Export Configuration")
        print("1. Export current configuration")
        print("2. Import configuration from file")
        
        choice = input("Select option (1-2): ").strip()
        
        if choice == "1":
            filename = input("Export filename (default: fertivision_config_export.json): ").strip()
            if not filename:
                filename = "fertivision_config_export.json"
            
            try:
                # Export current config
                with open(filename, 'w') as f:
                    json.dump({
                        "export_info": {
                            "version": "1.0",
                            "description": "FertiVision Model Configuration Export"
                        },
                        "configurations": self.manager.configurations
                    }, f, indent=2, default=str)
                
                print(f"✅ Configuration exported to {filename}")
            except Exception as e:
                print(f"❌ Export failed: {e}")
        
        elif choice == "2":
            filename = input("Import filename: ").strip()
            
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                    
                    print(f"✅ Configuration imported from {filename}")
                    print("⚠️  Restart application to apply changes")
                except Exception as e:
                    print(f"❌ Import failed: {e}")
            else:
                print(f"❌ File {filename} not found")

def main():
    """Main function"""
    manager = ModelConfigManager()
    manager.run_interactive_setup()

if __name__ == "__main__":
    main()
