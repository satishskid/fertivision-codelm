/**
 * FertiVision Configuration Management
 * Handles API keys, model selection, and environment variables
 */

class FertiVisionConfig {
    constructor() {
        this.apiProviders = {
            demo: {
                name: 'Demo Mode',
                description: 'No API required - uses mock data',
                requiresKey: false,
                models: ['demo-analysis']
            },
            groq: {
                name: 'Groq',
                description: 'Fast and free AI inference',
                requiresKey: true,
                baseUrl: 'https://api.groq.com/openai/v1',
                models: ['llava-v1.5-7b-4096-preview', 'llama-3.2-90b-vision-preview']
            },
            openrouter: {
                name: 'OpenRouter',
                description: 'Access to multiple AI models',
                requiresKey: true,
                baseUrl: 'https://openrouter.ai/api/v1',
                models: ['google/gemini-pro-vision', 'anthropic/claude-3-haiku', 'meta-llama/llama-3.2-90b-vision-instruct']
            }
        };
        
        this.currentConfig = this.loadConfig();
        this.initializeFromEnvironment();
    }

    /**
     * Initialize configuration from environment variables (Netlify)
     */
    initializeFromEnvironment() {
        // Check for Netlify environment variables
        const netlifyApiProvider = this.getEnvVar('VITE_API_PROVIDER') || this.getEnvVar('API_PROVIDER');
        const netlifyApiKey = this.getEnvVar('VITE_API_KEY') || this.getEnvVar('API_KEY');
        const netlifyModel = this.getEnvVar('VITE_MODEL') || this.getEnvVar('MODEL');

        if (netlifyApiProvider && this.apiProviders[netlifyApiProvider]) {
            this.currentConfig.provider = netlifyApiProvider;
            console.log(`🌐 Using environment API provider: ${netlifyApiProvider}`);
        }

        if (netlifyApiKey) {
            this.currentConfig.apiKey = netlifyApiKey;
            console.log('🔑 API key loaded from environment');
        }

        if (netlifyModel) {
            this.currentConfig.model = netlifyModel;
            console.log(`🤖 Using environment model: ${netlifyModel}`);
        }

        // Save the updated config
        this.saveConfig();
    }

    /**
     * Get environment variable (works in both development and production)
     */
    getEnvVar(name) {
        // Try different ways to access environment variables
        if (typeof process !== 'undefined' && process.env) {
            return process.env[name];
        }
        
        // For Netlify, environment variables are injected at build time
        if (typeof window !== 'undefined' && window.ENV) {
            return window.ENV[name];
        }
        
        // Fallback to checking if variables are defined globally
        if (typeof window !== 'undefined' && window[name]) {
            return window[name];
        }
        
        return null;
    }

    /**
     * Load configuration from localStorage
     */
    loadConfig() {
        const defaultConfig = {
            provider: 'demo',
            apiKey: '',
            model: 'demo-analysis',
            autoSave: true,
            showTechnicalDetails: true
        };

        try {
            const saved = localStorage.getItem('fertivision-config');
            if (saved) {
                return { ...defaultConfig, ...JSON.parse(saved) };
            }
        } catch (error) {
            console.warn('Failed to load config from localStorage:', error);
        }

        return defaultConfig;
    }

    /**
     * Save configuration to localStorage
     */
    saveConfig() {
        try {
            localStorage.setItem('fertivision-config', JSON.stringify(this.currentConfig));
            console.log('✅ Configuration saved');
        } catch (error) {
            console.error('Failed to save config:', error);
        }
    }

    /**
     * Update configuration
     */
    updateConfig(updates) {
        this.currentConfig = { ...this.currentConfig, ...updates };
        this.saveConfig();
        this.notifyConfigChange();
    }

    /**
     * Get current configuration
     */
    getConfig() {
        return { ...this.currentConfig };
    }

    /**
     * Get API provider information
     */
    getProviderInfo(provider = null) {
        const providerKey = provider || this.currentConfig.provider;
        return this.apiProviders[providerKey] || this.apiProviders.demo;
    }

