# CerebroGPT

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
cerebrogpt/
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
cd cerebrogpt
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

## 📖 Usage

### Making Research Queries

1. **Open CerebroGPT** in your browser at `http://localhost`
2. **Enter your research query** in the search bar (e.g., "latest AI breakthroughs 2024")
3. **Click "Launch Research"** or press Enter
4. **Wait for processing** - CerebroGPT will search the web and analyze results
5. **Review your research** - Get structured notes with:
   - Executive summary
   - Key insights and points
   - Properly cited sources

### Features

- **Research History**: View and reload previous research queries
- **Export Options**: Copy to clipboard or download as text file
- **Real-time Stats**: Monitor your research activity
- **Error Handling**: Clear error messages for troubleshooting

## 🔧 API Endpoints

### Research Endpoint
```http
GET /research?query=your_research_query
```

**Response:**
```json
{
  "title": "Research Title",
  "summary": "Executive summary...",
  "key_points": ["Point 1", "Point 2", "..."],
  "sources": [
    {
      "title": "Source Title",
      "url": "https://example.com"
    }
  ]
}
```

### Health Check
```http
GET /health
```

### Research History
```http
GET /history
```

### Statistics
```http
GET /stats
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
docker-compose exec backend python -m pytest

# Run specific test file
docker-compose exec backend python -m pytest tests/test_agent.py

# Run with coverage
docker-compose exec backend python -m pytest --cov=.
```

### Frontend Tests
```bash
# Run unit tests
docker-compose exec frontend npm test

# Run e2e tests
docker-compose exec frontend npm run e2e
```

## 🔒 Security

- **Environment Variables**: All API keys stored securely in environment variables
- **CORS Configuration**: Properly configured for frontend-backend communication
- **Input Validation**: All user inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling without exposing sensitive information

## 📊 Monitoring

### Built-in Statistics
- Total research queries
- Success rate percentage
- Recent activity (last 24 hours)

### Logs
- Backend logs available in Docker containers
- Structured logging for debugging
- Error tracking and reporting

## 🚀 Deployment

### Production Deployment
1. **Set up environment variables** for production
2. **Configure domain and SSL** certificates
3. **Set up monitoring** and logging
4. **Deploy with Docker Compose**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Variables
- `OPENAI_API_KEY` or `GOOGLE_API_KEY`: AI model access
- `SERPAPI_API_KEY`: Web search functionality
- `FLASK_ENV`: Set to `production` for production deployment

## 🔧 Configuration

### Backend Configuration
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **Caching**: In-memory caching for research results
- **Rate Limiting**: Configurable rate limits for API endpoints

### Frontend Configuration
- **API Endpoint**: Configurable backend URL
- **Theme**: Dark theme with futuristic design
- **Responsive**: Mobile-friendly interface

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify API keys are correctly set in `.env`
   - Check API key permissions and quotas

2. **Docker Issues**
   - Ensure Docker and Docker Compose are installed
   - Check container logs: `docker-compose logs`

3. **Frontend Not Loading**
   - Verify Nginx configuration
   - Check frontend container status

4. **Research Failures**
   - Check SerpAPI quota and API key
   - Verify internet connectivity
   - Review backend logs for errors

### Debug Mode
```bash
# Enable debug logging
export FLASK_ENV=development
docker-compose up --build
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Clone and setup
git clone <your-fork>
cd cerebrogpt

# Install dependencies
pip install -r backend/requirements.txt
npm install --prefix frontend

# Run development servers
python backend/app.py  # Backend on :5000
ng serve --prefix frontend  # Frontend on :4200
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **Google** for Gemini AI
- **SerpAPI** for web search capabilities
- **LangChain** for LLM orchestration framework
- **Angular** for the frontend framework
- **Flask** for the backend framework

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**CerebroGPT** - Where AI meets research intelligence! 🧠🤖
