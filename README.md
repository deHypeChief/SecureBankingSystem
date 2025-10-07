# Secure Banking System - Deployment Guide

## 🐳 Docker Deployment

### Prerequisites

1. **Install Docker:**
   - Windows: Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
   - Linux: `sudo apt-get install docker.io docker-compose`
   - macOS: Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

### Quick Start with Docker

1. **Clone and navigate to project:**
   ```bash
   cd SecureBankingSystem
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   Open http://localhost:5000 in your browser

### Manual Docker Commands

1. **Build the Docker image:**
   ```bash
   docker build -t secure-banking-system .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 --name banking-app secure-banking-system
   ```

3. **Run with environment variables:**
   ```bash
   docker run -p 5000:5000 \
     -e SECRET_KEY=your-secret-key \
     -e FLASK_ENV=production \
     --name banking-app \
     secure-banking-system
   ```

### Production Deployment

1. **Create production environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your production values
   ```

2. **Build for production:**
   ```bash
   docker build -t secure-banking-system:latest .
   ```

3. **Run in production mode:**
   ```bash
   docker run -d \
     --name banking-prod \
     -p 80:5000 \
     --env-file .env \
     --restart unless-stopped \
     secure-banking-system:latest
   ```

### Docker Commands Reference

- **View logs:** `docker logs banking-app`
- **Access container:** `docker exec -it banking-app /bin/bash`
- **Stop container:** `docker stop banking-app`
- **Remove container:** `docker rm banking-app`
- **Health check:** `docker inspect --format='{{.State.Health.Status}}' banking-app`

## ☁️ Vercel Deployment

### Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

### Deployment Steps

1. Navigate to your project directory:
   ```bash
   cd SecureBankingSystem
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

3. Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Choose your account
   - Link to existing project? **N** (for first deployment)
   - What's your project's name? **secure-banking-system** (or your preferred name)
   - In which directory is your code located? **./** (current directory)

4. Your app will be deployed! Vercel will provide you with a URL.

### Environment Variables

For production, set these environment variables in Vercel dashboard or Docker:

- `SECRET_KEY`: A secure secret key for Flask sessions
- `FLASK_ENV`: Set to `production` for production deployment
- `PORT`: Port number (default: 5000)

## 🖥️ Local Development

To run locally without Docker:
```bash
pip install -r requirements.txt
python web_app.py
```

Then open http://localhost:5000

## 🔐 Demo Credentials

- **Username:** alice (or register new user)
- **Password:** secure123 (or create strong password)
- **OTP:** Use the "Generate Fresh OTP" button

## ✨ Features

- 🔐 Multi-factor authentication
- 💰 Banking operations (transfer, balance check)
- 📊 Performance monitoring
- 🔒 Advanced cryptographic security
- 📱 Responsive web interface
- 🐳 Docker containerization
- ☁️ Cloud deployment ready

## 🏗️ Architecture

The application uses:
- **Flask** for the web framework
- **Gunicorn** for production WSGI server
- **Custom cryptographic modules** for security
- **Performance monitoring system**
- **Docker** for containerization
- **Vercel/Cloud** deployment options

## 🔧 Configuration

### Docker Environment Variables
```bash
SECRET_KEY=your-super-secret-key
FLASK_ENV=production
PORT=5000
DEBUG=false
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
```

### Health Monitoring
- Health check endpoint: `/health`
- Docker health checks included
- Performance metrics available at `/api/performance`

## 📊 Monitoring

- **Health Check:** GET `/health`
- **Performance Metrics:** Available in dashboard
- **Docker Logs:** `docker logs <container-name>`
- **Container Stats:** `docker stats <container-name>`