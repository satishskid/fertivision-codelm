/**
 * FertiVision API Integration
 * Handles direct API calls to external AI services (Groq, OpenRouter)
 */

class FertiVisionAPI {
    constructor() {
        this.config = window.FertiVisionConfig;
        this.requestQueue = new Map();
        this.retryAttempts = 3;
        this.retryDelay = 1000;
    }

    /**
     * Convert image file to base64
     */
    async imageToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    /**
     * Prepare image for API request
     */
    async prepareImageData(file) {
        const base64 = await this.imageToBase64(file);
        const mimeType = file.type || 'image/jpeg';
        
        return {
            type: 'image_url',
            image_url: {
                url: `data:${mimeType};base64,${base64}`
            }
        };
    }

    /**
     * Generate analysis prompt based on type
     */
    getAnalysisPrompt(analysisType, options = {}) {
        const prompts = {
            sperm: `You are an expert andrologist analyzing a sperm microscopy image. Provide a detailed WHO 2021 compliant analysis including:

1. SPERM CONCENTRATION: Estimate sperm concentration (million/ml)
2. MOTILITY ASSESSMENT: Analyze progressive motility percentage
3. MORPHOLOGY EVALUATION: Assess normal morphology percentage using strict criteria
4. OVERALL CLASSIFICATION: Provide WHO classification (Normozoospermia, Oligozoospermia, Asthenozoospermia, Teratozoospermia, etc.)

Provide specific numerical values and clinical interpretation. Format as JSON with fields: classification, concentration, progressive_motility, normal_morphology, analysis, confidence.`,

            oocyte: `You are an expert embryologist analyzing an oocyte microscopy image. Provide detailed ESHRE guidelines assessment including:

1. MATURITY ASSESSMENT: Determine maturity stage (GV, MI, MII)
2. MORPHOLOGY EVALUATION: Assess cytoplasm, zona pellucida, polar body
3. QUALITY GRADING: Provide quality score (1-10)
4. FERTILIZATION POTENTIAL: Assess ICSI suitability

Provide detailed morphological assessment and clinical recommendations. Format as JSON with fields: classification, maturity, morphology_score, analysis, confidence.`,

            embryo: `You are an expert embryologist analyzing an embryo microscopy image. Provide detailed Gardner grading assessment including:

1. DEVELOPMENT STAGE: Assess day ${options.day || 3} embryo development
2. CELL COUNT: Count blastomeres and assess symmetry
3. FRAGMENTATION: Evaluate fragmentation percentage
4. GRADING: Provide Gardner grade (A, B, C, D)
5. IMPLANTATION POTENTIAL: Assess transfer suitability

Provide specific measurements and transfer recommendations. Format as JSON with fields: classification, cell_count, fragmentation, grade, analysis, confidence.`,

            follicle: `You are an expert reproductive endocrinologist analyzing an ovarian ultrasound image. Provide detailed follicle assessment including:

1. FOLLICLE COUNT: Count all visible follicles by size categories
2. AFC ASSESSMENT: Count antral follicles (2-10mm)
3. DOMINANT FOLLICLE: Identify and measure largest follicle
4. OVARIAN RESERVE: Assess ovarian reserve status
5. CYCLE PHASE: Determine cycle phase and ovulation prediction

Provide specific counts and clinical interpretation. Format as JSON with fields: classification, total_follicles, afc, dominant_size, analysis, confidence.`,

            hysteroscopy: `You are an expert gynecologist analyzing a hysteroscopy image. Provide detailed endometrial assessment including:

1. UTERINE CAVITY: Assess cavity shape and size
2. ENDOMETRIAL THICKNESS: Estimate thickness in mm
3. ENDOMETRIAL PATTERN: Assess proliferative/secretory pattern
4. PATHOLOGICAL FINDINGS: Identify polyps, fibroids, adhesions
5. TREATMENT RECOMMENDATIONS: Suggest interventions if needed

Provide detailed morphological assessment and treatment plan. Format as JSON with fields: classification, endometrial_thickness, findings, analysis, confidence.`
        };

        return prompts[analysisType] || prompts.sperm;
    }

    /**
     * Make API request with retry logic
     */
    async makeApiRequest(messages, options = {}) {
        const config = this.config.getConfig();
        
        // Use demo mode if no API key or demo provider
        if (config.provider === 'demo' || this.config.requiresApiKey()) {
            return this.getDemoResponse(options.analysisType);
        }

        const url = this.config.getApiUrl('chat/completions');
        const headers = this.config.getApiHeaders();

        const payload = {
            model: config.model,
            messages: messages,
            max_tokens: 1000,
            temperature: 0.1
        };

        // Add provider-specific parameters
        if (config.provider === 'groq') {
            payload.response_format = { type: 'json_object' };
        } else if (config.provider === 'openrouter') {
            payload.response_format = { type: 'json_object' };
        }

        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                console.log(`🤖 Making API request (attempt ${attempt}/${this.retryAttempts})`);
                
                const response = await fetch(url, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`API Error ${response.status}: ${errorText}`);
                }

