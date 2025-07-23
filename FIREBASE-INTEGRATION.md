# Firebase Analytics Integration for FertiVision

## Configuration Added

Firebase Analytics has been integrated into the FertiVision application with the following components:

### 1. Firebase Configuration File
- **Location**: `static/js/firebase-config.js`
- **Purpose**: Initialize Firebase Analytics and provide custom tracking functions
- **Project**: `ovul-ind` (Ovulation Indicator)

### 2. Custom Analytics Events

The Firebase configuration includes three custom event tracking functions:

#### `trackAnalysis(analysisType)`
- Tracks when fertility analysis is performed
- Parameters:
  - `analysis_type`: Type of analysis performed
  - `timestamp`: Analysis timestamp

#### `trackUpload(fileType)`
- Tracks image uploads to the system
- Parameters:
  - `file_type`: Type of uploaded file
  - `timestamp`: Upload timestamp

#### `trackReport(reportType)`
- Tracks report generation events
- Parameters:
  - `report_type`: Type of report generated
  - `timestamp`: Generation timestamp

### 3. Integration Points

To integrate Firebase Analytics into your Flask templates:

1. **Add Firebase SDK to HTML templates**:
```html
<!-- Add to your base template -->
<script type="module" src="{{ url_for('static', filename='js/firebase-config.js') }}"></script>
```

2. **Track events in JavaScript**:
```javascript
import { trackAnalysis, trackUpload, trackReport } from './firebase-config.js';

// Example usage
trackAnalysis('sperm_morphology');
trackUpload('microscopy_image');
trackReport('detailed_analysis');
```

### 4. Production Benefits

Firebase Analytics will provide:
- Real-time user engagement metrics
- Analysis usage patterns
- Performance monitoring
- Error tracking
- User journey analytics

### 5. Privacy Considerations

The current configuration tracks:
- Analysis types and frequencies
- Upload patterns
- Report generation metrics
- Timestamps for user actions

No personal health information or image content is tracked.

### 6. Next Steps

1. **Deploy to Cloud Run**: Firebase will automatically start collecting data
2. **Monitor Dashboard**: Check Firebase Console for analytics data
3. **Custom Reports**: Create custom reports based on fertility analysis patterns
4. **Performance Tracking**: Use data to optimize user experience

## Firebase Console Access

- **Project ID**: `ovul-ind`
- **Console URL**: https://console.firebase.google.com/project/ovul-ind
- **Analytics Dashboard**: Available after deployment and user interactions

This integration enhances your FertiVision deployment with comprehensive analytics capabilities for monitoring user engagement and system performance in production.
