# Load Balancer Proofs - Nginx Load Balancing System

A production-ready load balancing system using Nginx to distribute traffic across multiple FastAPI backend services. This project demonstrates weighted load balancing, health checks, resource limits, and stress testing capabilities.

- ⚖️ Load Balancing, 🏥 Health Checks, 🔒 Resource Limits, 🏗️ Domain Driven Design, 🧪 Unit Testing, 🏗️ Clean Architecture, 🔄 Stress Testing
- 🐳 Docker, 🔀 Nginx, 🟩 FastAPI, 🟦 Python, 🛡️ Pydantic, 🧪 Pytest, 📊 Requests, 🖥️ Bash/Zsh, 📦 Docker Compose

## 📋 Table of Contents

- [Overview](#overview)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Load Balancer Configuration](#load-balancer-configuration)
- [Backend Services](#backend-services)
- [Deployment](#deployment)
- [Execution](#execution)
- [Monitoring](#monitoring)
- [Stress Testing](#stress-testing)
- [Docker Commands Reference](#docker-commands-reference)

## 🎯 Overview

This project implements a load-balanced API system with:

- **Nginx** as the load balancer (port 8080)
- **3 FastAPI backend services** (back-01, back-02, back-03) running on ports 8001, 8002, 8003
- **Weighted load distribution** to optimize resource usage
- **Health checks** for automatic failure detection
- **Resource limits** for controlled resource allocation
- **Stress testing tools** for performance validation

## 🚀 Technologies

### Core Technologies

- 🐳 **Docker** - Containerization and orchestration
- 🔀 **Nginx** - Load balancer and reverse proxy
- 🟩 **FastAPI** - High-performance Python web framework
- 🟦 **Python 3.12** - Backend programming language
- 🛡️ **Pydantic** - Data validation and settings management

### Development & Testing

- 🧪 **Pytest** - Unit and integration testing framework
- 📊 **Requests** - HTTP stress testing library
- 🖥️ **Bash/Zsh** - Shell scripting and automation

### Architecture & Patterns

- 🏗️ **Domain Driven Design** - Business logic organization
- ⚖️ **Load Balancing** - Weighted round-robin distribution
- 🏥 **Health Checks** - Automatic failure detection
- 🔒 **Resource Limits** - CPU and memory constraints

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │  Nginx (8080)   │
                    │  Load Balancer  │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  back-01     │ │  back-02     │ │  back-03     │
    │  Port: 8001  │ │  Port: 8002  │ │  Port: 8003  │
    │  Weight: 1   │ │  Weight: 2   │ │  Weight: 3   │
    │  CPU: 0.125  │ │  CPU: 0.250  │ │  CPU: 0.250  │
    │  RAM: 64M    │ │  RAM: 128M   │ │  RAM: 256M   │
    └──────────────┘ └──────────────┘ └──────────────┘
```

## ⚖️ Load Balancer Configuration

### Nginx Configuration (`load_balancer/nginx.conf`)

The load balancer uses **weighted round-robin** distribution:

```nginx
upstream backend {
    server back-01:8000 weight=1;  # Receives 1/6 of requests
    server back-02:8000 weight=2;  # Receives 2/6 of requests
    server back-03:8000 weight=3;  # Receives 3/6 of requests (50%)
}
```

### Key Configuration Parameters

| Parameter            | Value            | Description                               |
| -------------------- | ---------------- | ----------------------------------------- |
| `worker_processes`   | `auto`           | Automatically set based on CPU cores      |
| `worker_connections` | `1024`           | Max simultaneous connections per worker   |
| `listen`             | `80`             | Internal port (mapped to 8080 externally) |
| `proxy_pass`         | `http://backend` | Forwards requests to backend upstream     |

### Load Distribution Logic

With weights 1:2:3:

- **back-01**: ~16.7% of traffic (1/6)
- **back-02**: ~33.3% of traffic (2/6)
- **back-03**: ~50.0% of traffic (3/6)

This allows back-03 to handle more load due to higher resource allocation.

### Health Check Endpoints

- **Nginx health**: `http://localhost:8080/nginx-health`
- **Backend health**: Each backend has a `/health` endpoint checked every 30s

## 🔧 Backend Services

### Service Specifications

| Service | Container | Port | CPU Limit   | Memory Limit | Weight | HOST_TAG |
| ------- | --------- | ---- | ----------- | ------------ | ------ | -------- |
| back-01 | back-01   | 8001 | 0.125 cores | 64M          | 1      | back-01  |
| back-02 | back-02   | 8002 | 0.250 cores | 128M         | 2      | back-02  |
| back-03 | back-03   | 8003 | 0.250 cores | 256M         | 3      | back-03  |

### API Endpoints

#### POST `/models`

Creates a LEGO model with validation.

**Request Body:**

```json
{
  "name": "Starship Enterprise",
  "pieces": 1599,
  "theme": "Sci-Fi",
  "difficulty": "easy",
  "price_us": 199.99,
  "year": 2001
}
```

**Response:**

```json
{
  "host": "tag: back-01 - 172.18.0.2",
  "success": true,
  "message": "Item created successfully",
  "data": { ... }
}
```

### Environment Variables

Each backend service has:

- `PYTHONUNBUFFERED=1`: Ensures real-time log output
- `HOST_TAG`: Unique identifier for tracking request distribution

### Health Check Configuration

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🚀 Deployment

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- Python 3.12+ (for stress testing)

### Build and Start Services

```bash
# Build all services
docker-compose build

# Start all services in detached mode
docker-compose up -d

# Start specific services
docker-compose up -d back-01 back-02 nginx

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f back-01
```

### Stop and Remove Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop back-01
```

## 🎮 Execution

### Starting the System

1. **Start all services:**

   ```bash
   docker-compose up -d
   ```

2. **Verify services are running:**

   ```bash
   docker-compose ps
   ```

3. **Check nginx health:**

   ```bash
   curl http://localhost:8080/nginx-health
   ```

4. **Test load balancing:**
   ```bash
   curl -X POST http://localhost:8080/models \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test Model",
       "pieces": 100,
       "theme": "City",
       "difficulty": "easy",
       "price_us": 29.99,
       "year": 2023
     }'
   ```

### Access Individual Backends

```bash
# Direct access to back-01
curl http://localhost:8001/

# Direct access to back-02
curl http://localhost:8002/

# Direct access to back-03
curl http://localhost:8003/
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart back-01

# Rebuild and restart
docker-compose up -d --build
```

## 📊 Monitoring

### View Service Status

```bash
# List all containers
docker-compose ps

# View resource usage (CPU, Memory, Network, I/O)
docker stats

# View specific service stats
docker stats back-01 back-02 back-03 nginx
```

### Check Logs

```bash
# Follow all logs
docker-compose logs -f

# Follow specific service
docker-compose logs -f nginx

# Last 100 lines
docker-compose logs --tail=100 back-01

# Logs with timestamps
docker-compose logs -f -t
```

### Enter a Running Container

```bash
# Enter back-01 container
docker-compose exec back-01 /bin/bash

# Enter nginx container
docker-compose exec nginx /bin/sh

# Execute command without entering
docker-compose exec back-01 ls -la
```

### Monitor Nginx Access Logs

```bash
# View nginx access logs
docker-compose exec nginx tail -f /var/log/nginx/access.log

# View nginx error logs
docker-compose exec nginx tail -f /var/log/nginx/error.log
```

### Health Check Status

```bash
# Check docker health status
docker inspect --format='{{.State.Health.Status}}' back-01

# View health check logs
docker inspect --format='{{json .State.Health}}' back-01 | jq
```

### Resource Monitoring

```bash
# Real-time resource usage
docker stats --no-stream

# Get current resource limits
docker inspect back-03 | jq '.[0].HostConfig.NanoCpus'
docker inspect back-03 | jq '.[0].HostConfig.Memory'
```

## 🔥 Stress Testing

### Using the Stress Test Script

The project includes `sender_requests.py` for load testing the system.

#### Configuration

```python
url = "http://localhost:8080/models"
total_requests = 20000      # Total number of requests
concurrency = 10000          # Concurrent requests
```

#### Running the Test

```bash
# Install dependencies
pip install requests

# Run stress test
python sender_requests.py
```

#### Expected Output

```
Current host distribution:
    - tag: back-01 - 172.18.0.2: 3334
    - tag: back-02 - 172.18.0.3: 6666
    - tag: back-03 - 172.18.0.4: 10000

Load Balancer Host Distribution
    - total request sent 20000
    - total request completed 20000
```

### Stress Testing Scenarios

#### 1. Baseline Performance Test

```python
total_requests = 1000
concurrency = 100
```

Tests normal load with moderate concurrency.

#### 2. High Concurrency Test

```python
total_requests = 10000
concurrency = 5000
```

Tests system under high concurrent load.

#### 3. Sustained Load Test

```python
total_requests = 50000
concurrency = 1000
```

Tests system stability over extended periods.

#### 4. Spike Test

```python
total_requests = 20000
concurrency = 10000
```

Tests system response to sudden traffic spikes.

### Analyzing Results

#### Distribution Verification

The distribution should approximate the weight ratio (1:2:3):

- back-01: ~16-17% of requests
- back-02: ~33-34% of requests
- back-03: ~49-50% of requests

#### Performance Metrics to Monitor

```bash
# During stress test, monitor:
docker stats

# Check for:
# - CPU usage patterns
# - Memory consumption
# - Network I/O
# - Container restarts (should be 0)
```

#### Response Time Analysis

Modify `sender_requests.py` to track response times:

```python
import time

def send_request(i):
    start = time.time()
    response = requests.post(url, json=payload)
    elapsed = time.time() - start
    # Track elapsed time for analysis
```

### Stress Testing Best Practices

1. **Start Small**: Begin with low request counts and increase gradually
2. **Monitor Resources**: Watch CPU/memory during tests
3. **Check Health**: Verify health checks remain stable
4. **Review Logs**: Check for errors in backend logs
5. **Gradual Increase**: Increase load incrementally to find breaking points

### Troubleshooting During Stress Tests

```bash
# If services become unresponsive:
docker-compose restart

# If memory issues occur:
docker-compose down
docker system prune -a

# Check for container restarts:
docker-compose ps

# View recent errors:
docker-compose logs --tail=50 | grep -i error
```

## 🐳 Docker Commands Reference

### Service Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a service
docker-compose restart <service_name>

# Rebuild and start
docker-compose up -d --build

# Scale a service (if configured)
docker-compose up -d --scale back-01=3
```

### Container Inspection

```bash
# List containers
docker-compose ps

# Inspect container
docker inspect <container_name>

# View container logs
docker-compose logs <service_name>

# Execute command in container
docker-compose exec <service_name> <command>

# Enter container shell
docker-compose exec <service_name> /bin/bash
```

### Resource Management

```bash
# View resource usage
docker stats

# View disk usage
docker system df

# Clean up
docker system prune -a

# Remove volumes
docker volume prune
```

### Networking

```bash
# List networks
docker network ls

# Inspect network
docker network inspect load-balancer-proofs_default

# View container IPs
docker-compose exec back-01 hostname -i
```

## 📝 Configuration Files

### Key Files

- `docker-compose.yml`: Service definitions and configuration
- `load_balancer/nginx.conf`: Nginx load balancer configuration
- `back/Dockerfile`: Backend service image definition
- `back/main.py`: FastAPI application entry point
- `back/requirements.txt`: Python dependencies
- `sender_requests.py`: Stress testing script

## 🛠️ Troubleshooting

### Common Issues

#### Services won't start

```bash
# Check logs
docker-compose logs

# Verify ports are available
netstat -tulpn | grep -E '8080|8001|8002|8003'

# Rebuild images
docker-compose down && docker-compose up -d --build
```

#### Load balancer not distributing correctly

```bash
# Verify nginx config
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload

# Check backend connectivity
docker-compose exec nginx ping back-01
```

#### High memory usage

```bash
# Check current usage
docker stats

# Adjust limits in docker-compose.yml
# Restart services
docker-compose down && docker-compose up -d
```

## 📄 License

This project is for educational purposes.

---

**Author**: jcarloshg  
**Repository**: [load-balancers-nginx](https://github.com/jcarloshg/load-balancers-nginx)
