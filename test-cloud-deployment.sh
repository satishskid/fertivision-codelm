#!/bin/bash
# Cloud Run Deployment Test Script

echo "🧪 FertiVision Cloud Run Deployment Testing"
echo "==========================================="

# Get the Cloud Run URL
SERVICE_URL=$(gcloud run services describe fertivision --region=us-central1 --format="value(status.url)")

if [ -z "$SERVICE_URL" ]; then
    echo "❌ Error: Could not get service URL. Make sure the service is deployed."
    exit 1
fi

echo "🌐 Testing service at: $SERVICE_URL"
echo ""

# Test 1: Health Check
echo "🏥 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/health_response.json "$SERVICE_URL/health")
HEALTH_CODE="${HEALTH_RESPONSE: -3}"

if [ "$HEALTH_CODE" = "200" ]; then
    echo "✅ Health check passed"
    cat /tmp/health_response.json | python -m json.tool
else
    echo "❌ Health check failed with code: $HEALTH_CODE"
    cat /tmp/health_response.json
fi
echo ""

# Test 2: Readiness Check
echo "🚀 Testing readiness endpoint..."
READY_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/ready_response.json "$SERVICE_URL/ready")
READY_CODE="${READY_RESPONSE: -3}"

if [ "$READY_CODE" = "200" ]; then
    echo "✅ Readiness check passed"
    cat /tmp/ready_response.json | python -m json.tool
else
    echo "❌ Readiness check failed with code: $READY_CODE"
    cat /tmp/ready_response.json
fi
echo ""

# Test 3: Main Application (requires auth)
echo "🔒 Testing main application (will show auth requirement)..."
MAIN_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/main_response.html "$SERVICE_URL/")
MAIN_CODE="${MAIN_RESPONSE: -3}"

if [ "$MAIN_CODE" = "401" ] || [ "$MAIN_CODE" = "403" ]; then
    echo "✅ Main app properly requires authentication (code: $MAIN_CODE)"
elif [ "$MAIN_CODE" = "200" ]; then
    echo "✅ Main app accessible (code: $MAIN_CODE)"
else
    echo "❌ Main app returned unexpected code: $MAIN_CODE"
fi
echo ""

# Test 4: Performance Test
echo "⚡ Running performance test..."
echo "Testing response time..."
TIME_START=$(date +%s%3N)
curl -s "$SERVICE_URL/health" > /dev/null
TIME_END=$(date +%s%3N)
RESPONSE_TIME=$((TIME_END - TIME_START))

echo "Response time: ${RESPONSE_TIME}ms"
if [ $RESPONSE_TIME -lt 1000 ]; then
    echo "✅ Good response time"
elif [ $RESPONSE_TIME -lt 3000 ]; then
    echo "⚠️ Acceptable response time"
else
    echo "❌ Slow response time"
fi
echo ""

# Clean up temp files
rm -f /tmp/health_response.json /tmp/ready_response.json /tmp/main_response.html

echo "🎯 Deployment Test Summary:"
echo "=========================="
echo "Service URL: $SERVICE_URL"
echo "Health Check: $([ "$HEALTH_CODE" = "200" ] && echo "✅ PASS" || echo "❌ FAIL")"
echo "Readiness: $([ "$READY_CODE" = "200" ] && echo "✅ PASS" || echo "❌ FAIL")"
echo "Auth Protection: $([ "$MAIN_CODE" = "401" ] || [ "$MAIN_CODE" = "403" ] && echo "✅ PASS" || echo "❌ FAIL")"
echo "Response Time: ${RESPONSE_TIME}ms"
echo ""

if [ "$HEALTH_CODE" = "200" ] && [ "$READY_CODE" = "200" ]; then
    echo "🎉 Deployment successful! Your app is ready for use."
    echo "🌐 Access your app at: $SERVICE_URL"
    echo ""
    echo "🔍 Monitoring commands:"
    echo "Live logs: gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=fertivision'"
    echo "Service info: gcloud run services describe fertivision --region=us-central1"
else
    echo "❌ Deployment has issues. Check the logs:"
    echo "gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=fertivision AND severity>=ERROR' --limit=10"
fi