    /**
     * Get available models for current provider
     */
    getAvailableModels(provider = null) {
        const providerInfo = this.getProviderInfo(provider);
        return providerInfo.models || ['demo-analysis'];
    }

    /**
     * Check if current configuration requires API key
     */
    requiresApiKey() {
        const providerInfo = this.getProviderInfo();
        return providerInfo.requiresKey && !this.currentConfig.apiKey;
    }

    /**
     * Validate current configuration
     */
    isValid() {
        const providerInfo = this.getProviderInfo();
        
        if (providerInfo.requiresKey && !this.currentConfig.apiKey) {
            return {
                valid: false,
                error: `API key required for ${providerInfo.name}`
            };
        }

        return { valid: true };
    }

    /**
     * Get API headers for requests
     */
    getApiHeaders() {
        const providerInfo = this.getProviderInfo();
        const headers = {
            'Content-Type': 'application/json'
        };

        if (providerInfo.requiresKey && this.currentConfig.apiKey) {
            if (this.currentConfig.provider === 'groq') {
                headers['Authorization'] = `Bearer ${this.currentConfig.apiKey}`;
            } else if (this.currentConfig.provider === 'openrouter') {
                headers['Authorization'] = `Bearer ${this.currentConfig.apiKey}`;
                headers['HTTP-Referer'] = window.location.origin;
                headers['X-Title'] = 'FertiVision';
            }
        }

        return headers;
    }

    /**
     * Get API endpoint URL
     */
    getApiUrl(endpoint = 'chat/completions') {
        const providerInfo = this.getProviderInfo();
        
        if (this.currentConfig.provider === 'demo') {
            return null; // Demo mode doesn't use external APIs
        }

        return `${providerInfo.baseUrl}/${endpoint}`;
    }

    /**
     * Reset configuration to defaults
     */
    resetConfig() {
        localStorage.removeItem('fertivision-config');
        this.currentConfig = this.loadConfig();
        this.notifyConfigChange();
        console.log('🔄 Configuration reset to defaults');
    }

    /**
     * Notify listeners of configuration changes
     */
    notifyConfigChange() {
        const event = new CustomEvent('configChanged', {
            detail: this.currentConfig
        });
        window.dispatchEvent(event);
    }

    /**
     * Export configuration (for backup)
     */
    exportConfig() {
        const exportData = {
            ...this.currentConfig,
            apiKey: this.currentConfig.apiKey ? '[REDACTED]' : ''
        };
        return JSON.stringify(exportData, null, 2);
    }

    /**
     * Import configuration (from backup)
     */
    importConfig(configJson) {
        try {
            const imported = JSON.parse(configJson);
            // Don't import API key for security
            delete imported.apiKey;
            this.updateConfig(imported);
            return true;
        } catch (error) {
            console.error('Failed to import config:', error);
            return false;
        }
    }

