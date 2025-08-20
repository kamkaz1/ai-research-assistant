# 🚀 Railway Deployment Guide for CerebroGPT

## Prerequisites
- GitHub account
- Railway account (free at [railway.app](https://railway.app))
- Google Gemini API key
- SerpAPI key

## Step-by-Step Deployment

### 1. Prepare Your Repository
Ensure your project is pushed to GitHub with these files:
- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `railway.toml`
- `.env` (with your API keys)

### 2. Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Verify your email

### 3. Deploy Your Project
1. **Click "New Project"**
2. **Select "Deploy from GitHub repo"**
3. **Choose your CerebroGPT repository**
4. **Railway will auto-detect your Docker setup**

### 4. Configure Environment Variables
In Railway dashboard, go to your project → Variables tab:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
SERPAPI_API_KEY=your_serpapi_key
FLASK_ENV=production
NODE_ENV=production
```

### 5. Deploy
1. **Click "Deploy"**
2. **Wait for build to complete** (5-10 minutes)
3. **Get your deployment URL** (e.g., `https://cerebrogpt-production.up.railway.app`)

### 6. Custom Domain (Optional)
1. Go to Settings → Domains
2. Add your custom domain
3. Configure DNS records

## Troubleshooting

### Common Issues:
1. **Build fails**: Check Dockerfile syntax
2. **Environment variables**: Ensure all API keys are set
3. **Health check fails**: Verify `/health` endpoint works
4. **Port issues**: Railway handles port mapping automatically

### Logs:
- View logs in Railway dashboard
- Check both backend and frontend logs

## Cost Management
- **Free tier**: $5/month credit
- **Monitor usage** in Railway dashboard
- **Upgrade if needed** for production use

## Success!
Your CerebroGPT will be live at: `https://your-project-name.up.railway.app`