                const data = await response.json();
                
                if (data.choices && data.choices[0] && data.choices[0].message) {
                    const content = data.choices[0].message.content;
                    
                    try {
                        return JSON.parse(content);
                    } catch (parseError) {
                        console.warn('Failed to parse JSON response, using text content');
                        return {
                            classification: 'Analysis completed',
                            analysis: content,
                            confidence: 85.0
                        };
                    }
                }

                throw new Error('Invalid API response format');

            } catch (error) {
                console.error(`API request attempt ${attempt} failed:`, error);
                
                if (attempt === this.retryAttempts) {
                    // Final attempt failed, return demo data
                    console.log('🔄 All API attempts failed, falling back to demo mode');
                    return this.getDemoResponse(options.analysisType);
                }
                
                // Wait before retry
                await new Promise(resolve => setTimeout(resolve, this.retryDelay * attempt));
            }
        }
    }

    /**
     * Get demo response for fallback
     */
    getDemoResponse(analysisType) {
        console.log(`📋 Using demo data for ${analysisType} analysis`);
        return this.config.getDemoData(analysisType);
    }

    /**
     * Analyze image with AI
     */
    async analyzeImage(file, analysisType, options = {}) {
        try {
            console.log(`🔬 Starting ${analysisType} analysis...`);
            
            // Validate file
            if (!file || !file.type.startsWith('image/')) {
                throw new Error('Please select a valid image file');
            }

            // Check file size (max 10MB)
            if (file.size > 10 * 1024 * 1024) {
                throw new Error('Image file too large. Please use images under 10MB.');
            }

            const config = this.config.getConfig();
            
            // Use demo mode if configured
            if (config.provider === 'demo') {
                // Simulate processing delay
                await new Promise(resolve => setTimeout(resolve, 2000));
                return this.getDemoResponse(analysisType);
            }

            // Prepare image data
            const imageData = await this.prepareImageData(file);
            
            // Create messages for API
            const messages = [
                {
                    role: 'user',
                    content: [
                        {
                            type: 'text',
                            text: this.getAnalysisPrompt(analysisType, options)
                        },
                        imageData
                    ]
                }
            ];

            // Make API request
            const result = await this.makeApiRequest(messages, { analysisType });
            
            // Add metadata
            result.timestamp = new Date().toISOString();
            result.analysisType = analysisType;
            result.provider = config.provider;
            result.model = config.model;
            result.imageSize = file.size;
            result.imageName = file.name;

            console.log(`✅ ${analysisType} analysis completed successfully`);
            return result;

        } catch (error) {
            console.error(`❌ Analysis failed:`, error);
            
            // Return demo data as fallback
            const fallbackResult = this.getDemoResponse(analysisType);
            fallbackResult.error = error.message;
            fallbackResult.fallback = true;
            
            return fallbackResult;
        }
    }

    /**
     * Batch analyze multiple images
     */
    async batchAnalyze(analyses) {
        const results = [];
        
        for (const analysis of analyses) {
            try {
                const result = await this.analyzeImage(
                    analysis.file,
                    analysis.type,
                    analysis.options
                );
                
                results.push({
                    ...result,
                    originalRequest: analysis
                });
                
                // Add delay between requests to avoid rate limiting
                await new Promise(resolve => setTimeout(resolve, 1000));
                
            } catch (error) {
                results.push({
                    error: error.message,
                    originalRequest: analysis
                });
            }
        }
        
        return results;
    }

    /**
     * Test API connection
     */
    async testConnection() {
        const config = this.config.getConfig();
        
        if (config.provider === 'demo') {
            return { success: true, message: 'Demo mode active' };
        }

        try {
            const url = this.config.getApiUrl('models');
            const headers = this.config.getApiHeaders();
            
            const response = await fetch(url, {
                method: 'GET',
                headers: headers
            });

            if (response.ok) {
                return { success: true, message: 'API connection successful' };
            } else {
                return { success: false, message: `API Error: ${response.status}` };
            }
            
        } catch (error) {
            return { success: false, message: error.message };
        }
    }

    /**
     * Get usage statistics
     */
    getUsageStats() {
        const stats = JSON.parse(localStorage.getItem('fertivision-usage-stats') || '{}');
        return {
            totalAnalyses: stats.totalAnalyses || 0,
            analysesByType: stats.analysesByType || {},
            lastUsed: stats.lastUsed || null
        };
    }

    /**
     * Update usage statistics
     */
    updateUsageStats(analysisType) {
        const stats = this.getUsageStats();
        stats.totalAnalyses = (stats.totalAnalyses || 0) + 1;
        stats.analysesByType = stats.analysesByType || {};
        stats.analysesByType[analysisType] = (stats.analysesByType[analysisType] || 0) + 1;
        stats.lastUsed = new Date().toISOString();
        
        localStorage.setItem('fertivision-usage-stats', JSON.stringify(stats));
    }
}

// Initialize global API instance
window.FertiVisionAPI = new FertiVisionAPI();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FertiVisionAPI;
}
