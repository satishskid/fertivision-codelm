"""
FertiVision powered by AI - Model Service Manager

This module handles API calls to different model providers with automatic fallback
and quality assessment.

© 2025 FertiVision powered by AI (made by greybrain.ai) - DeepSeek LLM Image Analysis
"""

import requests
import base64
import json
import time
from typing import Dict, Optional, List, Any, Tuple
from dataclasses import dataclass
from model_config import (
    ModelProvider, AnalysisType, ModelConfig, AnalysisConfig, 
    model_manager
)

@dataclass
class ModelResponse:
    """Response from a model service"""
    success: bool
    response: str
    provider: ModelProvider
    model_name: str
    processing_time: float
    token_count: Optional[int] = None
    cost: float = 0.0
    error: Optional[str] = None
    quality_score: Optional[float] = None

class ModelServiceManager:
    """Manages API calls to different model providers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FertiVision-powered-by-AI/1.0'
        })
    
    def analyze_with_model(self, 
                          analysis_type: AnalysisType,
                          prompt: str,
                          image_path: Optional[str] = None,
                          **kwargs) -> ModelResponse:
        """
        Analyze using configured model with automatic fallback
        """
        config = model_manager.get_config(analysis_type)
        if not config:
            return ModelResponse(
                success=False,
                response="",
                provider=ModelProvider.LOCAL_API,
                model_name="unknown",
                processing_time=0.0,
                error=f"No configuration found for {analysis_type.value}"
            )
        
        # Try primary model first
        response = self._call_model(config.primary_model, prompt, image_path, **kwargs)
        
        # Check if we need to use fallback
        if not response.success and config.use_fallback:
            print(f"⚠️ Primary model failed, trying fallback models...")
            
            for fallback_model in config.fallback_models:
                if not fallback_model.enabled:
                    continue
                    
                print(f"🔄 Trying fallback: {fallback_model.provider.value}")
                response = self._call_model(fallback_model, prompt, image_path, **kwargs)
                
                if response.success:
                    print(f"✅ Fallback successful: {fallback_model.provider.value}")
                    break
        
        # Assess quality if successful
        if response.success and config.quality_threshold > 0:
            quality_score = self._assess_response_quality(response.response, analysis_type)
            response.quality_score = quality_score
            
            if quality_score < config.quality_threshold:
                print(f"⚠️ Response quality below threshold: {quality_score:.2f} < {config.quality_threshold}")
        
        return response
    
    def _call_model(self, 
                   model_config: ModelConfig,
                   prompt: str,
                   image_path: Optional[str] = None,
                   **kwargs) -> ModelResponse:
        """Call a specific model"""
        
        if not model_config.enabled:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=0.0,
                error="Model is disabled"
            )
        
        start_time = time.time()
        
        try:
            if model_config.provider == ModelProvider.OLLAMA_LOCAL:
                return self._call_ollama(model_config, prompt, image_path, **kwargs)
            elif model_config.provider == ModelProvider.OPENAI:
                return self._call_openai(model_config, prompt, image_path, **kwargs)
            elif model_config.provider == ModelProvider.ANTHROPIC:
                return self._call_anthropic(model_config, prompt, image_path, **kwargs)
            elif model_config.provider == ModelProvider.GOOGLE:
                return self._call_google(model_config, prompt, image_path, **kwargs)
            elif model_config.provider == ModelProvider.OPENROUTER:
                return self._call_openrouter(model_config, prompt, image_path, **kwargs)
            elif model_config.provider == ModelProvider.GROQ:
                return self._call_groq(model_config, prompt, image_path, **kwargs)
            elif model_config.provider == ModelProvider.TOGETHER_AI:
                return self._call_together(model_config, prompt, image_path, **kwargs)
            elif model_config.provider == ModelProvider.DEEPSEEK:
                return self._call_deepseek_api(model_config, prompt, image_path, **kwargs)
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=time.time() - start_time,
                    error=f"Provider {model_config.provider.value} not implemented"
                )
                
        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )
    
    def _call_ollama(self, 
                    model_config: ModelConfig,
                    prompt: str,
                    image_path: Optional[str] = None,
                    **kwargs) -> ModelResponse:
        """Call Ollama local API"""
        start_time = time.time()
        
        payload = {
            "model": model_config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": model_config.temperature
            }
        }
        
        # Add image if provided
        if image_path:
            try:
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                payload["images"] = [image_data]
            except Exception as e:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=time.time() - start_time,
                    error=f"Failed to encode image: {e}"
                )
        
        try:
            response = self.session.post(
                model_config.api_url,
                json=payload,
                timeout=model_config.timeout
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return ModelResponse(
                    success=True,
                    response=result.get("response", ""),
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    cost=0.0  # Local models are free
                )
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.exceptions.Timeout:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="Request timeout"
            )
        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )
    
    def _call_openai(self, 
                    model_config: ModelConfig,
                    prompt: str,
                    image_path: Optional[str] = None,
                    **kwargs) -> ModelResponse:
        """Call OpenAI API"""
        start_time = time.time()
        
        if not model_config.api_key:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="OpenAI API key not provided"
            )
        
        headers = {
            "Authorization": f"Bearer {model_config.api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages
        messages = []
        
        if image_path and "vision" in model_config.model_name:
            # Vision model
            try:
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                })
            except Exception as e:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=time.time() - start_time,
                    error=f"Failed to encode image: {e}"
                )
        else:
            # Text-only model
            messages.append({
                "role": "user",
                "content": prompt
            })
        
        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "temperature": model_config.temperature
        }
        
        if model_config.max_tokens:
            payload["max_tokens"] = model_config.max_tokens
        
        try:
            response = self.session.post(
                model_config.api_url,
                headers=headers,
                json=payload,
                timeout=model_config.timeout
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Calculate cost
                usage = result.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens
                
                return ModelResponse(
                    success=True,
                    response=content,
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    token_count=total_tokens,
                    cost=cost
                )
            else:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {error_data}"
                )
                
        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )

    def _call_anthropic(self,
                       model_config: ModelConfig,
                       prompt: str,
                       image_path: Optional[str] = None,
                       **kwargs) -> ModelResponse:
        """Call Anthropic Claude API"""
        start_time = time.time()

        if not model_config.api_key:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="Anthropic API key not provided"
            )

        headers = {
            "x-api-key": model_config.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        # Note: Claude doesn't support vision yet, so we'll use text-only
        payload = {
            "model": model_config.model_name,
            "max_tokens": model_config.max_tokens or 4000,
            "temperature": model_config.temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = self.session.post(
                model_config.api_url,
                headers=headers,
                json=payload,
                timeout=model_config.timeout
            )

            processing_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                content = result["content"][0]["text"]

                # Calculate cost
                usage = result.get("usage", {})
                total_tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens

                return ModelResponse(
                    success=True,
                    response=content,
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    token_count=total_tokens,
                    cost=cost
                )
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )

    def _call_google(self,
                    model_config: ModelConfig,
                    prompt: str,
                    image_path: Optional[str] = None,
                    **kwargs) -> ModelResponse:
        """Call Google Gemini API"""
        start_time = time.time()

        if not model_config.api_key:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="Google API key not provided"
            )

        # Prepare content
        contents = [{"parts": [{"text": prompt}]}]

        # Add image if provided and model supports vision
        if image_path and "vision" in model_config.model_name:
            try:
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')

                contents[0]["parts"].append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_data
                    }
                })
            except Exception as e:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=time.time() - start_time,
                    error=f"Failed to encode image: {e}"
                )

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": model_config.temperature,
                "maxOutputTokens": model_config.max_tokens or 2048
            }
        }

        url = f"{model_config.api_url}?key={model_config.api_key}"

        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=model_config.timeout
            )

            processing_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()

                if "candidates" in result and result["candidates"]:
                    content = result["candidates"][0]["content"]["parts"][0]["text"]

                    # Estimate tokens (Google doesn't provide usage in response)
                    estimated_tokens = len(content.split()) * 1.3  # Rough estimate
                    cost = (estimated_tokens / 1000) * model_config.cost_per_1k_tokens

                    return ModelResponse(
                        success=True,
                        response=content,
                        provider=model_config.provider,
                        model_name=model_config.model_name,
                        processing_time=processing_time,
                        token_count=int(estimated_tokens),
                        cost=cost
                    )
                else:
                    return ModelResponse(
                        success=False,
                        response="",
                        provider=model_config.provider,
                        model_name=model_config.model_name,
                        processing_time=processing_time,
                        error="No candidates in response"
                    )
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )

    def _assess_response_quality(self, response: str, analysis_type: AnalysisType) -> float:
        """Assess the quality of a model response"""
        if not response or len(response.strip()) < 10:
            return 0.0

        quality_score = 0.5  # Base score

        # Check for medical keywords based on analysis type
        medical_keywords = {
            AnalysisType.FOLLICLE_ANALYSIS: ["follicle", "afc", "ovarian", "antral", "dominant"],
            AnalysisType.SPERM_ANALYSIS: ["sperm", "motility", "morphology", "concentration", "who"],
            AnalysisType.EMBRYO_ANALYSIS: ["embryo", "blastocyst", "gardner", "icm", "trophectoderm"],
            AnalysisType.OOCYTE_ANALYSIS: ["oocyte", "metaphase", "polar body", "zona pellucida"],
            AnalysisType.HYSTEROSCOPY_ANALYSIS: ["endometrial", "uterine", "cavity", "hysteroscopy"]
        }

        keywords = medical_keywords.get(analysis_type, [])
        response_lower = response.lower()

        # Award points for relevant keywords
        keyword_score = sum(0.1 for keyword in keywords if keyword in response_lower)
        quality_score += min(keyword_score, 0.3)  # Max 0.3 from keywords

        # Check for numerical values (important for medical analysis)
        import re
        numbers = re.findall(r'\d+\.?\d*', response)
        if numbers:
            quality_score += 0.1

        # Check for structured format
        if any(marker in response for marker in ["1.", "2.", "•", "-", ":"]):
            quality_score += 0.1

        return min(quality_score, 1.0)

    def _call_openrouter(self,
                        model_config: ModelConfig,
                        prompt: str,
                        image_path: Optional[str] = None,
                        **kwargs) -> ModelResponse:
        """Call OpenRouter API (OpenAI-compatible)"""
        start_time = time.time()

        if not model_config.api_key:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="OpenRouter API key not provided"
            )

        headers = {
            "Authorization": f"Bearer {model_config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://fertivision.ai",
            "X-Title": "FertiVision powered by AI"
        }

        # Prepare messages (OpenAI-compatible format)
        messages = []

        if image_path and "vision" in model_config.model_name:
            try:
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')

                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                })
            except Exception as e:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=time.time() - start_time,
                    error=f"Failed to encode image: {e}"
                )
        else:
            messages.append({
                "role": "user",
                "content": prompt
            })

        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "temperature": model_config.temperature
        }

        if model_config.max_tokens:
            payload["max_tokens"] = model_config.max_tokens

        try:
            response = self.session.post(
                model_config.api_url,
                headers=headers,
                json=payload,
                timeout=model_config.timeout
            )

            processing_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Calculate cost
                usage = result.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens

                return ModelResponse(
                    success=True,
                    response=content,
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    token_count=total_tokens,
                    cost=cost
                )
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )

    def _call_groq(self,
                  model_config: ModelConfig,
                  prompt: str,
                  image_path: Optional[str] = None,
                  **kwargs) -> ModelResponse:
        """Call Groq API (OpenAI-compatible, ultra-fast)"""
        start_time = time.time()

        if not model_config.api_key:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="Groq API key not provided"
            )

        headers = {
            "Authorization": f"Bearer {model_config.api_key}",
            "Content-Type": "application/json"
        }

        # Prepare messages
        messages = []

        if image_path and "llava" in model_config.model_name:
            try:
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')

                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                })
            except Exception as e:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=time.time() - start_time,
                    error=f"Failed to encode image: {e}"
                )
        else:
            messages.append({
                "role": "user",
                "content": prompt
            })

        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "temperature": model_config.temperature
        }

        if model_config.max_tokens:
            payload["max_tokens"] = model_config.max_tokens

        try:
            response = self.session.post(
                model_config.api_url,
                headers=headers,
                json=payload,
                timeout=model_config.timeout
            )

            processing_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Groq often provides usage info
                usage = result.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens  # Often free

                return ModelResponse(
                    success=True,
                    response=content,
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    token_count=total_tokens,
                    cost=cost
                )
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )

    def _call_together(self,
                      model_config: ModelConfig,
                      prompt: str,
                      image_path: Optional[str] = None,
                      **kwargs) -> ModelResponse:
        """Call Together AI API"""
        start_time = time.time()

        if not model_config.api_key:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="Together AI API key not provided"
            )

        headers = {
            "Authorization": f"Bearer {model_config.api_key}",
            "Content-Type": "application/json"
        }

        # Together AI uses OpenAI-compatible format
        messages = [{"role": "user", "content": prompt}]

        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "temperature": model_config.temperature
        }

        if model_config.max_tokens:
            payload["max_tokens"] = model_config.max_tokens

        try:
            response = self.session.post(
                model_config.api_url,
                headers=headers,
                json=payload,
                timeout=model_config.timeout
            )

            processing_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Calculate cost
                usage = result.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens

                return ModelResponse(
                    success=True,
                    response=content,
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    token_count=total_tokens,
                    cost=cost
                )
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )

    def _call_deepseek_api(self,
                          model_config: ModelConfig,
                          prompt: str,
                          image_path: Optional[str] = None,
                          **kwargs) -> ModelResponse:
        """Call DeepSeek API"""
        start_time = time.time()

        if not model_config.api_key:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error="DeepSeek API key not provided"
            )

        headers = {
            "Authorization": f"Bearer {model_config.api_key}",
            "Content-Type": "application/json"
        }

        messages = [{"role": "user", "content": prompt}]

        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "temperature": model_config.temperature
        }

        if model_config.max_tokens:
            payload["max_tokens"] = model_config.max_tokens

        try:
            response = self.session.post(
                model_config.api_url,
                headers=headers,
                json=payload,
                timeout=model_config.timeout
            )

            processing_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Calculate cost
                usage = result.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens

                return ModelResponse(
                    success=True,
                    response=content,
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    token_count=total_tokens,
                    cost=cost
                )
            else:
                return ModelResponse(
                    success=False,
                    response="",
                    provider=model_config.provider,
                    model_name=model_config.model_name,
                    processing_time=processing_time,
                    error=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as e:
            return ModelResponse(
                success=False,
                response="",
                provider=model_config.provider,
                model_name=model_config.model_name,
                processing_time=time.time() - start_time,
                error=str(e)
            )

# Global service manager instance
service_manager = ModelServiceManager()
