#!/bin/zsh

# Script to toggle between Mock and DeepSeek modes for FertiVision-CodeLM

echo "🔄 FertiVision Analysis Mode Toggler"
echo "======================================"

# Use grep to detect current mode in config.py
current_mode=$(grep -A 1 "ANALYSIS_MODE" /Users/spr/fertivisiion\ codelm/config.py | grep -o "MOCK\|DEEPSEEK" | head -1)

if [ "$current_mode" = "MOCK" ]; then
    echo "📊 Current mode: MOCK (using simulated data)"
    echo "🔄 Switching to DEEPSEEK mode (AI-powered analysis)..."
    
    # Check if Ollama is running
    if ! pgrep -x "ollama" > /dev/null; then
        echo "⚠️  Ollama is not running. Starting Ollama service..."
        ollama serve &
        sleep 3
    fi
    
    # Check if DeepSeek model is available
    if ! ollama list | grep -q "deepseek-coder"; then
        echo "⚠️  DeepSeek model not found. Installing..."
        ollama pull deepseek-coder
    fi
    
    # Replace MOCK with DEEPSEEK in config.py
    sed -i '' 's/ANALYSIS_MODE = AnalysisMode.MOCK/ANALYSIS_MODE = AnalysisMode.DEEPSEEK/g' /Users/spr/fertivisiion\ codelm/config.py
    echo "✅ Switched to DEEPSEEK mode successfully!"
    
else
    echo "🤖 Current mode: DEEPSEEK (AI-powered analysis)"
    echo "🔄 Switching to MOCK mode (using simulated data)..."
    
    # Replace DEEPSEEK with MOCK in config.py
    sed -i '' 's/ANALYSIS_MODE = AnalysisMode.DEEPSEEK/ANALYSIS_MODE = AnalysisMode.MOCK/g' /Users/spr/fertivisiion\ codelm/config.py
    echo "✅ Switched to MOCK mode successfully!"
fi

echo ""
echo "📝 NOTE: Restart the Flask application for changes to take effect"
echo "Run: python app.py"