    /**
     * Get demo data for mock responses
     */
    getDemoData(analysisType) {
        const demoData = {
            sperm: {
                classification: 'Normozoospermia',
                parameters: {
                    concentration: 45.0,
                    progressive_motility: 65.0,
                    normal_morphology: 8.0,
                    volume: 3.0
                },
                confidence: 94.2,
                analysis: 'Comprehensive semen analysis demonstrates excellent reproductive potential with all parameters exceeding WHO 2021 reference values.',
                technicalDetails: {
                    'Concentration': '45.0 × 10⁶/ml (Ref: >15)',
                    'Progressive Motility': '65% (Ref: >32%)',
                    'Normal Morphology': '8% (Ref: >4%)',
                    'Volume': '3.0ml (Ref: >1.5ml)',
                    'pH': '7.8 (Ref: 7.2-8.0)',
                    'Vitality': '85% (Ref: >58%)'
                },
                clinicalRecommendations: [
                    'Excellent fertility potential - natural conception likely',
                    'Suitable for all ART procedures (IUI, IVF, ICSI)',
                    'No immediate treatment required',
                    'Maintain healthy lifestyle and nutrition'
                ]
            },
            oocyte: {
                classification: 'Metaphase II (MII) - Mature',
                parameters: {
                    maturity: 'MII',
                    morphology_score: 8.5,
                    polar_body: 'Present',
                    cytoplasm: 'Clear'
                },
                confidence: 92.8,
                analysis: 'Oocyte demonstrates optimal maturity with clear morphological indicators of fertilization competence.',
                technicalDetails: {
                    'Maturity Stage': 'Metaphase II (MII)',
                    'Morphology Score': '8.5/10 (Excellent)',
                    'Polar Body': 'Present and normal',
                    'Cytoplasm': 'Clear and homogeneous',
                    'Zona Pellucida': 'Normal thickness',
                    'Perivitelline Space': 'Normal'
                },
                clinicalRecommendations: [
                    'Excellent candidate for ICSI fertilization',
                    'High probability of successful fertilization',
                    'Optimal timing for insemination',
                    'Expected good embryo development'
                ]
            },
            embryo: {
                classification: 'Grade A Embryo - Excellent Quality',
                parameters: {
                    day: 3,
                    cell_count: 8,
                    fragmentation: 5.0,
                    grade: 'A'
                },
                confidence: 96.1,
                analysis: 'Outstanding embryo quality with optimal developmental progression and minimal fragmentation.',
                technicalDetails: {
                    'Development Day': 'Day 3 (72 hours)',
                    'Cell Count': '8 cells (optimal)',
                    'Fragmentation': '<5% (minimal)',
                    'Cell Symmetry': '95% (excellent)',
                    'Grade': 'A (excellent)',
                    'Implantation Potential': 'High (>60%)'
                },
                clinicalRecommendations: [
                    'Excellent candidate for fresh embryo transfer',
                    'High probability of successful implantation',
                    'Consider single embryo transfer',
                    'Suitable for cryopreservation if needed'
                ]
            },
            follicle: {
                classification: 'Normal Ovarian Reserve',
                parameters: {
                    total_follicles: 18,
                    afc: 12,
                    dominant_size: 16.2,
                    ovary_side: 'bilateral'
                },
                confidence: 91.5,
                analysis: 'Bilateral ovarian assessment shows excellent follicular development with normal antral follicle count indicating good ovarian reserve.',
                technicalDetails: {
                    'Total Follicles': '18 (bilateral)',
                    'Antral Follicle Count': '12 (2-10mm)',
                    'Dominant Follicle': '16.2mm (right ovary)',
                    'Small Follicles': '6 (<2mm)',
                    'Medium Follicles': '10 (2-10mm)',
                    'Large Follicles': '2 (>10mm)',
                    'Ovarian Volume': '8.5ml (normal)'
                },
                clinicalRecommendations: [
                    'Normal ovarian reserve for age',
                    'Good response expected for ovarian stimulation',
                    'Optimal timing for IVF cycle initiation',
                    'Continue current fertility treatment plan'
                ]
            },
            hysteroscopy: {
                classification: 'Normal Endometrial Morphology',
                parameters: {
                    cavity_shape: 'normal',
                    endometrial_thickness: 8.5,
                    pattern: 'proliferative',
                    pathology: 'none'
                },
                confidence: 89.3,
                analysis: 'Hysteroscopic examination reveals normal uterine cavity with healthy endometrial lining appropriate for cycle phase.',
                technicalDetails: {
                    'Uterine Cavity': 'Normal triangular shape',
                    'Endometrial Thickness': '8.5mm (normal)',
                    'Endometrial Pattern': 'Proliferative phase',
                    'Vascularization': 'Normal spiral arteries',
                    'Cervical Canal': 'Patent and normal',
                    'Tubal Ostia': 'Bilateral and patent'
                },
                clinicalRecommendations: [
                    'Excellent endometrial receptivity',
                    'Optimal for embryo transfer',
                    'No intervention required',
                    'Continue current treatment protocol'
                ]
            }
        };

        return demoData[analysisType] || demoData.sperm;
    }
}

// Initialize global configuration
window.FertiVisionConfig = new FertiVisionConfig();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FertiVisionConfig;
}
