# Use Node.js base image for frontend build
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source and build
COPY frontend/ .
RUN npm run build

# Use Python base image for runtime
FROM python:3.11-slim
WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy built frontend to nginx directory
COPY --from=frontend-build /app/frontend/dist/ai-research-assistant-frontend /usr/share/nginx/html

# Remove default nginx configuration and copy our custom config
RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Create startup script with comprehensive debugging
RUN echo '#!/bin/bash\n\
set -e\n\
echo "=== Starting CerebroGPT Services ==="\n\
echo "Current directory: $(pwd)"\n\
echo "Contents of /usr/share/nginx/html:" && ls -la /usr/share/nginx/html\n\
echo "Checking if index.html exists:" && ls -la /usr/share/nginx/html/index.html\n\
echo "Nginx configuration:" && cat /etc/nginx/conf.d/default.conf\n\
echo "Testing nginx configuration..."\n\
nginx -t && echo "Nginx config is valid"\n\
echo "Starting nginx..."\n\
nginx -g "daemon off;" &\n\
echo "Nginx started with PID: $!"\n\
echo "Starting Flask backend..."\n\
cd /app/backend\n\
python app.py' > /start.sh && chmod +x /start.sh

EXPOSE 80
CMD ["/start.sh"]
