/**
 * FertiVision Analysis Module
 * Handles image analysis workflows and result display
 */

class FertiVisionAnalysis {
    constructor() {
        this.api = window.FertiVisionAPI;
        this.config = window.FertiVisionConfig;
        this.currentAnalyses = new Map();
        this.analysisHistory = [];
        
        this.initializeEventListeners();
    }

    /**
     * Initialize event listeners for analysis workflows
     */
    initializeEventListeners() {
        // File input handlers
        document.addEventListener('change', (e) => {
            if (e.target.type === 'file' && e.target.accept === 'image/*') {
                this.handleFileSelection(e.target);
            }
        });

        // Drag and drop handlers
        document.addEventListener('dragover', (e) => {
            e.preventDefault();
            const uploadArea = e.target.closest('.upload-area');
            if (uploadArea) {
                uploadArea.classList.add('dragover');
            }
        });

        document.addEventListener('dragleave', (e) => {
            const uploadArea = e.target.closest('.upload-area');
            if (uploadArea && !uploadArea.contains(e.relatedTarget)) {
                uploadArea.classList.remove('dragover');
            }
        });

        document.addEventListener('drop', (e) => {
            e.preventDefault();
            const uploadArea = e.target.closest('.upload-area');
            if (uploadArea) {
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    const analysisType = this.getAnalysisTypeFromElement(uploadArea);
                    this.handleFileSelection(null, files[0], analysisType);
                }
            }
        });

