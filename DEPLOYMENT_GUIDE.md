# 🚀 Insurance Fraud Detection Platform - Deployment Guide

## Overview

This guide provides step-by-step instructions to deploy the Insurance Fraud Detection Platform locally and to cloud platforms.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Local Deployment with Docker](#local-deployment-with-docker)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Checklist](#production-checklist)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **CPU**: 2+ cores
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 5GB free space

### Software Requirements

- **Python**: 3.9+ ([Download](https://www.python.org/downloads/))
- **Docker**: 20.10+ ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose**: 1.29+ (included with Docker Desktop)
- **Git**: 2.20+ ([Download](https://git-scm.com/))

### Optional for Cloud Deployment

- AWS CLI or similar cloud provider CLI
- Kubernetes kubectl for K8s deployments
- Terraform for infrastructure-as-code

---

## Local Development Setup

### Step 1: Clone and Setup Repository

```bash
# Clone the repository
git clone <repository-url>
cd insurance-fraud-detection-platform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Prepare ML Models

Ensure you have pre-trained models in `app/artifacts/`:

```
app/artifacts/
├── model.pkl          # Trained XGBoost model
├── pipeline.pkl       # Data preprocessing pipeline
└── feature_names.txt  # Feature list (optional)
```

If models are missing, train them:

```bash
python app/model/train.py
```

### Step 3: Run Locally (Development)

**Terminal 1 - API Server:**

```bash
python -m uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Dashboard:**

```bash
streamlit run app/frontend/streamlit_app.py
```

**Access the application:**

- Dashboard: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Local Deployment with Docker

### Step 1: Prepare Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# nano .env  (or use your editor)
```

### Step 2: Build Docker Images

```bash
# Build both services
docker-compose build

# Or build individual services
docker-compose build fraud-api
docker-compose build fraud-dashboard
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f fraud-api
docker-compose logs -f fraud-dashboard
```

### Step 4: Verify Deployment

```bash
# Check services status
docker-compose ps

# Test API health
curl http://localhost:8000/health

# Test API endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Month": "January",
    "WeekOfMonth": 1,
    "DayOfWeek": "Monday",
    "Make": "Honda",
    "AccidentArea": "Urban",
    "Age": 35,
    "Fault": "Policy Holder",
    "PolicyType": "Sedan - Collision",
    "VehicleCategory": "Sedan",
    "VehiclePrice": "20000 to 29000",
    "Deductible": 500,
    "DriverRating": 3,
    "Year": 2015,
    "BasePolicy": "Collision"
  }'
```

### Step 5: Stop Services

```bash
# Stop all services
docker-compose down

# Remove volumes (clean data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

---

## Cloud Deployment

### AWS Elastic Container Service (ECS)

#### Step 1: Push to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create repositories
aws ecr create-repository --repository-name fraud-api --region us-east-1
aws ecr create-repository --repository-name fraud-dashboard --region us-east-1

# Tag and push images
docker tag insurance-fraud-detection-platform_fraud-api:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/fraud-api:latest

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/fraud-api:latest

# Repeat for dashboard
docker tag insurance-fraud-detection-platform_fraud-dashboard:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/fraud-dashboard:latest

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/fraud-dashboard:latest
```

#### Step 2: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name fraud-detection

# Create task definition (use AWS Console or CLI)
# Copy content from ecs-task-definition.json
```

#### Step 3: Deploy Service

```bash
aws ecs create-service \
  --cluster fraud-detection \
  --service-name fraud-api-service \
  --task-definition fraud-api:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

### Google Cloud Run

#### Step 1: Setup GCP

```bash
# Initialize gcloud
gcloud init

# Configure Docker for GCP
gcloud auth configure-docker

# Create project
gcloud projects create insurance-fraud-detection

# Set project
gcloud config set project insurance-fraud-detection
```

#### Step 2: Build and Push Images

```bash
# Build API
gcloud builds submit --tag gcr.io/insurance-fraud-detection/fraud-api

# Build Dashboard
gcloud builds submit --tag gcr.io/insurance-fraud-detection/fraud-dashboard
```

#### Step 3: Deploy to Cloud Run

```bash
# Deploy API
gcloud run deploy fraud-api \
  --image gcr.io/insurance-fraud-detection/fraud-api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2

# Deploy Dashboard
gcloud run deploy fraud-dashboard \
  --image gcr.io/insurance-fraud-detection/fraud-dashboard \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2
```

### Kubernetes Deployment

#### Step 1: Create Kubernetes Manifests

```bash
# Create namespace
kubectl create namespace fraud-detection

# Apply deployments
kubectl apply -f k8s/fraud-api-deployment.yaml -n fraud-detection
kubectl apply -f k8s/fraud-dashboard-deployment.yaml -n fraud-detection
kubectl apply -f k8s/service.yaml -n fraud-detection
```

#### Step 2: Verify Deployment

```bash
# Check pods
kubectl get pods -n fraud-detection

# Check services
kubectl get svc -n fraud-detection

# View logs
kubectl logs -f deployment/fraud-api -n fraud-detection
```

### Azure Container Instances (ACI)

```bash
# Create resource group
az group create \
  --name fraud-detection-rg \
  --location eastus

# Create container instances
az container create \
  --resource-group fraud-detection-rg \
  --name fraud-api \
  --image myregistry.azurecr.io/fraud-api:latest \
  --cpu 2 \
  --memory 2 \
  --port 8000 \
  --environment-variables API_PORT=8000
```

---

## Production Checklist

### Security

- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Implement API authentication (API keys, OAuth2)
- [ ] Set up VPC/Private networks
- [ ] Enable data encryption at rest and in transit
- [ ] Configure secrets management (AWS Secrets Manager, Vault)
- [ ] Implement rate limiting
- [ ] Enable CORS properly (not "*")
- [ ] Set up WAF (Web Application Firewall)
- [ ] Regular security audits and penetration testing

### Performance

- [ ] Configure auto-scaling policies
- [ ] Set up load balancing (ALB, NLB)
- [ ] Implement caching (Redis)
- [ ] Configure CDN for static assets
- [ ] Monitor API response times
- [ ] Optimize database queries
- [ ] Implement request/response compression
- [ ] Set up connection pooling

### Monitoring & Logging

- [ ] Configure centralized logging (CloudWatch, ELK, Datadog)
- [ ] Set up monitoring dashboards
- [ ] Configure alerts for critical metrics
- [ ] Enable distributed tracing
- [ ] Set up error tracking (Sentry)
- [ ] Implement health checks
- [ ] Monitor resource utilization

### Data Management

- [ ] Set up automated backups
- [ ] Configure disaster recovery
- [ ] Implement data retention policies
- [ ] Enable data governance
- [ ] Set up audit logs
- [ ] Implement GDPR compliance

### DevOps

- [ ] Set up CI/CD pipeline
- [ ] Configure automated testing
- [ ] Implement blue-green deployments
- [ ] Set up infrastructure as code
- [ ] Document deployment procedures
- [ ] Create runbooks for common issues

---

## Monitoring & Maintenance

### Health Monitoring

```bash
# Check API health
curl http://localhost:8000/health

# Get API statistics
curl http://localhost:8000/stats

# View logs
docker-compose logs -f fraud-api
```

### Database Maintenance

```bash
# Backup data
docker-compose exec fraud-api \
  python -m app.utils.backup

# Clean old logs
docker-compose exec fraud-api \
  python -m app.utils.cleanup
```

### Model Updates

```bash
# Retrain model
python app/model/train.py

# Evaluate model
python app/model/evaluate.py

# Deploy new model
docker-compose build fraud-api
docker-compose up -d fraud-api
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000

# Kill process
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>
```

### Docker Build Fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### API Connection Error

```bash
# Check if API is running
docker-compose ps

# View API logs
docker-compose logs fraud-api

# Restart API
docker-compose restart fraud-api
```

### Out of Memory

```bash
# Increase Docker memory
# In Docker Desktop settings: Preferences > Resources > Memory

# Or limit container memory
docker-compose down
# Edit docker-compose.yml
# Add under service: memory: 4G
docker-compose up -d
```

### Model Loading Error

```bash
# Verify model files exist
ls -la app/artifacts/

# Check file permissions
chmod 644 app/artifacts/model.pkl
chmod 644 app/artifacts/pipeline.pkl

# Retrain model
python app/model/train.py
```

---

## Environment Variables

Common environment variables:

```env
# API Configuration
API_URL=http://fraud-api:8000
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Model Paths
MODEL_PATH=./app/artifacts/model.pkl
PIPELINE_PATH=./app/artifacts/pipeline.pkl

# Logging
LOG_LEVEL=INFO

# Fraud Detection
FRAUD_PROBABILITY_THRESHOLD=0.7
HIGH_RISK_THRESHOLD=0.8

# Cloud Settings
ENVIRONMENT=production
DEBUG=false
```

---

## Support & Resources

- **Documentation**: [Full Documentation](./README.md)
- **API Documentation**: http://api-url:8000/docs
- **Issues**: GitHub Issues
- **Email**: support@frauddetection.com

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Last Updated**: May 2026
**Version**: 1.0.0
