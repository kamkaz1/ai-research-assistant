# AI Research Assistant

An intelligent AI-powered research assistant that combines web search capabilities with advanced language models to generate comprehensive, structured research notes with citations.

## 🚀 Features

- **Web Search Integration**: Uses SerpAPI to search the web for current information
- **AI-Powered Analysis**: Leverages GPT-4 or Google Gemini for intelligent content processing
- **Structured Output**: Generates organized research notes with:
  - Clear titles and summaries
  - Key points and insights
  - Properly cited sources with URLs
- **Modern Web Interface**: Clean, responsive Angular frontend
- **Research History**: Track and revisit previous research queries
- **Export Capabilities**: Download research results as text files
- **Real-time Statistics**: Monitor usage and success rates
- **Docker Deployment**: Easy containerized deployment

## 🏗️ Architecture

```
ai-research-assistant/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── research_agent.py   # AI research logic
│   ├── requirements.txt    # Python dependencies
│   ├── tests/              # Unit tests
│   └── Dockerfile          # Backend container
├── frontend/               # Angular web application
│   ├── src/                # Angular source code
│   ├── package.json        # Node.js dependencies
│   ├── angular.json        # Angular configuration
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Container orchestration
├── env.example             # Environment variables template
└── README.md              # This file
```

## 🛠️ Tech Stack

### Backend
- **Python 3.9+** - Core programming language
- **Flask** - Web framework for API
- **LangChain** - LLM orchestration framework
- **OpenAI GPT-4** / **Google Gemini** - Language models
- **SerpAPI** - Web search API
- **SQLite** - Database for research history
- **Pytest** - Unit testing framework

### Frontend
- **Angular 17** - Modern web framework
- **TypeScript** - Type-safe JavaScript
- **CSS3** - Modern styling with gradients and animations
- **Font Awesome** - Icon library
- **Nginx** - Web server and reverse proxy

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and static file serving

## 📋 Prerequisites

- Docker and Docker Compose
- API keys for:
  - OpenAI GPT-4 (recommended) or Google Gemini
  - SerpAPI

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-research-assistant
```

### 2. Set Up Environment Variables
```bash
cp env.example .env
```

Edit `.env` file and add your API keys:
```env
# Choose one: OpenAI GPT-4 (recommended) or Google Gemini
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Required for web search functionality
SERPAPI_API_KEY=your_serpapi_key_here
```

### 3. Build and Run with Docker
```bash
docker-compose up --build
```

### 4. Access the Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 🔧 API Endpoints

### Research Endpoint
```http
GET /research?query=<your_research_query>
```

**Example:**
```bash
curl "http://localhost:5000/research?query=latest%20AI%20developments%20in%20healthcare"
```

**Response:**
```json
{
  "query": "latest AI developments in healthcare",
  "timestamp": "2024-01-15T10:30:00Z",
  "result": {
    "title": "Recent AI Advancements in Healthcare",
    "summary": "Comprehensive overview of AI applications...",
    "key_points": [
      "AI-powered diagnostic tools show 95% accuracy",
      "Machine learning algorithms improve patient outcomes",
      "Natural language processing enhances medical records"
    ],
    "sources": [
      {
        "title": "AI in Healthcare Report 2024",
        "url": "https://example.com/ai-healthcare-2024"
      }
    ]
  }
}
```

### Additional Endpoints
- `GET /health` - Health check and system status
- `GET /history?limit=10&offset=0` - Research history
- `GET /stats` - Usage statistics

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Test Coverage
The backend includes comprehensive unit tests covering:
- Research agent initialization
- API endpoint functionality
- Error handling
- Data validation
- Integration testing

## 🎨 Frontend Features

### User Interface
- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Real-time Feedback**: Loading states and error handling
- **Interactive Elements**: Hover effects and smooth animations

### Functionality
- **Search Interface**: Large, prominent search bar with suggestions
- **Results Display**: Structured presentation of research findings
- **History Management**: View and reload previous research queries
- **Export Options**: Copy to clipboard or download as text file
- **Statistics Dashboard**: Real-time usage metrics

## 🔒 Security Features

- **Input Validation**: Sanitized user inputs
- **Error Handling**: Graceful error management
- **API Rate Limiting**: Built-in protection against abuse
- **Secure Headers**: Nginx security headers
- **Environment Variables**: Secure API key management

## 📊 Monitoring and Logging

### Backend Logging
- Structured logging with timestamps
- Error tracking and debugging
- API usage monitoring
- Performance metrics

### Frontend Analytics
- User interaction tracking
- Error reporting
- Performance monitoring
- Usage statistics

## 🚀 Deployment

### Production Deployment
1. **Environment Setup**
   ```bash
   # Set production environment variables
   export NODE_ENV=production
   export FLASK_ENV=production
   ```

2. **Build and Deploy**
   ```bash
   docker-compose -f docker-compose.yml up -d --build
   ```

3. **Health Monitoring**
   ```bash
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

### Scaling
- **Horizontal Scaling**: Add multiple backend instances
- **Load Balancing**: Configure Nginx for multiple backends
- **Database**: Consider PostgreSQL for production use

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes (or GOOGLE_API_KEY) |
| `GOOGLE_API_KEY` | Google API key for Gemini | Yes (or OPENAI_API_KEY) |
| `SERPAPI_API_KEY` | SerpAPI key for web search | Yes |

### Nginx Configuration
The frontend includes optimized Nginx configuration for:
- Static file serving
- API proxy routing
- Gzip compression
- Security headers
- Caching strategies

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Errors**
   ```bash
   # Check API keys
   docker-compose logs backend
   
   # Verify environment variables
   docker-compose exec backend env | grep API
   ```

2. **Build Failures**
   ```bash
   # Clear Docker cache
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

3. **Frontend Not Loading**
   ```bash
   # Check frontend logs
   docker-compose logs frontend
   
   # Verify nginx configuration
   docker-compose exec frontend nginx -t
   ```

### Performance Optimization
- **Caching**: Enable Redis for session storage
- **CDN**: Use CDN for static assets
- **Database**: Optimize queries and add indexes
- **Monitoring**: Implement APM tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Development Setup
```bash
# Backend development
cd backend
pip install -r requirements.txt
python app.py

# Frontend development
cd frontend
npm install
npm start
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **Google** for Gemini API
- **SerpAPI** for web search capabilities
- **LangChain** for LLM orchestration
- **Angular** team for the excellent framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

---

**Built with ❤️ for comprehensive AI-powered research**
