# 👨‍💻 FertiVision Developer Manual - Complete Technical Guide

**Comprehensive Technical Implementation Guide for Developers**

This manual provides complete technical documentation for implementing, integrating, and extending the FertiVision AI-enhanced reproductive medicine analysis system.

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Development Environment Setup](#development-environment-setup)
3. [API Integration](#api-integration)
4. [SDK Development](#sdk-development)
5. [Database Schema](#database-schema)
6. [AI Model Implementation](#ai-model-implementation)
7. [Security Implementation](#security-implementation)
8. [Performance Optimization](#performance-optimization)
9. [Testing Framework](#testing-framework)
10. [Deployment Guide](#deployment-guide)
11. [Monitoring & Logging](#monitoring--logging)
12. [Troubleshooting](#troubleshooting)

---

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   Mobile App    │    │   EMR System    │
│   (React/Vue)   │    │   (React Native)│    │   (HL7/FHIR)    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │      API Gateway         │
                    │   (FastAPI/Flask)        │
                    └─────────────┬─────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
┌─────────┴───────┐    ┌─────────┴───────┐    ┌─────────┴───────┐
│   Auth Service  │    │  Image Analysis │    │  Report Service │
│   (JWT/OAuth)   │    │   (AI Models)   │    │   (PDF/Export)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │      Data Layer          │
                    │  (PostgreSQL/MongoDB)    │
                    └───────────────────────────┘
```

### Technology Stack

#### Backend
- **API Framework**: FastAPI 0.104.1
- **Language**: Python 3.8+
- **Database**: PostgreSQL 13+ / SQLite (development)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT tokens, OAuth 2.0
- **File Storage**: AWS S3 / Local filesystem
- **Caching**: Redis 6.0+

#### AI/ML Stack
- **Deep Learning**: PyTorch 2.0, TensorFlow 2.13
- **Computer Vision**: OpenCV 4.8, Pillow 10.0
- **Model Serving**: TorchServe, ONNX Runtime
- **Image Processing**: NumPy, scikit-image

#### Frontend
- **Framework**: React 18+ / Vue.js 3+
- **State Management**: Redux Toolkit / Pinia
- **UI Library**: Material-UI / Ant Design
- **Charts**: Chart.js / D3.js

#### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes (production)
- **CI/CD**: GitHub Actions, GitLab CI
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

---

## 💻 Development Environment Setup

### Prerequisites
```bash
# Required software versions
Python >= 3.8
Node.js >= 16.0
Docker >= 20.10
Git >= 2.30

# Operating System Support
macOS 10.15+
Ubuntu 18.04+ / Debian 10+
Windows 10+ (with WSL2)
```

### Local Development Setup

#### 1. Clone Repository
```bash
git clone https://github.com/satishskid/fertivision-codelm.git
cd fertivision-codelm
```

#### 2. Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_enhanced.txt
pip install -r requirements_api.txt
pip install -r requirements_dataset_testing.txt
```

#### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env.local

# Configure environment variables
cat > .env.local << EOF
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/fertivision
SQLITE_DATABASE=reproductive_analysis.db

# API Configuration
API_HOST=localhost
API_PORT=5003
API_KEY=fv_demo_key_12345
DEBUG=True

# AI Model Configuration
HUGGINGFACE_API_KEY=your_hf_token_here
MODEL_CACHE_DIR=./models
ENABLE_GPU=False

# Storage Configuration
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=52428800  # 50MB

# Security
SECRET_KEY=your_secret_key_here
JWT_EXPIRATION=3600
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
EOF
```

#### 4. Database Setup
```bash
# PostgreSQL (Production)
createdb fertivision
python -m alembic upgrade head

# SQLite (Development)
python reproductive_classification_system.py
```

#### 5. Model Setup
```bash
# Download required AI models
python model_config_manager.py --download-all

# Test model loading
python test_enhanced_features.py
```

#### 6. Start Development Server
```bash
# Start API server
python app.py

# Alternative: Use enhanced system
./run_enhanced_system.sh

# Start with auto-reload
uvicorn app:app --host 0.0.0.0 --port 5003 --reload
```

### Docker Development Setup

#### 1. Docker Compose
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5003:5003"
    volumes:
      - .:/app
      - ./uploads:/app/uploads
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://postgres:password@db:5432/fertivision
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: fertivision
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

#### 2. Start Development Environment
```bash
# Build and start services
docker-compose -f docker-compose.dev.yml up --build

# Run in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f api
```

---

## 🔌 API Integration

### Authentication Implementation

#### JWT Token Authentication
```python
# auth.py
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

class AuthService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.security = HTTPBearer()
    
    def create_access_token(self, user_id: str, permissions: list) -> str:
        payload = {
            'user_id': user_id,
            'permissions': permissions,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

# Usage in FastAPI
auth_service = AuthService(settings.SECRET_KEY)

def get_current_user(token: str = Depends(auth_service.security)):
    return auth_service.verify_token(token.credentials)
```

#### API Key Authentication
```python
# config.py
from fastapi import HTTPException, Header
from typing import Optional

API_KEYS = {
    "fv_demo_key_12345": {
        "name": "Demo Client",
        "permissions": ["sperm_analysis", "oocyte_analysis", "embryo_analysis"],
        "rate_limit": 1000
    },
    "fv_clinic_001": {
        "name": "IVF Clinic 001",
        "permissions": ["all"],
        "rate_limit": 5000
    }
}

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    return API_KEYS[x_api_key]
```

### API Endpoint Implementation

#### Image Analysis Endpoints
```python
# api_server.py
from fastapi import FastAPI, File, UploadFile, Form, Depends
from PIL import Image
import io

app = FastAPI(title="FertiVision API", version="1.2.0")

@app.post("/api/v1/analyze/sperm")
async def analyze_sperm(
    image: UploadFile = File(...),
    patient_id: str = Form(...),
    case_id: str = Form(...),
    analysis_type: str = Form(default="standard"),
    api_key: dict = Depends(verify_api_key)
):
    try:
        # Validate image format
        if image.content_type not in ['image/jpeg', 'image/png', 'image/tiff']:
            raise HTTPException(400, "Unsupported image format")
        
        # Load and process image
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data))
        
        # Perform AI analysis
        analyzer = SpermAnalyzer()
        results = await analyzer.analyze(pil_image, analysis_type)
        
        # Store results
        analysis_record = {
            "analysis_id": f"SA_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "patient_id": patient_id,
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "confidence_scores": results.get('confidence_scores', {}),
            "image_metadata": {
                "resolution": f"{pil_image.width}x{pil_image.height}",
                "format": pil_image.format,
                "size_bytes": len(image_data)
            }
        }
        
        # Save to database
        db.save_analysis(analysis_record)
        
        return analysis_record
        
    except Exception as e:
        logger.error(f"Sperm analysis failed: {str(e)}")
        raise HTTPException(500, f"Analysis failed: {str(e)}")
```

#### Batch Processing Implementation
```python
@app.post("/api/v1/analyze/batch")
async def analyze_batch(
    images: List[UploadFile] = File(...),
    patient_ids: List[str] = Form(...),
    analysis_types: List[str] = Form(...),
    api_key: dict = Depends(verify_api_key)
):
    if len(images) > 10:  # Limit batch size
        raise HTTPException(400, "Maximum 10 images per batch")
    
    results = []
    for image, patient_id, analysis_type in zip(images, patient_ids, analysis_types):
        try:
            # Process each image
            result = await process_single_image(image, patient_id, analysis_type)
            results.append(result)
        except Exception as e:
            results.append({
                "patient_id": patient_id,
                "error": str(e),
                "status": "failed"
            })
    
    return {
        "batch_id": f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "total_processed": len(results),
        "successful": len([r for r in results if "error" not in r]),
        "failed": len([r for r in results if "error" in r]),
        "results": results
    }
```

### Rate Limiting Implementation
```python
# rate_limiter.py
import redis
import time
from fastapi import HTTPException

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def check_rate_limit(self, api_key: str, limit: int, window: int = 3600):
        """Check if API key is within rate limit"""
        key = f"rate_limit:{api_key}"
        current_time = int(time.time())
        
        # Use sliding window
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, current_time - window)
        pipe.zcard(key)
        pipe.zadd(key, {str(current_time): current_time})
        pipe.expire(key, window)
        
        results = pipe.execute()
        current_requests = results[1]
        
        if current_requests >= limit:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Limit: {limit} requests per hour"
            )
        
        return {
            "requests_made": current_requests,
            "requests_remaining": limit - current_requests,
            "reset_time": current_time + window
        }
```

---

## 🧬 AI Model Implementation

### Model Architecture

#### Sperm Analysis Model
```python
# models/sperm_analyzer.py
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet50

class SpermAnalysisNet(nn.Module):
    def __init__(self, num_classes=4):  # concentration, motility, morphology, vitality
        super(SpermAnalysisNet, self).__init__()
        
        # Backbone: ResNet-50
        self.backbone = resnet50(pretrained=True)
        self.backbone.fc = nn.Identity()  # Remove final layer
        
        # Custom heads for different parameters
        self.concentration_head = nn.Sequential(
            nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 1)  # Regression output
        )
        
        self.motility_head = nn.Sequential(
            nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 3)  # Progressive, non-progressive, immotile
        )
        
        self.morphology_head = nn.Sequential(
            nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 4)  # Normal, head, neck, tail defects
        )
        
        self.vitality_head = nn.Sequential(
            nn.Linear(2048, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 2)  # Live, dead
        )
    
    def forward(self, x):
        features = self.backbone(x)
        
        concentration = self.concentration_head(features)
        motility = self.motility_head(features)
        morphology = self.morphology_head(features)
        vitality = self.vitality_head(features)
        
        return {
            'concentration': concentration,
            'motility': motility,
            'morphology': morphology,
            'vitality': vitality
        }

class SpermAnalyzer:
    def __init__(self, model_path: str, device: str = 'cpu'):
        self.device = torch.device(device)
        self.model = SpermAnalysisNet()
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        tensor = self.transform(image).unsqueeze(0)
        return tensor.to(self.device)
    
    def postprocess_results(self, outputs):
        """Convert model outputs to clinical parameters"""
        results = {}
        
        # Concentration (million/mL)
        concentration = torch.sigmoid(outputs['concentration']).item() * 100
        results['concentration'] = {
            'value': round(concentration, 1),
            'unit': 'million/ml',
            'reference': '≥15 million/ml',
            'status': 'normal' if concentration >= 15 else 'abnormal'
        }
        
        # Motility percentages
        motility_probs = torch.softmax(outputs['motility'], dim=1)[0]
        progressive = motility_probs[0].item() * 100
        non_progressive = motility_probs[1].item() * 100
        immotile = motility_probs[2].item() * 100
        
        results['motility'] = {
            'progressive': round(progressive, 1),
            'non_progressive': round(non_progressive, 1),
            'immotile': round(immotile, 1),
            'total_motile': round(progressive + non_progressive, 1),
            'status': 'normal' if progressive >= 32 else 'abnormal'
        }
        
        # Morphology percentages
        morphology_probs = torch.softmax(outputs['morphology'], dim=1)[0]
        normal_forms = morphology_probs[0].item() * 100
        
        results['morphology'] = {
            'normal_forms': round(normal_forms, 1),
            'head_defects': round(morphology_probs[1].item() * 100, 1),
            'neck_defects': round(morphology_probs[2].item() * 100, 1),
            'tail_defects': round(morphology_probs[3].item() * 100, 1),
            'status': 'normal' if normal_forms >= 4 else 'abnormal'
        }
        
        # Vitality
        vitality_probs = torch.softmax(outputs['vitality'], dim=1)[0]
        live_percentage = vitality_probs[0].item() * 100
        
        results['vitality'] = {
            'live': round(live_percentage, 1),
            'dead': round(100 - live_percentage, 1),
            'status': 'normal' if live_percentage >= 58 else 'abnormal'
        }
        
        return results
    
    async def analyze(self, image, analysis_type: str = 'standard'):
        """Perform complete sperm analysis"""
        try:
            # Preprocess
            input_tensor = self.preprocess_image(image)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
            
            # Postprocess
            results = self.postprocess_results(outputs)
            
            # Calculate confidence scores
            confidence_scores = self.calculate_confidence(outputs)
            results['confidence_scores'] = confidence_scores
            
            return results
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def calculate_confidence(self, outputs):
        """Calculate confidence scores for each parameter"""
        confidence = {}
        
        # Use entropy-based confidence
        for param_name, logits in outputs.items():
            if param_name == 'concentration':
                # For regression, use prediction stability
                confidence[param_name] = 0.95  # Placeholder
            else:
                # For classification, use entropy
                probs = torch.softmax(logits, dim=1)[0]
                entropy = -torch.sum(probs * torch.log(probs + 1e-8))
                confidence[param_name] = (1 - entropy / torch.log(torch.tensor(len(probs)))).item()
        
        return confidence
```

#### Embryo Analysis Model
```python
# models/embryo_analyzer.py
class EmbryoGardnerNet(nn.Module):
    def __init__(self):
        super(EmbryoGardnerNet, self).__init__()
        
        # Multi-task architecture for Gardner grading
        self.feature_extractor = models.efficientnet_b4(pretrained=True)
        self.feature_extractor.classifier = nn.Identity()
        
        # Gardner criteria heads
        self.expansion_head = nn.Linear(1792, 6)  # Grades 1-6
        self.icm_head = nn.Linear(1792, 3)        # Grades A, B, C
        self.te_head = nn.Linear(1792, 3)         # Grades A, B, C
        
        # Quality assessment
        self.quality_head = nn.Linear(1792, 1)    # Overall quality score
    
    def forward(self, x):
        features = self.feature_extractor(x)
        
        return {
            'expansion': self.expansion_head(features),
            'icm': self.icm_head(features),
            'te': self.te_head(features),
            'quality': torch.sigmoid(self.quality_head(features))
        }

class EmbryoAnalyzer:
    def __init__(self, model_path: str):
        self.model = EmbryoGardnerNet()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        
        self.gardner_mapping = {
            'expansion': {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6'},
            'icm': {0: 'A', 1: 'B', 2: 'C'},
            'te': {0: 'A', 1: 'B', 2: 'C'}
        }
    
    async def analyze(self, image, day: int = 5):
        """Analyze embryo using Gardner criteria"""
        input_tensor = self.preprocess_image(image)
        
        with torch.no_grad():
            outputs = self.model(input_tensor)
        
        # Get predictions
        expansion_pred = torch.argmax(outputs['expansion'], dim=1).item()
        icm_pred = torch.argmax(outputs['icm'], dim=1).item()
        te_pred = torch.argmax(outputs['te'], dim=1).item()
        quality_score = outputs['quality'].item()
        
        # Format Gardner grade
        expansion_grade = self.gardner_mapping['expansion'][expansion_pred]
        icm_grade = self.gardner_mapping['icm'][icm_pred]
        te_grade = self.gardner_mapping['te'][te_pred]
        gardner_grade = f"{expansion_grade}{icm_grade}{te_grade}"
        
        return {
            'gardner_grade': gardner_grade,
            'expansion': {
                'grade': int(expansion_grade),
                'description': self.get_expansion_description(int(expansion_grade))
            },
            'inner_cell_mass': {
                'grade': icm_grade,
                'description': self.get_icm_description(icm_grade)
            },
            'trophectoderm': {
                'grade': te_grade,
                'description': self.get_te_description(te_grade)
            },
            'quality_assessment': {
                'overall': self.get_quality_category(quality_score),
                'viability_score': round(quality_score, 3),
                'implantation_potential': self.get_implantation_potential(gardner_grade, quality_score)
            }
        }
```

### Model Training Pipeline
```python
# training/train_sperm_model.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import wandb
from sklearn.metrics import mean_absolute_error, r2_score

class SpermDataLoader:
    def __init__(self, data_dir: str, batch_size: int = 32):
        self.data_dir = data_dir
        self.batch_size = batch_size
        
    def get_dataloaders(self):
        # Custom dataset implementation
        train_dataset = SpermDataset(
            data_dir=f"{self.data_dir}/train",
            transform=self.get_train_transform()
        )
        
        val_dataset = SpermDataset(
            data_dir=f"{self.data_dir}/val",
            transform=self.get_val_transform()
        )
        
        train_loader = DataLoader(
            train_dataset, 
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=4
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=4
        )
        
        return train_loader, val_loader

class SpermTrainer:
    def __init__(self, model, train_loader, val_loader, device='cuda'):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        
        # Multi-task losses
        self.criterion_regression = nn.MSELoss()
        self.criterion_classification = nn.CrossEntropyLoss()
        
        # Optimizer
        self.optimizer = torch.optim.AdamW(
            model.parameters(), 
            lr=1e-4, 
            weight_decay=1e-5
        )
        
        # Scheduler
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=100
        )
    
    def train_epoch(self):
        self.model.train()
        total_loss = 0
        
        for batch_idx, (images, targets) in enumerate(self.train_loader):
            images = images.to(self.device)
            
            # Forward pass
            outputs = self.model(images)
            
            # Calculate multi-task loss
            loss = 0
            loss += self.criterion_regression(
                outputs['concentration'], 
                targets['concentration'].to(self.device)
            )
            loss += self.criterion_classification(
                outputs['motility'], 
                targets['motility'].to(self.device)
            )
            loss += self.criterion_classification(
                outputs['morphology'], 
                targets['morphology'].to(self.device)
            )
            loss += self.criterion_classification(
                outputs['vitality'], 
                targets['vitality'].to(self.device)
            )
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 10 == 0:
                wandb.log({
                    'batch_loss': loss.item(),
                    'learning_rate': self.optimizer.param_groups[0]['lr']
                })
        
        return total_loss / len(self.train_loader)
    
    def validate(self):
        self.model.eval()
        total_loss = 0
        predictions = []
        targets_list = []
        
        with torch.no_grad():
            for images, targets in self.val_loader:
                images = images.to(self.device)
                outputs = self.model(images)
                
                # Calculate loss (same as training)
                loss = self.calculate_loss(outputs, targets)
                total_loss += loss.item()
                
                # Store predictions for metrics
                predictions.append(outputs)
                targets_list.append(targets)
        
        # Calculate metrics
        metrics = self.calculate_metrics(predictions, targets_list)
        
        return total_loss / len(self.val_loader), metrics
    
    def train(self, num_epochs: int):
        wandb.init(project="fertivision-sperm-analysis")
        
        best_val_loss = float('inf')
        
        for epoch in range(num_epochs):
            train_loss = self.train_epoch()
            val_loss, metrics = self.validate()
            
            self.scheduler.step()
            
            # Log metrics
            wandb.log({
                'epoch': epoch,
                'train_loss': train_loss,
                'val_loss': val_loss,
                **metrics
            })
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(
                    self.model.state_dict(), 
                    f'models/sperm_analyzer_best.pth'
                )
            
            print(f"Epoch {epoch}: Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
```

---

## 🗄️ Database Schema

### Core Tables
```sql
-- patients table
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    medical_history JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- analyses table
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    analysis_id VARCHAR(100) UNIQUE NOT NULL,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    analysis_type VARCHAR(50) NOT NULL, -- 'sperm', 'oocyte', 'embryo', 'follicle'
    sample_id VARCHAR(100),
    image_path VARCHAR(500),
    image_metadata JSONB,
    results JSONB NOT NULL,
    confidence_scores JSONB,
    status VARCHAR(20) DEFAULT 'completed',
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by VARCHAR(100)
);

-- treatment_cycles table
CREATE TABLE treatment_cycles (
    id SERIAL PRIMARY KEY,
    cycle_id VARCHAR(100) UNIQUE NOT NULL,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    cycle_type VARCHAR(50), -- 'IVF', 'ICSI', 'FET', 'IUI'
    protocol VARCHAR(100),
    start_date DATE,
    end_date DATE,
    outcome VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- reports table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(100) UNIQUE NOT NULL,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    report_type VARCHAR(50), -- 'clinical', 'research', 'summary'
    analysis_ids JSONB, -- Array of analysis IDs included
    template_used VARCHAR(100),
    file_path VARCHAR(500),
    generated_by VARCHAR(100),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- api_keys table
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    key_id VARCHAR(100) UNIQUE NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    client_name VARCHAR(200),
    permissions JSONB,
    rate_limit INTEGER DEFAULT 1000,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP
);

-- audit_logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    user_id VARCHAR(100),
    api_key_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    request_data JSONB,
    response_status INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Database Indexes
```sql
-- Performance indexes
CREATE INDEX idx_patients_patient_id ON patients(patient_id);
CREATE INDEX idx_analyses_patient_id ON analyses(patient_id);
CREATE INDEX idx_analyses_analysis_type ON analyses(analysis_type);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
CREATE INDEX idx_treatment_cycles_patient_id ON treatment_cycles(patient_id);
CREATE INDEX idx_reports_patient_id ON reports(patient_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);

-- JSONB indexes for better query performance
CREATE INDEX idx_analyses_results_gin ON analyses USING GIN(results);
CREATE INDEX idx_patients_medical_history_gin ON patients USING GIN(medical_history);
```

### Database Migration System
```python
# migrations/env.py
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os

# Import your models
from models import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## 🔒 Security Implementation

### Data Encryption
```python
# security/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class DataEncryption:
    def __init__(self, password: bytes):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher_suite = Fernet(key)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode()

# Usage for PHI encryption
encryption_service = DataEncryption(os.environ.get('ENCRYPTION_KEY').encode())

def encrypt_patient_data(patient_data):
    """Encrypt patient PII/PHI data"""
    encrypted_data = patient_data.copy()
    
    # Encrypt sensitive fields
    if 'first_name' in patient_data:
        encrypted_data['first_name'] = encryption_service.encrypt_data(patient_data['first_name'])
    if 'last_name' in patient_data:
        encrypted_data['last_name'] = encryption_service.encrypt_data(patient_data['last_name'])
    if 'contact_email' in patient_data:
        encrypted_data['contact_email'] = encryption_service.encrypt_data(patient_data['contact_email'])
    
    return encrypted_data
```

### HIPAA Compliance Implementation
```python
# security/hipaa_compliance.py
from datetime import datetime, timedelta
import hashlib
import hmac

class HIPAACompliance:
    def __init__(self):
        self.minimum_necessary = True
        self.access_logging = True
        self.data_retention_days = 2555  # 7 years
    
    def log_phi_access(self, user_id: str, patient_id: str, action: str, reason: str):
        """Log PHI access for audit trail"""
        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'patient_id': self.hash_patient_id(patient_id),
            'action': action,
            'reason': reason,
            'ip_address': self.get_client_ip(),
            'session_id': self.get_session_id()
        }
        
        # Store in secure audit log
        self.store_audit_log(audit_entry)
    
    def hash_patient_id(self, patient_id: str) -> str:
        """Create HIPAA-compliant hash of patient ID"""
        salt = os.environ.get('PATIENT_ID_SALT', 'default_salt')
        return hashlib.pbkdf2_hmac('sha256', 
                                  patient_id.encode(), 
                                  salt.encode(), 
                                  100000).hex()
    
    def check_data_retention(self, created_date: datetime) -> bool:
        """Check if data is within retention period"""
        retention_limit = datetime.utcnow() - timedelta(days=self.data_retention_days)
        return created_date > retention_limit
    
    def anonymize_expired_data(self, record):
        """Anonymize data past retention period"""
        if not self.check_data_retention(record['created_at']):
            # Remove or anonymize PHI
            record['first_name'] = 'ANONYMIZED'
            record['last_name'] = 'ANONYMIZED'
            record['contact_email'] = 'ANONYMIZED'
            record['contact_phone'] = 'ANONYMIZED'
        
        return record
```

### Input Validation and Sanitization
```python
# security/validation.py
from pydantic import BaseModel, validator, EmailStr
from typing import Optional, List
import re

class PatientCreateRequest(BaseModel):
    patient_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    
    @validator('patient_id')
    def validate_patient_id(cls, v):
        if not re.match(r'^[A-Z0-9]{3,20}$', v):
            raise ValueError('Patient ID must be 3-20 alphanumeric characters')
        return v
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if v and not re.match(r'^[a-zA-Z\s\-\']{1,100}$', v):
            raise ValueError('Name contains invalid characters')
        return v
    
    @validator('gender')
    def validate_gender(cls, v):
        if v and v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be male, female, or other')
        return v.lower() if v else v
    
    @validator('contact_phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?[\d\s\-\(\)]{10,20}$', v):
            raise ValueError('Invalid phone number format')
        return v

class ImageAnalysisRequest(BaseModel):
    patient_id: str
    analysis_type: str
    case_id: Optional[str] = None
    
    @validator('analysis_type')
    def validate_analysis_type(cls, v):
        valid_types = ['sperm', 'oocyte', 'embryo', 'follicle']
        if v not in valid_types:
            raise ValueError(f'Analysis type must be one of: {valid_types}')
        return v
    
    @validator('patient_id', 'case_id')
    def validate_ids(cls, v):
        if v and not re.match(r'^[A-Za-z0-9_\-]{1,50}$', v):
            raise ValueError('ID contains invalid characters')
        return v

# File upload validation
def validate_image_file(file: UploadFile) -> bool:
    """Validate uploaded image file"""
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif']
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(400, f"Invalid file type. Allowed: {allowed_extensions}")
    
    # Check MIME type
    allowed_mime_types = ['image/jpeg', 'image/png', 'image/tiff']
    if file.content_type not in allowed_mime_types:
        raise HTTPException(400, f"Invalid MIME type: {file.content_type}")
    
    # Check file size (50MB limit)
    if file.size > 50 * 1024 * 1024:
        raise HTTPException(413, "File too large. Maximum size: 50MB")
    
    return True
```

---

**FertiVision Developer Manual v2.1**  
Last Updated: July 23, 2025  
© 2025 FertiVision Technologies. All rights reserved.

For technical support or additional development resources, contact:  
**FertiVision Development Team**  
Email: dev-support@fertivision.com  
Documentation: https://docs.fertivision.com/developers  
GitHub: https://github.com/satishskid/fertivision-codelm
