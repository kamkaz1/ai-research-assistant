# Use multi-stage build for Railway
FROM node:18-alpine AS frontend-build

# Set working directory
WORKDIR /app

# Copy frontend files
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend

# Install frontend dependencies
RUN npm ci --only=production

# Copy frontend source
COPY frontend/ .

# Build frontend
RUN npm run build

# Backend stage
FROM python:3.11-slim AS backend-build

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Final stage
FROM nginx:alpine

# Install Python and dependencies
RUN apk add --no-cache python3 py3-pip gcc musl-dev

# Copy Python dependencies from backend stage
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin

# Copy backend application
COPY --from=backend-build /app /app/backend

# Copy frontend build
COPY --from=frontend-build /app/frontend/dist/ai-research-assistant-frontend /usr/share/nginx/html

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Create startup script
RUN echo '#!/bin/sh\n\
cd /app/backend\n\
python app.py &\n\
nginx -g "daemon off;"' > /start.sh && chmod +x /start.sh

# Expose port
EXPOSE 80

# Start both services
CMD ["/start.sh"]
