# Use Node.js base image for frontend build
FROM node:18-alpine AS frontend-build
WORKDIR /app

# Copy package.json only (ignore package-lock.json to avoid conflicts)
COPY frontend/package.json ./frontend/
WORKDIR /app/frontend

# Clear npm cache and do a clean install with fallback
RUN echo "Clearing npm cache..." && \
    npm cache clean --force && \
    echo "Removing any existing node_modules..." && \
    rm -rf node_modules package-lock.json && \
    echo "Installing npm dependencies..." && \
    (npm install --verbose --no-optional || \
     (echo "First install failed, trying with legacy peer deps..." && \
      npm install --verbose --no-optional --legacy-peer-deps)) && \
    echo "Dependencies installed successfully"

# Copy frontend source
COPY frontend/ .

# Build with verbose output and error checking
RUN echo "Starting Angular build..." && \
    (npm run build || \
     (echo "Build failed, trying with legacy peer deps..." && \
      npm install --legacy-peer-deps && \
      npm run build)) && \
    echo "Angular build completed successfully" && \
    echo "Build output directory contents:" && \
    ls -la && \
    echo "Dist directory contents:" && \
    ls -la dist/ && \
    echo "Frontend dist directory contents:" && \
    ls -la dist/ai-research-assistant-frontend/ && \
    echo "Checking for index.html:" && \
    ls -la dist/ai-research-assistant-frontend/index.html && \
    echo "Checking for main.js:" && \
    ls -la dist/ai-research-assistant-frontend/main*.js

# Verify build output exists
RUN if [ ! -f "dist/ai-research-assistant-frontend/index.html" ]; then \
        echo "ERROR: index.html not found after build!" && \
        echo "Build output contents:" && \
        ls -la dist/ai-research-assistant-frontend/ && \
        exit 1; \
    fi

# Use Python base image for backend and final runtime
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nginx \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy built frontend from frontend-build stage
COPY --from=frontend-build /app/frontend/dist/ai-research-assistant-frontend /usr/share/nginx/html

# Verify frontend files were copied
RUN echo "Verifying frontend files in nginx directory:" && \
    ls -la /usr/share/nginx/html/ && \
    echo "Checking for index.html:" && \
    ls -la /usr/share/nginx/html/index.html && \
    echo "Checking for main.js:" && \
    ls -la /usr/share/nginx/html/main*.js

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Verify nginx configuration
RUN echo "Verifying nginx configuration:" && \
    nginx -t && \
    echo "Nginx configuration is valid"

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting nginx..."\n\
nginx -g "daemon off;" &\n\
echo "Starting Flask backend..."\n\
cd /app/backend\n\
python app.py' > /start.sh && chmod +x /start.sh

# Expose port
EXPOSE 80

# Start services
CMD ["/start.sh"]
