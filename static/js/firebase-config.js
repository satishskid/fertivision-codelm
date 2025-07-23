// Firebase Analytics Configuration for FertiVision
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCMNyB4HI8XKBMxcboKQE8MUAtBIHOduuk",
  authDomain: "ovul-ind.firebaseapp.com",
  projectId: "ovul-ind",
  storageBucket: "ovul-ind.firebasestorage.app",
  messagingSenderId: "105145457421",
  appId: "1:105145457421:web:466b5d794be5daaef66e44",
  measurementId: "G-GZN6GT58CM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Custom analytics events for FertiVision
export const trackAnalysis = (analysisType) => {
  analytics.logEvent('fertility_analysis', {
    analysis_type: analysisType,
    timestamp: new Date().toISOString()
  });
};

export const trackUpload = (fileType) => {
  analytics.logEvent('image_upload', {
    file_type: fileType,
    timestamp: new Date().toISOString()
  });
};

export const trackReport = (reportType) => {
  analytics.logEvent('report_generation', {
    report_type: reportType,
    timestamp: new Date().toISOString()
  });
};

export { analytics };
