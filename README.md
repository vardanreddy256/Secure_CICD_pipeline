# 🔐 Secure CI/CD Pipeline

A production-ready, security-hardened CI/CD pipeline for a Python Flask application. Demonstrates industry best practices including automated testing, SAST scanning, container vulnerability scanning, and secret detection — all integrated into GitHub Actions.

---

## 📐 Architecture

```
Code Push / PR
      │
      ▼
┌─────────────────────────┐
│  Job 1: Test & SAST     │  ← pytest + coverage + Bandit
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│  Job 2: Secret Scan     │  ← Gitleaks
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│  Job 3: Build & Push    │  ← Docker build + Trivy + Docker Hub
└─────────────────────────┘
```

Each job must pass before the next runs. A failure in any stage **blocks the deployment**.

---

## 🚀 Features

| Feature | Tool | Description |
|---------|------|-------------|
| ✅ Unit Tests | `pytest` | Full test suite with coverage reporting |
| ✅ SAST | `bandit` | Python static application security testing |
| ✅ Secret Detection | `gitleaks` | Prevents credentials from entering the repo |
| ✅ Container Scanning | `trivy` | Scans Docker image for CRITICAL/HIGH CVEs |
| ✅ Non-root Container | Docker best practice | App runs as `appuser`, not root |
| ✅ Pinned Dependencies | `requirements.txt` | Reproducible, auditable builds |
| ✅ Health Check | `/health` endpoint | Ready for load balancers & monitoring |
| ✅ Env-based Config | `os.getenv` | Zero hardcoded secrets |

---

## 📁 Project Structure

```
Secure_CICD_pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml              # Full CI/CD pipeline
├── app.py                      # Flask application
├── test_app.py                 # pytest test suite
├── Dockerfile                  # Hardened Docker image
├── docker-compose.yml          # Local development
├── requirements.txt            # Pinned prod dependencies
├── requirements-dev.txt        # Dev/test dependencies
├── pyproject.toml              # Tool configuration
├── .env.example                # Environment variable reference
├── .gitignore                  # Excludes secrets & caches
└── .dockerignore               # Lean Docker build context
```

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Secure_CICD_pipeline.git
cd Secure_CICD_pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Set environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

### 5. Run the app locally

```bash
python app.py
# App running at http://localhost:5000
```

### 6. Run with Docker Compose

```bash
docker-compose up --build
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Run SAST scan locally
bandit -r app.py
```

---

## 🔑 GitHub Secrets Required

Go to **Settings → Secrets and variables → Actions** and add:

| Secret Name | Description |
|-------------|-------------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub access token |

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | App info (name, status, environment) |
| `GET` | `/health` | Health check for monitoring |

### Example Responses

**`GET /`**
```json
{
  "app": "Secure Python App",
  "status": "running",
  "environment": "production"
}
```

**`GET /health`**
```json
{
  "status": "healthy"
}
```

---

## 🔒 Security Practices Applied

- **No hardcoded secrets** — all config via environment variables
- **Non-root Docker user** — container runs as `appuser`
- **Slim base image** — `python:3.11-slim` minimizes attack surface
- **Dependency pinning** — prevents supply chain drift
- **SAST on every push** — Bandit catches common Python vulnerabilities
- **Secret scanning** — Gitleaks blocks credential leaks before merge
- **CVE scanning** — Trivy blocks images with CRITICAL/HIGH vulnerabilities
- **No push on PR** — Docker Hub push only happens on `main` branch merge

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
