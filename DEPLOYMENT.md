# 🚀 Deployment Guide - QuizMaster Pro

Comprehensive deployment instructions for various platforms.

---

## 📋 Table of Contents

1. [Streamlit Cloud (Recommended)](#streamlit-cloud)
2. [Render](#render)
3. [Heroku](#heroku)
4. [AWS EC2](#aws-ec2)
5. [DigitalOcean](#digitalocean)
6. [Google Cloud Run](#google-cloud-run)
7. [Azure](#azure)
8. [Docker Deployment](#docker)

---

## 🌟 Streamlit Cloud

**Best for:** Quick deployment, free hosting, easy sharing  
**Cost:** FREE  
**Time:** 5 minutes

### Prerequisites
- GitHub account
- GitHub repository with your code

### Steps

1. **Prepare Repository**
   ```bash
   git init
   git add quiz_app.py requirements.txt
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/quiz-app.git
   git push -u origin main
   ```

2. **Deploy**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select repository: `YOUR_USERNAME/quiz-app`
   - Main file path: `quiz_app.py`
   - Click "Deploy"

3. **Access**
   - Your app: `https://YOUR_APP_NAME.streamlit.app`
   - Auto-updates on git push

### Configuration

Add `.streamlit/secrets.toml` for sensitive data:
```toml
[database]
url = "your-database-url"
```

### Advantages
✅ Free forever  
✅ Automatic HTTPS  
✅ Custom domains  
✅ Auto-deploy on push  
✅ Built-in secrets management  

---

## 🎨 Render

**Best for:** Free tier with custom domains  
**Cost:** FREE (with limitations) or $7/month  
**Time:** 10 minutes

### Steps

1. **Create `render.yaml`**
   ```yaml
   services:
     - type: web
       name: quizmaster-pro
       env: python
       region: oregon
       plan: free
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run quiz_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
   ```

2. **Deploy**
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub repository
   - Use the `render.yaml` blueprint
   - Click "Create Web Service"

3. **Custom Domain** (Optional)
   - Go to Settings > Custom Domain
   - Add your domain
   - Update DNS records

### Database Persistence

For persistent database on Render:

1. Create a disk:
   ```yaml
   disk:
     name: quiz-data
     mountPath: /app/data
     sizeGB: 1
   ```

2. Update app to use `/app/data/quiz_results.db`

---

## 🔥 Heroku

**Best for:** Traditional deployment, add-ons  
**Cost:** $5-7/month (no free tier as of Nov 2022)  
**Time:** 15 minutes

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh

   # Windows
   # Download from heroku.com/downloads
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create quizmaster-pro-app
   ```

3. **Files Already Created**
   - ✅ `Procfile`
   - ✅ `setup.sh`
   - ✅ `requirements.txt`

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

### Database Addon

For PostgreSQL:
```bash
heroku addons:create heroku-postgresql:mini
```

Update code to use Postgres:
```python
import os
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### Monitoring
```bash
heroku logs --tail
heroku ps
```

---

## ☁️ AWS EC2

**Best for:** Full control, scalability  
**Cost:** ~$5-20/month  
**Time:** 30 minutes

### Steps

1. **Launch EC2 Instance**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t2.micro (free tier) or t2.small
   - Security Group: Allow port 8501, 22, 80

2. **Connect via SSH**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install requirements
   pip install streamlit pandas
   ```

4. **Upload Application**
   ```bash
   # From local machine
   scp -i your-key.pem quiz_app.py ubuntu@your-ec2-ip:~/
   ```

5. **Run with Systemd** (for auto-restart)

   Create `/etc/systemd/system/quiz-app.service`:
   ```ini
   [Unit]
   Description=QuizMaster Pro
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu
   ExecStart=/home/ubuntu/venv/bin/streamlit run quiz_app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable quiz-app
   sudo systemctl start quiz-app
   sudo systemctl status quiz-app
   ```

6. **Setup Nginx Reverse Proxy**

   Create `/etc/nginx/sites-available/quiz-app`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/quiz-app /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **SSL Certificate** (Optional but recommended)
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

## 🌊 DigitalOcean

**Best for:** Simple cloud hosting  
**Cost:** $6-12/month  
**Time:** 20 minutes

### Steps

1. **Create Droplet**
   - Image: Ubuntu 22.04
   - Plan: Basic $6/month
   - Add SSH key

2. **SSH into Droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Setup Application**
   ```bash
   # Install Python and pip
   apt update
   apt install python3-pip python3-venv -y

   # Create app directory
   mkdir /var/www/quiz-app
   cd /var/www/quiz-app

   # Upload files (from local)
   # scp quiz_app.py requirements.txt root@your-droplet-ip:/var/www/quiz-app/

   # Install dependencies
   pip3 install -r requirements.txt
   ```

4. **Use Docker** (Easier)
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Install Docker Compose
   curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose

   # Run application
   docker-compose up -d
   ```

5. **Configure Firewall**
   ```bash
   ufw allow 8501
   ufw allow 22
   ufw enable
   ```

---

## 🐳 Docker

**Best for:** Containerized deployment anywhere  
**Cost:** Depends on hosting  
**Time:** 10 minutes

### Local Docker Deployment

1. **Build Image**
   ```bash
   docker build -t quizmaster-pro .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name quiz-app \
     -p 8501:8501 \
     -v $(pwd)/data:/app/data \
     quizmaster-pro
   ```

3. **Access**
   - Open `http://localhost:8501`

### Docker Compose

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Push to Docker Hub

```bash
# Tag image
docker tag quizmaster-pro yourusername/quizmaster-pro:latest

# Login
docker login

# Push
docker push yourusername/quizmaster-pro:latest
```

---

## ☁️ Google Cloud Run

**Best for:** Serverless, auto-scaling  
**Cost:** Free tier available, then pay-per-use  
**Time:** 15 minutes

### Steps

1. **Install Google Cloud SDK**
   ```bash
   # Follow: https://cloud.google.com/sdk/docs/install
   ```

2. **Build Container**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/quiz-app
   ```

3. **Deploy**
   ```bash
   gcloud run deploy quiz-app \
     --image gcr.io/YOUR_PROJECT_ID/quiz-app \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8501
   ```

4. **Get URL**
   ```bash
   gcloud run services describe quiz-app --platform managed --region us-central1
   ```

---

## 🔷 Azure

**Best for:** Microsoft ecosystem integration  
**Cost:** Free tier available  
**Time:** 20 minutes

### Steps

1. **Install Azure CLI**
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Login**
   ```bash
   az login
   ```

3. **Create Resources**
   ```bash
   # Create resource group
   az group create --name quiz-app-rg --location eastus

   # Create App Service Plan
   az appservice plan create \
     --name quiz-app-plan \
     --resource-group quiz-app-rg \
     --sku B1 \
     --is-linux

   # Create Web App
   az webapp create \
     --resource-group quiz-app-rg \
     --plan quiz-app-plan \
     --name quizmaster-pro-app \
     --runtime "PYTHON:3.11"
   ```

4. **Deploy**
   ```bash
   az webapp up \
     --name quizmaster-pro-app \
     --resource-group quiz-app-rg
   ```

---

## 🔐 Security Checklist

Before going to production:

- [ ] Enable HTTPS (SSL certificate)
- [ ] Set up firewall rules
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor application logs
- [ ] Use strong passwords
- [ ] Implement CSRF protection
- [ ] Validate all user inputs

---

## 📊 Monitoring & Maintenance

### Application Monitoring

**Streamlit Cloud:**
- Built-in logs and metrics
- View at: App menu > Manage app > Logs

**Self-hosted:**
```bash
# View logs
journalctl -u quiz-app -f

# Monitor resources
htop

# Check disk space
df -h
```

### Database Backups

**Automated backup script:**
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp quiz_results.db "$BACKUP_DIR/quiz_results_$DATE.db"

# Keep only last 7 days
find $BACKUP_DIR -name "quiz_results_*.db" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup-script.sh
```

---

## 🎯 Performance Optimization

### For High Traffic

1. **Use PostgreSQL instead of SQLite**
2. **Add caching:**
   ```python
   @st.cache_data
   def load_quiz_data():
       return QUIZ_DATA
   ```
3. **Implement CDN for static assets**
4. **Use load balancer for multiple instances**
5. **Enable gzip compression**
6. **Optimize database queries with indexes**

---

## 📞 Support

Having deployment issues?

1. Check platform-specific documentation
2. Review logs for errors
3. Verify all files are uploaded
4. Check environment variables
5. Ensure ports are open
6. Verify dependencies are installed

---

**Choose your deployment platform and follow the guide above! 🚀**
