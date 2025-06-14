/**
 * FertiVision UI Management
 * Handles user interface interactions and navigation
 */

class FertiVisionUI {
    constructor() {
        this.config = window.FertiVisionConfig;
        this.currentTab = 'sperm';
        this.initializeEventListeners();
        this.initializeUI();
    }

    /**
     * Initialize UI event listeners
     */
    initializeEventListeners() {
        // Tab navigation
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('tab-btn')) {
                const tabName = e.target.getAttribute('data-tab');
                this.switchTab(tabName);
            }
        });

        // Settings modal
        document.addEventListener('click', (e) => {
            if (e.target.id === 'settings-btn') {
                this.openSettingsModal();
            } else if (e.target.id === 'close-settings') {
                this.closeSettingsModal();
            } else if (e.target.id === 'save-settings') {
                this.saveSettings();
            } else if (e.target.id === 'reset-settings') {
                this.resetSettings();
            }
        });

        // Modal backdrop click
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeSettingsModal();
            }
        });

        // API provider change
        document.addEventListener('change', (e) => {
            if (e.target.id === 'api-provider') {
                this.handleProviderChange(e.target.value);
            }
        });

        // Configuration change listener
        window.addEventListener('configChanged', (e) => {
            this.updateModeIndicator();
            this.updateModelSelection();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case ',':
                        e.preventDefault();
                        this.openSettingsModal();
                        break;
                    case '1':
                    case '2':
                    case '3':
                    case '4':
                    case '5':
                    case '6':
                    case '7':
                        e.preventDefault();
                        const tabs = ['sperm', 'oocyte', 'embryo', 'follicle', 'hysteroscopy', 'datasets', 'training'];
                        const tabIndex = parseInt(e.key) - 1;
                        if (tabs[tabIndex]) {
                            this.switchTab(tabs[tabIndex]);
                        }
                        break;
                }
            }
        });
    }

    /**
     * Initialize UI components
     */
    initializeUI() {
        this.hideLoadingScreen();
        this.updateModeIndicator();
        this.initializeSettingsModal();
        this.addKeyboardShortcutsHelp();
    }

    /**
     * Hide loading screen and show app
     */
    hideLoadingScreen() {
        setTimeout(() => {
            const loadingScreen = document.getElementById('loading-screen');
            const appContainer = document.getElementById('app-container');
            
            if (loadingScreen && appContainer) {
                loadingScreen.style.opacity = '0';
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                    appContainer.style.display = 'flex';
                    appContainer.style.opacity = '0';
                    setTimeout(() => {
                        appContainer.style.opacity = '1';
                        appContainer.style.transition = 'opacity 0.5s ease';
                    }, 50);
                }, 500);
            }
        }, 1500);
    }

    /**
     * Switch between tabs
     */
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        this.currentTab = tabName;

        // Add tab-specific initialization
        this.initializeTabContent(tabName);
    }

    /**
     * Initialize tab-specific content
     */
    initializeTabContent(tabName) {
        switch (tabName) {
            case 'embryo':
                this.initializeEmbryoTab();
                break;
            case 'datasets':
                this.initializeDatasetsTab();
                break;
            case 'training':
                this.initializeTrainingTab();
                break;
        }
    }

    /**
     * Initialize embryo tab with day selection
     */
    initializeEmbryoTab() {
        const embryoTab = document.getElementById('embryo-tab');
        if (!embryoTab || embryoTab.querySelector('#embryo-day')) return;

        const analysisOptions = embryoTab.querySelector('.analysis-options');
        if (analysisOptions) {
            const dayOption = document.createElement('div');
            dayOption.className = 'option-group';
            dayOption.innerHTML = `
                <label for="embryo-day">Development Day</label>
                <select id="embryo-day">
                    <option value="3">Day 3 (Cleavage stage)</option>
                    <option value="5">Day 5 (Blastocyst)</option>
                    <option value="6">Day 6 (Blastocyst)</option>
                </select>
            `;
            analysisOptions.insertBefore(dayOption, analysisOptions.firstChild);
        }
    }

    /**
     * Initialize datasets tab
     */
    initializeDatasetsTab() {
        const demoResults = document.getElementById('demo-results');
        if (demoResults && !demoResults.innerHTML.trim()) {
            demoResults.innerHTML = `
                <div class="demo-placeholder">
                    <div class="placeholder-content">
                        <i class="fas fa-flask placeholder-icon"></i>
                        <h3>Interactive AI Demos</h3>
                        <p>Click any demo button above to see comprehensive medical analysis results</p>
                    </div>
                </div>
            `;
        }
    }

    /**
     * Initialize training tab
     */
    initializeTrainingTab() {
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
                                <ul>
                                    <li>Concentration measurement (million/ml)</li>
                                    <li>Progressive motility percentage</li>
                                    <li>Normal morphology assessment</li>
                                    <li>Clinical classification and recommendations</li>
                                </ul>
                            </div>
                            
                            <div class="analysis-type">
                                <h4>🥚 Oocyte Analysis</h4>
                                <p>ESHRE guidelines-based maturity and quality assessment for ICSI procedures.</p>
                                <ul>
                                    <li>Maturity stage determination (GV, MI, MII)</li>
                                    <li>Morphology scoring (1-10 scale)</li>
                                    <li>Fertilization potential assessment</li>
                                    <li>ICSI suitability evaluation</li>
                                </ul>
                            </div>
                            
                            <div class="analysis-type">
                                <h4>👶 Embryo Analysis</h4>
                                <p>Gardner grading system for Day 3-6 embryo evaluation and transfer selection.</p>
                                <ul>
                                    <li>Cell count and symmetry assessment</li>
                                    <li>Fragmentation percentage calculation</li>
                                    <li>Grade assignment (A, B, C, D)</li>
                                    <li>Implantation potential prediction</li>
                                </ul>
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
                                <li><strong>Groq:</strong> Visit <a href="https://console.groq.com" target="_blank">console.groq.com</a> to get your free API key</li>
                                <li><strong>OpenRouter:</strong> Sign up at <a href="https://openrouter.ai" target="_blank">openrouter.ai</a> for API access</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="training-section">
                        <h3>🔒 Security & Privacy</h3>
                        <div class="training-content">
                            <p>FertiVision prioritizes the security and privacy of medical data:</p>
                            <ul>
                                <li>All image processing is done through secure API connections</li>
                                <li>API keys are stored locally in your browser only</li>
                                <li>No medical images are stored on our servers</li>
                                <li>Analysis results can be exported for local storage</li>
                                <li>HIPAA-compliant data handling practices</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="training-section">
                        <h3>⌨️ Keyboard Shortcuts</h3>
                        <div class="training-content">
                            <div class="shortcuts-grid">
                                <div class="shortcut-item">
                                    <kbd>Ctrl/Cmd + ,</kbd>
                                    <span>Open Settings</span>
                                </div>
                                <div class="shortcut-item">
                                    <kbd>Ctrl/Cmd + 1-7</kbd>
                                    <span>Switch Tabs</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Update mode indicator
     */
    updateModeIndicator() {
        const modeIndicator = document.getElementById('current-mode');
        if (!modeIndicator) return;

        const config = this.config.getConfig();
        const providerInfo = this.config.getProviderInfo();
        
        modeIndicator.textContent = providerInfo.name;
        modeIndicator.className = 'mode-value';
        
        if (config.provider === 'demo') {
            modeIndicator.classList.add('demo-mode');
        } else {
            modeIndicator.classList.add('api-mode');
        }
    }

    /**
     * Open settings modal
     */
    openSettingsModal() {
        const modal = document.getElementById('settings-modal');
        if (modal) {
            modal.classList.add('active');
            this.populateSettingsForm();
        }
    }

    /**
     * Close settings modal
     */
    closeSettingsModal() {
        const modal = document.getElementById('settings-modal');
        if (modal) {
            modal.classList.remove('active');
        }
    }

    /**
     * Initialize settings modal
     */
    initializeSettingsModal() {
        this.populateSettingsForm();
    }

    /**
     * Populate settings form with current configuration
     */
    populateSettingsForm() {
        const config = this.config.getConfig();
        
        // API Provider
        const providerSelect = document.getElementById('api-provider');
        if (providerSelect) {
            providerSelect.value = config.provider;
            this.handleProviderChange(config.provider);
        }

        // API Key
        const apiKeyInput = document.getElementById('api-key');
        if (apiKeyInput) {
            apiKeyInput.value = config.apiKey || '';
        }

        // Model Selection
        this.updateModelSelection();

        // Other settings
        const autoSaveCheckbox = document.getElementById('auto-save-results');
        if (autoSaveCheckbox) {
            autoSaveCheckbox.checked = config.autoSave;
        }

        const technicalDetailsCheckbox = document.getElementById('show-technical-details');
        if (technicalDetailsCheckbox) {
            technicalDetailsCheckbox.checked = config.showTechnicalDetails;
        }
    }

    /**
     * Handle API provider change
     */
    handleProviderChange(provider) {
        const providerInfo = this.config.getProviderInfo(provider);
        const apiKeyGroup = document.getElementById('api-key-group');
        
        if (apiKeyGroup) {
            if (providerInfo.requiresKey) {
                apiKeyGroup.style.display = 'block';
            } else {
                apiKeyGroup.style.display = 'none';
            }
        }

        this.updateModelSelection(provider);
    }

    /**
     * Update model selection dropdown
     */
    updateModelSelection(provider = null) {
        const modelSelect = document.getElementById('model-selection');
        if (!modelSelect) return;

        const models = this.config.getAvailableModels(provider);
        const config = this.config.getConfig();
        
        modelSelect.innerHTML = '';
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            if (model === config.model) {
                option.selected = true;
            }
            modelSelect.appendChild(option);
        });
    }

    /**
     * Save settings
     */
    saveSettings() {
        const provider = document.getElementById('api-provider').value;
        const apiKey = document.getElementById('api-key').value;
        const model = document.getElementById('model-selection').value;
        const autoSave = document.getElementById('auto-save-results').checked;
        const showTechnicalDetails = document.getElementById('show-technical-details').checked;

        this.config.updateConfig({
            provider,
            apiKey,
            model,
            autoSave,
            showTechnicalDetails
        });

        this.closeSettingsModal();
        this.showNotification('Settings saved successfully!', 'success');
    }

    /**
     * Reset settings to defaults
     */
    resetSettings() {
        if (confirm('Are you sure you want to reset all settings to defaults?')) {
            this.config.resetConfig();
            this.populateSettingsForm();
            this.showNotification('Settings reset to defaults', 'info');
        }
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);

        // Manual close
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });

        // Add notification styles if not present
        this.addNotificationStyles();
    }

    /**
     * Add notification styles
     */
    addNotificationStyles() {
        if (document.getElementById('notification-styles')) return;

        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--bg-primary);
                border-radius: var(--border-radius);
                box-shadow: var(--shadow-lg);
                border-left: 4px solid var(--primary-color);
                z-index: 10000;
                animation: slideIn 0.3s ease;
            }
            
            .notification.success {
                border-left-color: var(--success-color);
            }
            
            .notification.error {
                border-left-color: var(--error-color);
            }
            
            .notification.warning {
                border-left-color: var(--warning-color);
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1rem 1.5rem;
                gap: 1rem;
            }
            
            .notification-close {
                background: none;
                border: none;
                font-size: 1.2rem;
                cursor: pointer;
                color: var(--text-secondary);
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Add keyboard shortcuts help
     */
    addKeyboardShortcutsHelp() {
        const style = document.createElement('style');
        style.textContent = `
            .shortcuts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }
            
            .shortcut-item {
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 0.75rem;
                background: var(--bg-secondary);
                border-radius: var(--border-radius);
            }
            
            kbd {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 0.25rem 0.5rem;
                font-family: monospace;
                font-size: 0.8rem;
                font-weight: 600;
            }
            
            .training-container {
                max-width: 800px;
                margin: 0 auto;
            }
            
            .training-sections {
                display: flex;
                flex-direction: column;
                gap: 2rem;
            }
            
            .training-section {
                background: var(--bg-primary);
                border-radius: var(--border-radius);
                padding: 2rem;
                box-shadow: var(--shadow-md);
            }
            
            .training-section h3 {
                color: var(--primary-color);
                margin-bottom: 1rem;
                font-size: 1.3rem;
            }
            
            .training-content h4 {
                color: var(--text-primary);
                margin: 1.5rem 0 0.5rem 0;
                font-size: 1.1rem;
            }
            
            .training-content ul,
            .training-content ol {
                margin: 1rem 0;
                padding-left: 1.5rem;
            }
            
            .training-content li {
                margin-bottom: 0.5rem;
                line-height: 1.6;
            }
            
            .analysis-type {
                margin-bottom: 2rem;
                padding-bottom: 1.5rem;
                border-bottom: 1px solid var(--border-color);
            }
            
            .analysis-type:last-child {
                border-bottom: none;
                margin-bottom: 0;
            }
            
            .demo-mode {
                color: var(--warning-color) !important;
            }
            
            .api-mode {
                color: var(--success-color) !important;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize global UI instance
window.FertiVisionUI = new FertiVisionUI();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FertiVisionUI;
}
