/**
 * FertiVision Demo Module
 * Handles interactive demos and sample data
 */

class FertiVisionDemos {
    constructor() {
        this.config = window.FertiVisionConfig;
        this.demoData = this.initializeDemoData();
        this.initializeEventListeners();
    }

    /**
     * Initialize demo event listeners
     */
    initializeEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('demo-btn')) {
                const demoType = e.target.getAttribute('data-demo');
                this.runDemo(demoType);
            }
        });
    }

    /**
     * Initialize comprehensive demo data
     */
    initializeDemoData() {
        return {
            follicle: {
                title: '🔬 Follicle Counting Analysis',
                subtitle: 'Automated AFC and Ovarian Reserve Assessment',
                result: {
                    classification: 'Normal Ovarian Reserve',
                    confidence: 94.8,
                    analysis: 'Comprehensive follicle analysis demonstrates normal ovarian reserve with excellent reproductive potential. The antral follicle count of 12 indicates optimal ovarian function for reproductive age.',
                    technicalDetails: {
                        'Total Follicle Count': '12 follicles',
                        'Antral Follicle Count (AFC)': '8 follicles (2-10mm)',
                        'Dominant Follicle': '16.5mm (pre-ovulatory)',
                        'Small Follicles': '4 follicles (<2mm)',
                        'Ovarian Volume': '8.5ml (normal)',
                        'Stromal Echogenicity': 'Normal pattern',
                        'Blood Flow': 'Normal vascularization'
                    },
                    clinicalRecommendations: [
                        'Normal ovarian reserve - excellent fertility potential',
                        'Optimal candidate for natural conception or IVF',
                        'Expected good response to ovarian stimulation',
                        'Consider ovulation monitoring for timed intercourse',
                        'AMH correlation suggested for complete assessment'
                    ],
                    parameters: {
                        total_follicles: 12,
                        afc: 8,
                        dominant_size: 16.5,
                        ovarian_volume: 8.5
                    }
                }
            },
            sperm: {
                title: '🧬 Sperm Analysis Demo',
                subtitle: 'WHO 2021 Compliant Morphology Assessment',
                result: {
                    classification: 'Normozoospermia',
                    confidence: 96.3,
                    analysis: 'Comprehensive semen analysis demonstrates excellent reproductive potential with all parameters exceeding WHO 2021 reference values. The sample shows optimal concentration, motility, and morphology characteristics.',
                    technicalDetails: {
                        'Concentration': '45.0 × 10⁶/ml (Ref: >15)',
                        'Progressive Motility': '65% (Ref: >32%)',
                        'Total Motility': '78% (Ref: >40%)',
                        'Normal Morphology': '8% (Ref: >4%)',
                        'Volume': '3.0ml (Ref: >1.5ml)',
                        'pH': '7.8 (Ref: 7.2-8.0)',
                        'Vitality': '85% (Ref: >58%)',
                        'Leukocytes': '<1 × 10⁶/ml (Normal)'
                    },
                    clinicalRecommendations: [
                        'Excellent fertility potential - natural conception highly likely',
                        'Suitable for all assisted reproductive techniques',
                        'No immediate treatment or intervention required',
                        'Maintain healthy lifestyle and nutrition',
                        'Consider partner evaluation if conception delayed'
                    ],
                    parameters: {
                        concentration: 45.0,
                        progressive_motility: 65.0,
                        normal_morphology: 8.0,
                        volume: 3.0
                    }
                }
            },
            embryo: {
                title: '👶 Embryo Grading Demo',
                subtitle: 'Gardner Grading System Evaluation',
                result: {
                    classification: 'Grade A Embryo - Excellent Quality',
                    confidence: 97.1,
                    analysis: 'Outstanding embryo quality with optimal developmental progression and minimal fragmentation. This Day 3 embryo demonstrates excellent cellular organization and high implantation potential.',
                    technicalDetails: {
                        'Development Day': 'Day 3 (72 hours post-fertilization)',
                        'Cell Count': '8 cells (optimal for Day 3)',
                        'Fragmentation': '<5% (minimal)',
                        'Cell Symmetry': '95% (excellent)',
                        'Cytoplasmic Appearance': 'Clear and uniform',
                        'Zona Pellucida': 'Normal thickness',
                        'Grade': 'A (excellent quality)',
                        'Implantation Potential': 'High (>60%)'
                    },
                    clinicalRecommendations: [
                        'Excellent candidate for fresh embryo transfer',
                        'High probability of successful implantation',
                        'Consider single embryo transfer to reduce multiple pregnancy risk',
                        'Suitable for cryopreservation if transfer delayed',
                        'Expected continued normal development to blastocyst stage'
                    ],
                    parameters: {
                        day: 3,
                        cell_count: 8,
                        fragmentation: 5.0,
                        grade: 'A'
                    }
                }
            },
            oocyte: {
                title: '🥚 Oocyte Analysis Demo',
                subtitle: 'ESHRE Guidelines Maturity Assessment',
                result: {
                    classification: 'Metaphase II (MII) - Mature Oocyte',
                    confidence: 93.7,
                    analysis: 'Oocyte demonstrates optimal maturity with clear morphological indicators of fertilization competence. The presence of the first polar body and clear cytoplasm indicate readiness for ICSI procedure.',
                    technicalDetails: {
                        'Maturity Stage': 'Metaphase II (MII)',
                        'Morphology Score': '8.5/10 (Excellent)',
                        'Polar Body': 'Present and normal morphology',
                        'Cytoplasm': 'Clear and homogeneous',
                        'Zona Pellucida': 'Normal thickness and clarity',
                        'Perivitelline Space': 'Normal size',
                        'Cumulus Cells': 'Appropriately expanded',
                        'Overall Quality': 'Grade 1 (Excellent)'
                    },
                    clinicalRecommendations: [
                        'Excellent candidate for ICSI fertilization',
                        'High probability of successful fertilization (>80%)',
                        'Optimal timing for sperm injection',
                        'Expected good embryo development potential',
                        'Consider immediate ICSI procedure'
                    ],
                    parameters: {
                        maturity: 'MII',
                        morphology_score: 8.5,
                        polar_body: 'Present',
                        cytoplasm: 'Clear'
                    }
                }
            },
            hysteroscopy: {
                title: '🏥 Hysteroscopy Analysis Demo',
                subtitle: 'Endometrial Morphology Assessment',
                result: {
                    classification: 'Normal Hysteroscopy - Healthy Endometrium',
                    confidence: 91.4,
                    analysis: 'Hysteroscopic examination reveals normal uterine cavity with healthy endometrial morphology. The endometrial thickness and pattern are appropriate for the menstrual cycle phase.',
                    technicalDetails: {
                        'Uterine Cavity': 'Normal triangular shape',
                        'Endometrial Thickness': '8.5mm (normal for cycle phase)',
                        'Endometrial Pattern': 'Proliferative (appropriate)',
                        'Cervical Canal': 'Normal appearance',
                        'Tubal Ostia': 'Bilateral patent',
                        'Pathological Findings': 'None detected',
                        'Vascularization': 'Normal pattern',
                        'Overall Assessment': 'Normal findings'
                    },
                    clinicalRecommendations: [
                        'Normal uterine cavity - no intervention required',
                        'Endometrial receptivity appears optimal',
                        'No contraindications for embryo transfer',
                        'Continue with planned fertility treatment',
                        'Routine follow-up as per protocol'
                    ],
                    parameters: {
                        endometrial_thickness: 8.5,
                        findings: 'Normal',
                        classification: 'Normal'
                    }
                }
            }
        };
    }

    /**
     * Run interactive demo
     */
    async runDemo(demoType) {
        const demoInfo = this.demoData[demoType];
        if (!demoInfo) {
            console.error('Demo type not found:', demoType);
            return;
        }

        const resultsContainer = document.getElementById('demo-results');
        if (!resultsContainer) {
            console.error('Demo results container not found');
            return;
        }

        // Show loading state
        this.showDemoLoading(resultsContainer, demoInfo);

        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2500));

        // Display demo results
        this.displayDemoResults(resultsContainer, demoInfo);

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Show demo loading state
     */
    showDemoLoading(container, demoInfo) {
        container.innerHTML = `
            <div class="demo-loading">
                <div class="demo-header">
                    <h2>${demoInfo.title}</h2>
                    <p>${demoInfo.subtitle}</p>
                </div>
                
                <div class="loading-animation">
                    <div class="loading-spinner"></div>
                    <p>Running AI analysis demo...</p>
                </div>
                
                <div class="demo-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="animation: demoProgress 2.5s ease-in-out forwards;"></div>
                    </div>
                    <div class="progress-text">Processing medical image with advanced AI models</div>
                </div>
            </div>
        `;

        // Add demo-specific CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes demoProgress {
                0% { width: 0%; }
                30% { width: 40%; }
                70% { width: 85%; }
                100% { width: 100%; }
            }
            .demo-loading {
                background: var(--bg-primary);
                border-radius: var(--border-radius);
                padding: 3rem;
                text-align: center;
                box-shadow: var(--shadow-lg);
                margin-top: 2rem;
            }
            .demo-header h2 {
                color: var(--primary-color);
                margin-bottom: 0.5rem;
                font-size: 1.8rem;
            }
            .demo-header p {
                color: var(--text-secondary);
                margin-bottom: 2rem;
            }
            .loading-animation {
                margin: 2rem 0;
            }
            .loading-animation p {
                margin-top: 1rem;
                color: var(--text-secondary);
            }
            .demo-progress {
                margin-top: 2rem;
            }
            .progress-text {
                margin-top: 1rem;
                color: var(--text-secondary);
                font-size: 0.9rem;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Display demo results
     */
    displayDemoResults(container, demoInfo) {
        const result = demoInfo.result;
        
        container.innerHTML = `
            <div class="demo-result fade-in">
                <div class="demo-result-header">
                    <div class="result-badge">
                        <span class="badge-icon">✨</span>
                        <span class="badge-text">AI Demo Analysis</span>
                    </div>
                    <h2>${demoInfo.title}</h2>
                    <p class="demo-subtitle">${demoInfo.subtitle}</p>
                </div>
                
                <div class="result-summary">
                    <div class="summary-card classification">
                        <div class="card-icon">🎯</div>
                        <div class="card-content">
                            <h3>Classification</h3>
                            <p class="classification-result">${result.classification}</p>
                        </div>
                        <div class="confidence-indicator">
                            <div class="confidence-circle">
                                <span>${result.confidence}%</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="result-analysis-section">
                    <h3><i class="fas fa-microscope"></i> Detailed Analysis</h3>
                    <div class="analysis-content">
                        <p>${result.analysis}</p>
                    </div>
                </div>
                
                <div class="result-technical-section">
                    <h3><i class="fas fa-chart-bar"></i> Technical Parameters</h3>
                    <div class="technical-parameters">
                        ${this.renderTechnicalParameters(result.technicalDetails)}
                    </div>
                </div>
                
                <div class="result-recommendations-section">
                    <h3><i class="fas fa-lightbulb"></i> Clinical Recommendations</h3>
                    <div class="recommendations-grid">
                        ${this.renderRecommendations(result.clinicalRecommendations)}
                    </div>
                </div>
                
                <div class="demo-actions">
                    <button class="btn btn-primary" onclick="window.FertiVisionDemos.exportDemoReport('${demoInfo.title}')">
                        <i class="fas fa-download"></i> Export Demo Report
                    </button>
                    <button class="btn btn-secondary" onclick="window.FertiVisionDemos.runRandomDemo()">
                        <i class="fas fa-random"></i> Try Another Demo
                    </button>
                    <button class="btn btn-secondary" onclick="window.FertiVisionDemos.clearDemoResults()">
                        <i class="fas fa-times"></i> Clear Results
                    </button>
                </div>
                
                <div class="demo-metadata">
                    <div class="metadata-grid">
                        <div class="metadata-item">
                            <i class="fas fa-robot"></i>
                            <span>AI Model: Demo Analysis Engine</span>
                        </div>
                        <div class="metadata-item">
                            <i class="fas fa-clock"></i>
                            <span>Generated: ${new Date().toLocaleString()}</span>
                        </div>
                        <div class="metadata-item">
                            <i class="fas fa-shield-alt"></i>
                            <span>Confidence: ${result.confidence}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add result-specific styling
        this.addDemoResultStyling();
    }

    /**
     * Render technical parameters
     */
    renderTechnicalParameters(technicalDetails) {
        return Object.entries(technicalDetails)
            .map(([key, value]) => `
                <div class="parameter-item">
                    <div class="parameter-label">${key}</div>
                    <div class="parameter-value">${value}</div>
                </div>
            `).join('');
    }

    /**
     * Render clinical recommendations
     */
    renderRecommendations(recommendations) {
        return recommendations
            .map((rec, index) => `
                <div class="recommendation-item">
                    <div class="rec-number">${index + 1}</div>
                    <div class="rec-content">${rec}</div>
                </div>
            `).join('');
    }

    /**
     * Add demo result styling
     */
    addDemoResultStyling() {
        if (document.getElementById('demo-result-styles')) return;

        const style = document.createElement('style');
        style.id = 'demo-result-styles';
        style.textContent = `
            .demo-result {
                background: var(--bg-primary);
                border-radius: var(--border-radius);
                padding: 2rem;
                margin-top: 2rem;
                box-shadow: var(--shadow-lg);
                border: 1px solid var(--border-color);
            }
            
            .demo-result-header {
                text-align: center;
                margin-bottom: 2rem;
                padding-bottom: 1.5rem;
                border-bottom: 1px solid var(--border-color);
            }
            
            .result-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: linear-gradient(135deg, var(--primary-color), var(--success-color));
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 500;
                margin-bottom: 1rem;
            }
            
            .demo-result-header h2 {
                color: var(--primary-color);
                margin-bottom: 0.5rem;
                font-size: 1.8rem;
            }
            
            .demo-subtitle {
                color: var(--text-secondary);
                font-size: 1rem;
            }
            
            .result-summary {
                margin-bottom: 2rem;
            }
            
            .summary-card {
                display: flex;
                align-items: center;
                gap: 1.5rem;
                background: var(--bg-secondary);
                padding: 1.5rem;
                border-radius: var(--border-radius);
                border-left: 4px solid var(--success-color);
            }
            
            .card-icon {
                font-size: 2.5rem;
            }
            
            .card-content h3 {
                color: var(--primary-color);
                margin-bottom: 0.5rem;
                font-size: 1.1rem;
            }
            
            .classification-result {
                font-size: 1.2rem;
                font-weight: 600;
                color: var(--success-color);
            }
            
            .confidence-circle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--success-color), var(--primary-color));
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 600;
                font-size: 0.9rem;
            }
            
            .result-analysis-section,
            .result-technical-section,
            .result-recommendations-section {
                margin-bottom: 2rem;
            }
            
            .result-analysis-section h3,
            .result-technical-section h3,
            .result-recommendations-section h3 {
                color: var(--primary-color);
                margin-bottom: 1rem;
                font-size: 1.2rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .analysis-content {
                background: var(--bg-secondary);
                padding: 1.5rem;
                border-radius: var(--border-radius);
                border-left: 4px solid var(--primary-color);
            }
            
            .technical-parameters {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1rem;
            }
            
            .parameter-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem;
                background: var(--bg-secondary);
                border-radius: var(--border-radius);
                border: 1px solid var(--border-color);
            }
            
            .parameter-label {
                font-weight: 500;
                color: var(--text-primary);
            }
            
            .parameter-value {
                font-weight: 600;
                color: var(--primary-color);
            }
            
            .recommendations-grid {
                display: grid;
                gap: 1rem;
            }
            
            .recommendation-item {
                display: flex;
                gap: 1rem;
                padding: 1rem;
                background: var(--bg-secondary);
                border-radius: var(--border-radius);
                border-left: 4px solid var(--success-color);
            }
            
            .rec-number {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: var(--success-color);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                font-size: 0.9rem;
                flex-shrink: 0;
            }
            
            .rec-content {
                flex: 1;
                color: var(--text-primary);
            }
            
            .demo-actions {
                display: flex;
                gap: 1rem;
                justify-content: center;
                margin: 2rem 0;
                flex-wrap: wrap;
            }
            
            .demo-metadata {
                margin-top: 2rem;
                padding-top: 1.5rem;
                border-top: 1px solid var(--border-color);
            }
            
            .metadata-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
            }
            
            .metadata-item {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: var(--text-secondary);
                font-size: 0.9rem;
            }
            
            @media (max-width: 768px) {
                .summary-card {
                    flex-direction: column;
                    text-align: center;
                }
                
                .technical-parameters {
                    grid-template-columns: 1fr;
                }
                
                .demo-actions {
                    flex-direction: column;
                }
                
                .metadata-grid {
                    grid-template-columns: 1fr;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Run random demo
     */
    runRandomDemo() {
        const demoTypes = Object.keys(this.demoData);
        const randomType = demoTypes[Math.floor(Math.random() * demoTypes.length)];
        this.runDemo(randomType);
    }

    /**
     * Clear demo results
     */
    clearDemoResults() {
        const resultsContainer = document.getElementById('demo-results');
        if (resultsContainer) {
            resultsContainer.innerHTML = `
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
     * Export demo report
     */
    exportDemoReport(title) {
        const timestamp = new Date().toISOString();
        const reportData = {
            title: title,
            type: 'Demo Report',
            generated: timestamp,
            application: 'FertiVision',
            version: '1.0.0',
            note: 'This is a demonstration report generated by FertiVision AI analysis system.'
        };

        const blob = new Blob([JSON.stringify(reportData, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `fertivision-demo-${timestamp.split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Download sample image
     */
    downloadSampleImage(imageType) {
        // Create a simple colored rectangle as sample image
        const canvas = document.createElement('canvas');
        canvas.width = 800;
        canvas.height = 600;
        const ctx = canvas.getContext('2d');
        
        // Set background color based on image type
        const colors = {
            sperm: '#e6f3ff',
            oocyte: '#fff0e6',
            embryo: '#f0ffe6',
            follicle: '#ffe6f3',
            hysteroscopy: '#f3e6ff'
        };
        
        ctx.fillStyle = colors[imageType] || '#f0f0f0';
        ctx.fillRect(0, 0, 800, 600);
        
        // Add sample text
        ctx.fillStyle = '#333';
        ctx.font = '24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`Sample ${imageType.charAt(0).toUpperCase() + imageType.slice(1)} Image`, 400, 300);
        ctx.font = '16px Arial';
        ctx.fillText('For FertiVision AI Analysis Testing', 400, 330);
        
        // Convert to blob and download
        canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `sample-${imageType}-image.png`;
            a.click();
            URL.revokeObjectURL(url);
        });
    }
}

// Initialize global demos instance
window.FertiVisionDemos = new FertiVisionDemos();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FertiVisionDemos;
}
