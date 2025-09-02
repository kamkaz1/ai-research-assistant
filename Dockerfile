# Use Python base image for Railway
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    curl \
    nginx \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Node.js for frontend build
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy frontend files and build
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install
RUN npm run build --verbose
RUN echo "=== Build output directory ===" && ls -la
RUN echo "=== Dist directory ===" && ls -la dist/ || echo "Dist directory not found"
RUN echo "=== Frontend dist directory ===" && ls -la dist/ai-research-assistant-frontend/ || echo "Frontend dist directory not found"
WORKDIR /app

# Copy built frontend to nginx directory
RUN echo "=== Copying frontend files ===" && \
    cp -r /app/frontend/dist/ai-research-assistant-frontend/* /usr/share/nginx/html/ && \
    echo "=== Nginx html directory ===" && \
    ls -la /usr/share/nginx/html/

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

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
