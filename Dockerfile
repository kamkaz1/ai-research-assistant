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

# Copy simple nginx configuration
COPY frontend/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting nginx..."\n\
nginx -g "daemon off;" &\n\
echo "Starting Flask backend..."\n\
cd /app/backend\n\
python app.py' > /start.sh && chmod +x /start.sh

EXPOSE 80
CMD ["/start.sh"]