        // Analysis button handlers
        document.addEventListener('click', (e) => {
            if (e.target.id && e.target.id.startsWith('analyze-') && e.target.id.endsWith('-btn')) {
                const analysisType = e.target.id.replace('analyze-', '').replace('-btn', '');
                this.startAnalysis(analysisType);
            }
        });
    }

    /**
     * Get analysis type from DOM element
     */
    getAnalysisTypeFromElement(element) {
        const tabContent = element.closest('.tab-content');
        if (tabContent) {
            return tabContent.id.replace('-tab', '');
        }
        return 'sperm'; // default
    }

    /**
     * Handle file selection
     */
    handleFileSelection(input, file = null, analysisType = null) {
        const selectedFile = file || (input && input.files[0]);
        if (!selectedFile) return;

        const type = analysisType || this.getAnalysisTypeFromElement(input);
        
        // Validate file
        if (!selectedFile.type.startsWith('image/')) {
            this.showError(`Please select a valid image file`, type);
            return;
        }

        if (selectedFile.size > 10 * 1024 * 1024) {
            this.showError(`Image file too large. Please use images under 10MB.`, type);
            return;
        }

        // Store file and update UI
        this.currentAnalyses.set(type, {
            file: selectedFile,
            timestamp: new Date().toISOString()
        });

        this.updateFileDisplay(type, selectedFile);
        this.enableAnalysisButton(type);
    }

    /**
     * Update file display in upload area
     */
    updateFileDisplay(analysisType, file) {
        const uploadArea = document.querySelector(`#${analysisType}-upload`);
        if (!uploadArea) return;

        const uploadContent = uploadArea.querySelector('.upload-content');
        if (!uploadContent) return;

        // Create file preview
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        fileInfo.innerHTML = `
            <div class="file-preview">
                <i class="fas fa-image file-icon"></i>
                <div class="file-details">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${this.formatFileSize(file.size)}</div>
                </div>
                <button class="btn btn-secondary btn-sm" onclick="this.parentElement.parentElement.remove(); window.FertiVisionAnalysis.disableAnalysisButton('${analysisType}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Remove existing file info
        const existingFileInfo = uploadContent.querySelector('.file-info');
        if (existingFileInfo) {
            existingFileInfo.remove();
        }

        uploadContent.appendChild(fileInfo);

        // Add image preview if possible
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = document.createElement('img');
                preview.src = e.target.result;
                preview.className = 'image-preview';
                preview.style.cssText = 'max-width: 200px; max-height: 150px; border-radius: 4px; margin-top: 10px;';
                fileInfo.appendChild(preview);
            };
            reader.readAsDataURL(file);
        }
    }

    /**
     * Format file size for display
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Enable analysis button
     */
    enableAnalysisButton(analysisType) {
        const button = document.getElementById(`analyze-${analysisType}-btn`);
        if (button) {
            button.disabled = false;
            button.classList.add('ready');
        }
    }

    /**
     * Disable analysis button
     */
    disableAnalysisButton(analysisType) {
        const button = document.getElementById(`analyze-${analysisType}-btn`);
        if (button) {
            button.disabled = true;
            button.classList.remove('ready');
        }
        this.currentAnalyses.delete(analysisType);
    }

    /**
     * Start analysis process
     */
    async startAnalysis(analysisType) {
        const analysisData = this.currentAnalyses.get(analysisType);
        if (!analysisData) {
            this.showError('Please select an image first', analysisType);
            return;
        }

        const button = document.getElementById(`analyze-${analysisType}-btn`);
        const resultsContainer = document.getElementById(`${analysisType}-results`);

        try {
            // Update button state
            this.setAnalysisState(button, 'analyzing');
            
            // Show progress
            this.showProgress(resultsContainer, analysisType);

            // Get additional options
            const options = this.getAnalysisOptions(analysisType);

            // Perform analysis
            const result = await this.api.analyzeImage(
                analysisData.file,
                analysisType,
                options
            );

            // Update usage stats
            this.api.updateUsageStats(analysisType);

            // Display results
            this.displayResults(resultsContainer, result, analysisType);

            // Store in history
            this.analysisHistory.push({
                ...result,
                analysisType,
                timestamp: new Date().toISOString(),
                options
            });

            // Auto-save if enabled
            if (this.config.getConfig().autoSave) {
                this.saveAnalysisHistory();
            }

        } catch (error) {
            console.error('Analysis failed:', error);
            this.showError(error.message, analysisType);
        } finally {
            this.setAnalysisState(button, 'ready');
        }
    }

    /**
     * Get analysis options from form
     */
    getAnalysisOptions(analysisType) {
        const options = {};

        // Get patient ID
        const patientIdInput = document.getElementById(`${analysisType}-patient-id`);
        if (patientIdInput && patientIdInput.value) {
            options.patientId = patientIdInput.value;
        }

        // Get notes
        const notesInput = document.getElementById(`${analysisType}-notes`);
        if (notesInput && notesInput.value) {
            options.notes = notesInput.value;
        }

        // Analysis-specific options
        if (analysisType === 'embryo') {
            const dayInput = document.getElementById('embryo-day');
            if (dayInput && dayInput.value) {
                options.day = parseInt(dayInput.value);
            }
        }

        return options;
    }

    /**
     * Set analysis button state
     */
    setAnalysisState(button, state) {
        if (!button) return;

        const states = {
            ready: {
                text: '<i class="fas fa-microscope"></i> Analyze with AI',
                disabled: false,
                className: 'btn-primary'
            },
            analyzing: {
                text: '<i class="fas fa-spinner fa-spin"></i> Analyzing...',
                disabled: true,
                className: 'btn-primary analyzing'
            },
            complete: {
                text: '<i class="fas fa-check"></i> Analysis Complete',
                disabled: false,
                className: 'btn-success'
            }
        };

        const stateConfig = states[state] || states.ready;
        button.innerHTML = stateConfig.text;
        button.disabled = stateConfig.disabled;
        button.className = `btn btn-large ${stateConfig.className}`;
    }

    /**
     * Show analysis progress
     */
    showProgress(container, analysisType) {
        container.innerHTML = `
            <div class="analysis-progress">
                <div class="progress-header">
                    <h3><i class="fas fa-microscope"></i> AI Analysis in Progress</h3>
                    <p>Processing ${analysisType} image with advanced AI models...</p>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 0%; animation: progress 3s ease-in-out forwards;"></div>
                </div>
                
                <div class="progress-steps">
                    <div class="step active">
                        <i class="fas fa-upload"></i>
                        <span>Image Upload</span>
                    </div>
                    <div class="step active">
                        <i class="fas fa-cog"></i>
                        <span>AI Processing</span>
                    </div>
                    <div class="step">
                        <i class="fas fa-chart-line"></i>
                        <span>Results</span>
                    </div>
                </div>
            </div>
        `;

        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes progress {
                0% { width: 0%; }
                50% { width: 70%; }
                100% { width: 100%; }
            }
            .progress-steps {
                display: flex;
                justify-content: space-between;
                margin-top: 2rem;
            }
            .step {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.5rem;
                opacity: 0.5;
                transition: opacity 0.3s ease;
            }
            .step.active {
                opacity: 1;
                color: var(--primary-color);
            }
            .step i {
                font-size: 1.5rem;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Display analysis results
     */
    displayResults(container, result, analysisType) {
        const config = this.config.getConfig();
        
        container.innerHTML = `
            <div class="result success fade-in">
                <div class="result-header">
                    <div class="result-icon">
                        ${this.getAnalysisIcon(analysisType)}
                    </div>
                    <div class="result-title">
                        <h3>✅ AI Analysis Complete</h3>
                        <p>Comprehensive ${analysisType} analysis results</p>
                    </div>
                    <div class="result-confidence">
                        <div class="confidence-badge">
                            ${result.confidence || 90}% Confidence
                        </div>
                    </div>
                </div>
                
                <div class="result-classification">
                    <h4>🎯 Classification</h4>
                    <p class="classification-text">${result.classification}</p>
                </div>
                
                <div class="result-analysis">
                    <h4>📋 Detailed Analysis</h4>
                    <p>${result.analysis}</p>
                </div>
                
                ${this.renderTechnicalDetails(result, config.showTechnicalDetails)}
                ${this.renderClinicalRecommendations(result)}
                ${this.renderMetadata(result)}
                
                <div class="result-actions">
                    <button class="btn btn-secondary" onclick="window.FertiVisionAnalysis.exportResult('${analysisType}')">
                        <i class="fas fa-download"></i> Export Report
                    </button>
                    <button class="btn btn-secondary" onclick="window.FertiVisionAnalysis.shareResult('${analysisType}')">
                        <i class="fas fa-share"></i> Share
                    </button>
                    <button class="btn btn-primary" onclick="window.FertiVisionAnalysis.startNewAnalysis('${analysisType}')">
                        <i class="fas fa-plus"></i> New Analysis
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Get analysis icon
     */
    getAnalysisIcon(analysisType) {
        const icons = {
            sperm: '🧬',
            oocyte: '🥚',
            embryo: '👶',
            follicle: '🔬',
            hysteroscopy: '🏥'
        };
        return icons[analysisType] || '🔬';
    }

    /**
     * Render technical details section
     */
    renderTechnicalDetails(result, showDetails) {
        if (!showDetails || !result.technicalDetails) return '';

        const details = Object.entries(result.technicalDetails)
            .map(([key, value]) => `
                <div class="detail-item">
                    <span class="detail-label">${key}:</span>
                    <span class="detail-value">${value}</span>
                </div>
            `).join('');

        return `
            <div class="result-technical">
                <h4>🔬 Technical Parameters</h4>
                <div class="technical-grid">
                    ${details}
                </div>
            </div>
        `;
    }

    /**
     * Render clinical recommendations
     */
    renderClinicalRecommendations(result) {
        if (!result.clinicalRecommendations || !Array.isArray(result.clinicalRecommendations)) {
            return '';
        }

        const recommendations = result.clinicalRecommendations
            .map(rec => `<li>${rec}</li>`)
            .join('');

        return `
            <div class="result-recommendations">
                <h4>💡 Clinical Recommendations</h4>
                <ul class="recommendations-list">
                    ${recommendations}
                </ul>
            </div>
        `;
    }

    /**
     * Render metadata
     */
    renderMetadata(result) {
        return `
            <div class="result-metadata">
                <div class="metadata-item">
                    <i class="fas fa-clock"></i>
                    <span>${new Date(result.timestamp).toLocaleString()}</span>
                </div>
                <div class="metadata-item">
                    <i class="fas fa-robot"></i>
                    <span>${result.provider || 'Demo'} - ${result.model || 'Demo Model'}</span>
                </div>
                ${result.fallback ? '<div class="metadata-item"><i class="fas fa-exclamation-triangle"></i><span>Fallback Mode</span></div>' : ''}
            </div>
        `;
    }

    /**
     * Show error message
     */
    showError(message, analysisType) {
        const container = document.getElementById(`${analysisType}-results`);
        if (!container) return;

        container.innerHTML = `
            <div class="result error">
                <div class="error-content">
                    <i class="fas fa-exclamation-triangle error-icon"></i>
                    <h3>Analysis Error</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="window.FertiVisionAnalysis.startNewAnalysis('${analysisType}')">
                        Try Again
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Start new analysis
     */
    startNewAnalysis(analysisType) {
        // Clear current analysis
        this.currentAnalyses.delete(analysisType);
        
        // Reset file input
        const fileInput = document.getElementById(`${analysisType}-file`);
        if (fileInput) {
            fileInput.value = '';
        }
        
        // Reset upload area
        const uploadArea = document.querySelector(`#${analysisType}-upload .upload-content`);
        if (uploadArea) {
            const fileInfo = uploadArea.querySelector('.file-info');
            if (fileInfo) {
                fileInfo.remove();
            }
        }
        
        // Reset results
        const resultsContainer = document.getElementById(`${analysisType}-results`);
        if (resultsContainer) {
            resultsContainer.innerHTML = `
                <div class="placeholder-content">
                    <i class="fas fa-chart-line placeholder-icon"></i>
                    <h3>Analysis Results</h3>
                    <p>Upload an image to see detailed analysis results</p>
                </div>
            `;
        }
        
        // Disable button
        this.disableAnalysisButton(analysisType);
    }

    /**
     * Export analysis result
     */
    exportResult(analysisType) {
        const lastResult = this.analysisHistory
            .filter(h => h.analysisType === analysisType)
            .pop();
            
        if (!lastResult) return;

        const exportData = {
            ...lastResult,
            exportedAt: new Date().toISOString(),
            application: 'FertiVision'
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `fertivision-${analysisType}-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Share analysis result
     */
    shareResult(analysisType) {
        const lastResult = this.analysisHistory
            .filter(h => h.analysisType === analysisType)
            .pop();
            
        if (!lastResult) return;

        const shareText = `FertiVision ${analysisType} analysis: ${lastResult.classification}`;
        
        if (navigator.share) {
            navigator.share({
                title: 'FertiVision Analysis Result',
                text: shareText,
                url: window.location.href
            });
        } else {
            // Fallback to clipboard
            navigator.clipboard.writeText(shareText).then(() => {
                alert('Analysis result copied to clipboard!');
            });
        }
    }

    /**
     * Save analysis history
     */
    saveAnalysisHistory() {
        try {
            localStorage.setItem('fertivision-analysis-history', 
                JSON.stringify(this.analysisHistory.slice(-50)) // Keep last 50
            );
        } catch (error) {
            console.warn('Failed to save analysis history:', error);
        }
    }

    /**
     * Load analysis history
     */
    loadAnalysisHistory() {
        try {
            const saved = localStorage.getItem('fertivision-analysis-history');
            if (saved) {
                this.analysisHistory = JSON.parse(saved);
            }
        } catch (error) {
            console.warn('Failed to load analysis history:', error);
        }
    }
}

// Initialize global analysis instance
window.FertiVisionAnalysis = new FertiVisionAnalysis();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FertiVisionAnalysis;
}
