#!/bin/bash

echo "🚀 Starting CerebroGPT locally..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please create a .env file with your API keys:"
    echo "   GOOGLE_API_KEY=your_google_api_key"
    echo "   SERPAPI_API_KEY=your_serpapi_key"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build and start the containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ CerebroGPT is running successfully!"
    echo "🌐 Frontend: http://localhost"
    echo "🔧 Backend API: http://localhost:5000"
    echo "📊 Health Check: http://localhost/health"
    echo ""
    echo "To stop the application, run: docker-compose down"
else
    echo "❌ Services failed to start properly"
    echo "📋 Check logs with: docker-compose logs"
    exit 1
fi
