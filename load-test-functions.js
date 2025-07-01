// Load test helper functions for Artillery.js

// Simulate image upload for testing
function uploadTestImage(requestParams, context, ee, next) {
    // In a real scenario, you would use actual test images
    // For load testing, we'll use a small test file
    
    const testImageData = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1BMVEUAAACnej3aAAAAAWJLR0QAiAUdSAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9wKExQZLWTEaOUAAAAddEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIFRoZSBHSU1Q72QlbgAAAA1JREFUCB1jYGBgYAAAAAUAAY27m/MAAAAASUVORK5CYII=', 'base64');
    
    // Add form data for file upload
    requestParams.formData = {
        ...requestParams.form,
        image: {
            value: testImageData,
            options: {
                filename: 'test-image.png',
                contentType: 'image/png'
            }
        }
    };
    
    // Remove the form property since we're using formData
    delete requestParams.form;
    
    return next();
}

// Generate random patient data
function generatePatientData(requestParams, context, ee, next) {
    const firstNames = ['Alice', 'Bob', 'Carol', 'David', 'Emma', 'Frank', 'Grace', 'Henry'];
    const lastNames = ['Johnson', 'Smith', 'Brown', 'Wilson', 'Davis', 'Miller', 'Taylor', 'Anderson'];
    
    context.vars.patient_name = `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`;
    context.vars.age = Math.floor(Math.random() * 25) + 20; // Age between 20-45
    
    return next();
}

// Validate response structure
function validateAnalysisResponse(requestParams, response, context, ee, next) {
    if (response.statusCode === 200) {
        try {
            const body = JSON.parse(response.body);
            
            // Check if response contains expected fields
            if (body.analysis_id || body.sample_report) {
                ee.emit('counter', 'analysis.success', 1);
            } else {
                ee.emit('counter', 'analysis.invalid_response', 1);
            }
            
            // Track analysis processing time if provided
            if (body.processing_time) {
                ee.emit('histogram', 'analysis.processing_time', body.processing_time);
            }
            
        } catch {
            ee.emit('counter', 'analysis.parse_error', 1);
        }
    } else {
        ee.emit('counter', `analysis.http_${response.statusCode}`, 1);
    }
    
    return next();
}

// Track custom metrics
function trackMetrics(requestParams, response, context, ee, next) {
    // Track response times by endpoint
    const endpoint = requestParams.url;
    const responseTime = response.timings ? response.timings.response : 0;
    
    ee.emit('histogram', `response_time.${endpoint.replace(/[^a-zA-Z0-9]/g, '_')}`, responseTime);
    
    // Track success/error rates
    if (response.statusCode >= 200 && response.statusCode < 300) {
        ee.emit('counter', 'requests.success', 1);
    } else {
        ee.emit('counter', 'requests.error', 1);
        ee.emit('counter', `http_${response.statusCode}`, 1);
    }
    
    return next();
}

// Simulate realistic user behavior
function simulateUserBehavior(context, events, done) {
    // Add random delays to simulate real user interaction
    const thinkTime = Math.random() * 2000 + 500; // 0.5-2.5 seconds
    
    setTimeout(() => {
        done();
    }, thinkTime);
}

// Memory and performance monitoring
function monitorPerformance(requestParams, response, context, ee, next) {
    // Track memory usage if response includes it
    if (response.headers['x-memory-usage']) {
        ee.emit('histogram', 'server.memory_usage', parseInt(response.headers['x-memory-usage']));
    }
    
    // Track CPU usage if response includes it
    if (response.headers['x-cpu-usage']) {
        ee.emit('histogram', 'server.cpu_usage', parseFloat(response.headers['x-cpu-usage']));
    }
    
    return next();
}

// Export functions for Artillery
module.exports = {
    uploadTestImage,
    generatePatientData,
    validateAnalysisResponse,
    trackMetrics,
    simulateUserBehavior,
    monitorPerformance
};
