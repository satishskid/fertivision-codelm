/**
 * FertiVision Main Application
 * Initializes and coordinates all application modules
 */

class FertiVisionApp {
    constructor() {
        this.version = '1.0.0';
        this.buildDate = '2025-01-13';
        this.isInitialized = false;
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initialize());
        } else {
            this.initialize();
        }
    }

    /**
     * Initialize the application
     */
    async initialize() {
        if (this.isInitialized) return;

        console.log(`🚀 Initializing FertiVision v${this.version}`);
        console.log('🧬 AI-Enhanced Reproductive Medicine Analysis Platform');
        console.log('© 2025 FertiVision powered by AI | Made by greybrain.ai');

        try {
            // Initialize core modules
            await this.initializeModules();
            
            // Setup global error handling
            this.setupErrorHandling();
            
            // Setup performance monitoring
            this.setupPerformanceMonitoring();
            
            // Initialize tab content
            this.initializeTabContent();
            
            // Setup service worker for offline support
            this.setupServiceWorker();
            
            // Mark as initialized
            this.isInitialized = true;
            
            console.log('✅ FertiVision initialization complete');
            
            // Dispatch ready event
            window.dispatchEvent(new CustomEvent('fertivisionReady', {
                detail: { version: this.version, buildDate: this.buildDate }
            }));

        } catch (error) {
            console.error('❌ FertiVision initialization failed:', error);
            this.showInitializationError(error);
        }
    }

    /**
     * Initialize all application modules
     */
    async initializeModules() {
        // Modules are already initialized via their constructors
        // This method can be used for additional setup if needed
        
        // Verify all modules are available
        const requiredModules = [
            'FertiVisionConfig',
            'FertiVisionAPI', 
            'FertiVisionAnalysis',
            'FertiVisionDemos',
            'FertiVisionUI'
        ];

        for (const moduleName of requiredModules) {
            if (!window[moduleName]) {
                throw new Error(`Required module ${moduleName} not found`);
            }
        }

        console.log('📦 All modules loaded successfully');
    }

    /**
     * Initialize tab content
     */
    initializeTabContent() {
        // Add missing tab content for follicle and hysteroscopy
        this.createFollicleTab();
        this.createHysteroscopyTab();
        this.createTrainingTab();
    }

    /**
     * Create follicle analysis tab
     */
    createFollicleTab() {
        const follicleTab = document.getElementById('follicle-tab');
        if (!follicleTab || follicleTab.innerHTML.trim()) return;

        follicleTab.innerHTML = `
            <div class="analysis-container">
                <div class="upload-section">
                    <h2><i class="fas fa-search"></i> Follicle Scan Analysis</h2>
                    <p class="section-description">Upload ultrasound images for automated follicle counting and ovarian reserve assessment</p>
                    
                    <div class="upload-area" id="follicle-upload">
                        <div class="upload-content">
                            <i class="fas fa-cloud-upload-alt upload-icon"></i>
                            <h3>Upload Ovarian Ultrasound Image</h3>
                            <p>Drag & drop or click to select ultrasound image</p>
                            <input type="file" id="follicle-file" accept="image/*" class="file-input">
                            <button class="btn btn-primary" onclick="document.getElementById('follicle-file').click()">
                                Choose File
                            </button>
                        </div>
                    </div>
                    
                    <div class="analysis-options">
                        <div class="option-group">
                            <label for="follicle-patient-id">Patient ID (Optional)</label>
                            <input type="text" id="follicle-patient-id" placeholder="Enter patient ID">
                        </div>
                        <div class="option-group">
                            <label for="follicle-ovary-side">Ovary Side</label>
                            <select id="follicle-ovary-side">
                                <option value="bilateral">Bilateral</option>
                                <option value="left">Left Ovary</option>
                                <option value="right">Right Ovary</option>
                            </select>
                        </div>
                        <div class="option-group">
                            <label for="follicle-notes">Notes (Optional)</label>
                            <textarea id="follicle-notes" placeholder="Additional notes or observations"></textarea>
                        </div>
                    </div>
                    
                    <button id="analyze-follicle-btn" class="btn btn-primary btn-large" disabled>
                        <i class="fas fa-microscope"></i>
                        Analyze with AI
                    </button>
                </div>
                
                <div class="results-section">
                    <div id="follicle-results" class="results-container">
                        <div class="placeholder-content">
                            <i class="fas fa-chart-line placeholder-icon"></i>
                            <h3>Analysis Results</h3>
                            <p>Upload an ultrasound image to see detailed follicle analysis results</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create hysteroscopy analysis tab
     */
    createHysteroscopyTab() {
        const hysteroscopyTab = document.getElementById('hysteroscopy-tab');
        if (!hysteroscopyTab || hysteroscopyTab.innerHTML.trim()) return;

        hysteroscopyTab.innerHTML = `
            <div class="analysis-container">
                <div class="upload-section">
                    <h2><i class="fas fa-hospital"></i> Hysteroscopy Analysis</h2>
                    <p class="section-description">Upload hysteroscopy images for endometrial morphology and pathology analysis</p>
                    
                    <div class="upload-area" id="hysteroscopy-upload">
                        <div class="upload-content">
                            <i class="fas fa-cloud-upload-alt upload-icon"></i>
                            <h3>Upload Hysteroscopy Image</h3>
                            <p>Drag & drop or click to select hysteroscopy image</p>
                            <input type="file" id="hysteroscopy-file" accept="image/*" class="file-input">
                            <button class="btn btn-primary" onclick="document.getElementById('hysteroscopy-file').click()">
                                Choose File
                            </button>
                        </div>
                    </div>
                    
                    <div class="analysis-options">
                        <div class="option-group">
                            <label for="hysteroscopy-patient-id">Patient ID (Optional)</label>
                            <input type="text" id="hysteroscopy-patient-id" placeholder="Enter patient ID">
                        </div>
                        <div class="option-group">
                            <label for="hysteroscopy-cycle-day">Cycle Day (Optional)</label>
                            <input type="number" id="hysteroscopy-cycle-day" placeholder="Day of menstrual cycle" min="1" max="35">
                        </div>
                        <div class="option-group">
                            <label for="hysteroscopy-notes">Notes (Optional)</label>
                            <textarea id="hysteroscopy-notes" placeholder="Additional notes or observations"></textarea>
                        </div>
                    </div>
                    
                    <button id="analyze-hysteroscopy-btn" class="btn btn-primary btn-large" disabled>
                        <i class="fas fa-microscope"></i>
                        Analyze with AI
                    </button>
                </div>
                
                <div class="results-section">
                    <div id="hysteroscopy-results" class="results-container">
                        <div class="placeholder-content">
                            <i class="fas fa-chart-line placeholder-icon"></i>
                            <h3>Analysis Results</h3>
                            <p>Upload a hysteroscopy image to see detailed endometrial analysis results</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create training tab
     */
    createTrainingTab() {
        const trainingTab = document.getElementById('training-tab');
        if (!trainingTab || trainingTab.innerHTML.trim()) return;

        trainingTab.innerHTML = `
            <div class="training-container">
                <h2><i class="fas fa-graduation-cap"></i> FertiVision Training Center</h2>
                
                <div class="training-sections">
                    <div class="training-section">
                        <h3>🚀 Quick Start Guide</h3>
                        <div class="training-content">
                            <h4>Getting Started with FertiVision</h4>
                            <ol>
                                <li><strong>Upload Images:</strong> Click or drag medical images to the upload areas</li>
                                <li><strong>Configure Settings:</strong> Set up your AI provider and API keys in Settings</li>
                                <li><strong>Run Analysis:</strong> Click "Analyze with AI" to process your images</li>
                                <li><strong>Review Results:</strong> Examine detailed reports and clinical recommendations</li>
                                <li><strong>Export Reports:</strong> Download analysis results for documentation</li>
                            </ol>
                        </div>
                    </div>
                    
                    <div class="training-section">
                        <h3>🔬 Analysis Types</h3>
                        <div class="training-content">
                            <div class="analysis-type">
                                <h4>🧬 Sperm Analysis</h4>
                                <p>WHO 2021 compliant semen analysis including concentration, motility, and morphology assessment.</p>
                            </div>
                            
                            <div class="analysis-type">
                                <h4>🥚 Oocyte Analysis</h4>
                                <p>ESHRE guidelines-based maturity and quality assessment for ICSI procedures.</p>
                            </div>
                            
                            <div class="analysis-type">
                                <h4>👶 Embryo Analysis</h4>
                                <p>Gardner grading system for Day 3-6 embryo evaluation and transfer selection.</p>
                            </div>
                            
                            <div class="analysis-type">
                                <h4>🔬 Follicle Scan</h4>
                                <p>Automated follicle counting and ovarian reserve assessment using ultrasound images.</p>
                            </div>
                            
                            <div class="analysis-type">
                                <h4>🏥 Hysteroscopy</h4>
                                <p>Endometrial morphology analysis and pathology detection from hysteroscopy images.</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="training-section">
                        <h3>⚙️ Settings Configuration</h3>
                        <div class="training-content">
                            <h4>API Provider Setup</h4>
                            <p>Configure your preferred AI analysis provider:</p>
                            <ul>
                                <li><strong>Demo Mode:</strong> No API key required, uses mock data for testing</li>
                                <li><strong>Groq:</strong> Fast and free AI inference with vision models</li>
                                <li><strong>OpenRouter:</strong> Access to multiple AI models including Claude and GPT</li>
                            </ul>
                            
                            <h4>Getting API Keys</h4>
                            <ul>
                                <li><strong>Groq:</strong> Visit <a href="https://console.groq.com" target="_blank">console.groq.com</a></li>
                                <li><strong>OpenRouter:</strong> Sign up at <a href="https://openrouter.ai" target="_blank">openrouter.ai</a></li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="training-section">
                        <h3>🔒 Security & Privacy</h3>
                        <div class="training-content">
                            <p>FertiVision prioritizes the security and privacy of medical data:</p>
                            <ul>
                                <li>All processing is done through secure API connections</li>
                                <li>API keys are stored locally in your browser only</li>
                                <li>No medical images are stored on our servers</li>
                                <li>HIPAA-compliant data handling practices</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Setup global error handling
     */
    setupErrorHandling() {
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            this.logError('JavaScript Error', event.error);
        });

        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.logError('Promise Rejection', event.reason);
        });
    }

    /**
     * Setup performance monitoring
     */
    setupPerformanceMonitoring() {
        // Monitor page load performance
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    console.log(`📊 Page load time: ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
                }
            }, 0);
        });

        // Monitor memory usage (if available)
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                if (memory.usedJSHeapSize > memory.jsHeapSizeLimit * 0.9) {
                    console.warn('⚠️ High memory usage detected');
                }
            }, 30000); // Check every 30 seconds
        }
    }

    /**
     * Setup service worker for offline support
     */
    async setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                // For now, we'll skip service worker registration
                // Can be added later for offline support
                console.log('📱 Service worker support available');
            } catch (error) {
                console.warn('Service worker registration failed:', error);
            }
        }
    }

    /**
     * Log error for debugging
     */
    logError(type, error) {
        const errorInfo = {
            type,
            message: error.message || error,
            stack: error.stack,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href
        };

        // Store in localStorage for debugging
        try {
            const errors = JSON.parse(localStorage.getItem('fertivision-errors') || '[]');
            errors.push(errorInfo);
            // Keep only last 10 errors
            localStorage.setItem('fertivision-errors', JSON.stringify(errors.slice(-10)));
        } catch (e) {
            console.warn('Failed to store error log:', e);
        }
    }

    /**
     * Show initialization error
     */
    showInitializationError(error) {
        const errorContainer = document.createElement('div');
        errorContainer.className = 'initialization-error';
        errorContainer.innerHTML = `
            <div class="error-content">
                <h2>⚠️ Initialization Error</h2>
                <p>FertiVision failed to initialize properly.</p>
                <details>
                    <summary>Error Details</summary>
                    <pre>${error.message}\n${error.stack}</pre>
                </details>
                <button onclick="location.reload()" class="btn btn-primary">
                    Reload Application
                </button>
            </div>
        `;

        // Add error styles
        const style = document.createElement('style');
        style.textContent = `
            .initialization-error {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: var(--bg-secondary);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
            }
            .error-content {
                background: var(--bg-primary);
                padding: 2rem;
                border-radius: var(--border-radius);
                box-shadow: var(--shadow-lg);
                max-width: 500px;
                text-align: center;
            }
            .error-content h2 {
                color: var(--error-color);
                margin-bottom: 1rem;
            }
            .error-content details {
                margin: 1rem 0;
                text-align: left;
            }
            .error-content pre {
                background: var(--bg-secondary);
                padding: 1rem;
                border-radius: 4px;
                font-size: 0.8rem;
                overflow: auto;
                max-height: 200px;
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(errorContainer);
    }

    /**
     * Get application info
     */
    getAppInfo() {
        return {
            name: 'FertiVision',
            version: this.version,
            buildDate: this.buildDate,
            description: 'AI-Enhanced Reproductive Medicine Analysis Platform',
            author: 'greybrain.ai',
            isInitialized: this.isInitialized
        };
    }

    /**
     * Download sample image helper
     */
    downloadSampleImage(imageType) {
        if (window.FertiVisionDemos) {
            window.FertiVisionDemos.downloadSampleImage(imageType);
        }
    }
}

// Initialize the application
window.FertiVisionApp = new FertiVisionApp();

// Make downloadSampleImage globally available
window.downloadSampleImage = (imageType) => {
    if (window.FertiVisionApp) {
        window.FertiVisionApp.downloadSampleImage(imageType);
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FertiVisionApp;
}

console.log('🔬 FertiVision - AI-Enhanced Reproductive Medicine Analysis');
console.log('© 2025 FertiVision powered by AI | Made by greybrain.ai');
