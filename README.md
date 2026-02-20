![Python](https://img.shields.io/badge/python-3.12-blue.svg?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129-05998b.svg?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ed.svg?style=flat&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.46-red.svg?style=flat)
![Alembic](https://img.shields.io/badge/Alembic-1.18.4-6B4F3B.svg?style=flat)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg?style=flat&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-python--jose-black.svg?style=flat&logo=jsonwebtokens&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-4.4.10-336699.svg?style=flat)
![Pytest](https://img.shields.io/badge/Pytest-8.0-white.svg?style=flat&logo=pytest&logoColor=000000)
![Pytest-Asyncio](https://img.shields.io/badge/Pytest--Asyncio-0.24-00b0ff.svg?style=flat)

# Prana Backend Task: Microservices Architecture

---

## Description
A microservices-based system designed for user management and automated PDF profile generation. The project demonstrates
modern backend development practices, including asynchronous database operations, secure inter-service communication via
JWT, and containerized deployment.

---

## Directory Tree
```text
auth_service/         
├── app/
│   ├── core/          
│   │   ├── config.py  
│   │   └── security.py 
│   ├── database.py     
│   ├── dependencies.py
│   ├── main.py         
│   ├── models.py       
│   ├── repository.py   
│   ├── router.py       
│   ├── schemas.py     
│   └── services.py
├── alembic/            
├── tests/              
├── Dockerfile          
├── requirements.txt    
├── requirements-dev.txt
└── alembic.ini         

pdf_service/            
├── app/
│   ├── core/
│   │   ├── config.py   
│   │   └── security.py
│   ├── dependencies.py
│   ├── main.py         
│   ├── router.py       
│   ├── schemas.py      
│   └── services.py
├── tests/              
├── Dockerfile          
├── requirements.txt    
└── requirements-dev.txt

docker-compose.yml
.env.example
```
---

## System Design

The system is split into two independent services:

1. **Auth Service**:
    - Handles user registration (`signup`) and authentication (`login`).
    - Manages user data storage in PostgreSQL.
    - Issues JWT tokens for authorized access to other system components.

2. **PDF Service**:
    - Generates personalized PDF profile documents.
    - Processes data in-memory using `BytesIO` to avoid unnecessary disk I/O.
    - Features a protected endpoint that validates JWT tokens issued by the Auth Service.

---

## API Endpoints

| Service  | Method | Endpoint        | Description          | Auth Required |
|----------|--------|-----------------|----------------------|---------------|
| **Auth** | POST   | `/auth/signup`  | Register a new user  | No            |
| **Auth** | POST   | `/auth/login`   | Get JWT access token | No            |
| **PDF**  | GET    | `/pdf/generate` | Generate profile PDF | **Yes (JWT)** |

---

## Installation & Setup

### 1. Environment Configuration

Create a `.env` file in the project root and fill in your credentials:

```env
# PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin_password
POSTGRES_DB=database
POSTGRES_HOST=database
POSTGRES_PORT=5432

# JWT / Security
SECRET_KEY=YOUR_SUPER_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 2. Service Deployment

Build the Docker images and launch the infrastructure in detached mode:

```bash
# Build the containers from Dockerfiles
docker compose build

# Start all services in the background
docker compose up -d
```

### 3. Database Migrations

Once the database container is healthy and running, initialize the schema by applying migrations:

```bash
# Apply Alembic migrations to the PostgreSQL database
docker compose exec auth-service alembic upgrade head
```

### 4. Interactive API Documentation

Once the services are active, you can explore and test the endpoints via the built-in Swagger UI:

* **Auth Service API:** [http://localhost:8001/docs](http://localhost:8001/docs)
* **PDF Service API:** [http://localhost:8002/docs](http://localhost:8002/docs)