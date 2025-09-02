#!/bin/bash

echo "🧪 Testing Angular build locally..."

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: frontend/package.json not found. Are you in the right directory?"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"

# Go to frontend directory
cd frontend

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building Angular app..."
npm run build

echo "📁 Checking build output..."
if [ -d "dist/ai-research-assistant-frontend" ]; then
    echo "✅ Build successful! Frontend files found in dist/ai-research-assistant-frontend/"
    echo "📋 Contents:"
    ls -la dist/ai-research-assistant-frontend/
    
    if [ -f "dist/ai-research-assistant-frontend/index.html" ]; then
        echo "✅ index.html found"
    else
        echo "❌ index.html not found"
    fi
    
    if [ -d "dist/ai-research-assistant-frontend/assets" ]; then
        echo "✅ assets directory found"
    else
        echo "❌ assets directory not found"
    fi
else
    echo "❌ Build failed! dist/ai-research-assistant-frontend/ not found"
    echo "📋 Available directories:"
    ls -la dist/ || echo "dist/ directory not found"
    exit 1
fi

echo "🎉 Local build test completed!"
