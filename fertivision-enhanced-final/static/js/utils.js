// Utility JS for FertiVision-CodeLM

function showTab(tabId, btn) {
    // Remove active class from all tabs and buttons
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    // Add active class to selected tab and button
    const tab = document.getElementById(tabId);
    if (tab) {
        tab.classList.add('active');
    } else {
        console.error('Tab not found:', tabId);
    }
    
    if (btn) {
        btn.classList.add('active');
    }
}

function handleFormSubmit(event, tabId) {
    event.preventDefault();
    const barContainer = document.getElementById('progress-bar-container');
    const bar = document.getElementById('progress-bar');
    const label = document.getElementById('progress-label');
    
    if (!barContainer || !bar || !label) {
        console.error('Progress bar elements not found');
        return false;
    }
    
    barContainer.style.display = 'block';
    bar.style.width = '0%';
    label.textContent = 'Processing...';
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress >= 100) {
            progress = 100;
            label.textContent = 'Analysis complete! Draft report generated below.';
            clearInterval(interval);
            setTimeout(() => {
                barContainer.style.display = 'none';
                showAIReport();
            }, 1200);
        }
        bar.style.width = progress + '%';
    }, 300);
    
    // Actually submit the form after a short delay to simulate processing
    setTimeout(() => {
        event.target.submit();
    }, 1800);
    
    return false;
}

function showAIReport() {
    const formatSelect = document.getElementById('report-format');
    const format = formatSelect ? formatSelect.value : 'summary';
    let reportText = '';
    
    if (format === 'summary') {
        reportText = 'AI Summary: The submitted image shows normal morphology and motility patterns. No significant abnormalities detected.';
    } else if (format === 'detailed') {
        reportText = 'AI Detailed Report:\n- Morphology: Normal sperm morphology observed\n- Motility: 85% progressive motility\n- Concentration: 60 million/ml\n- Volume: Normal\n- No significant abnormalities detected.\n\nRecommendation: Results within normal parameters.';
    } else {
        reportText = 'Clinical Draft Report:\n\nPlease review the AI findings and edit as needed for your clinical report.\n\nThe automated analysis indicates normal parameters. Manual verification recommended before finalizing clinical assessment.';
    }
    
    const reportTextarea = document.getElementById('ai-report');
    const reportSection = document.getElementById('report-section');
    
    if (reportTextarea && reportSection) {
        reportTextarea.value = reportText;
        reportSection.style.display = 'block';
    } else {
        console.error('Report elements not found');
    }
}

function finalizeReport() {
    const reportTextarea = document.getElementById('ai-report');
    const finalReportContent = document.getElementById('final-report-content');
    const finalReport = document.getElementById('final-report');
    
    if (reportTextarea && finalReportContent && finalReport) {
        const report = reportTextarea.value;
        finalReportContent.textContent = report;
        finalReport.style.display = 'block';
        
        // Scroll to the final report
        finalReport.scrollIntoView({ behavior: 'smooth' });
    } else {
        console.error('Final report elements not found');
    }
}

function showProgress() {
    // Show progress bar
    const barContainer = document.getElementById('progress-bar-container');
    if (barContainer) {
        barContainer.style.display = 'block';
    }
}
