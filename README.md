![Python](https://img.shields.io/badge/python-3.12-geen.svg?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-05998b.svg?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ed.svg?style=flat&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-red.svg?style=flat)
![Alembic](https://img.shields.io/badge/Alembic-1.14.0-6B4F3B.svg?style=flat)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg?style=flat&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-python--jose-black.svg?style=flat&logo=jsonwebtokens&logoColor=white)
![AWS SQS](https://img.shields.io/badge/AWS_SQS-LocalStack-FF9900.svg?style=flat&logo=amazonsqs&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS_S3-LocalStack-569A31.svg?style=flat&logo=amazons3&logoColor=white)
![Aioboto3](https://img.shields.io/badge/Aioboto3-Async_AWS-blue.svg?style=flat)
![ReportLab](https://img.shields.io/badge/ReportLab-4.2.5-336699.svg?style=flat)
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
│   ├── worker.py   
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
    - Asynchronous Task Queuing: Offloads long-running generation tasks to AWS SQS as a producer, allowing a background
      worker to handle the workload without blocking the API.
    - Cloud Storage Integration: Automatically uploads completed documents to AWS S3, making them accessible via the
      predictable URL pattern:
      http://localhost:4566/user-pdfs/profile_{user_id}.pdf

---

## API Endpoints

| Service  | Method | Endpoint               | Description                     | Auth Required |
|----------|--------|------------------------|---------------------------------|---------------|
| **Auth** | POST   | `api/auth/signup`      | Register a new user             | No            |
| **Auth** | POST   | `api/auth/login`       | Get JWT access token            | No            |
| **PDF**  | GET    | `api/pdf/download`     | Generate profile PDF            | **Yes (JWT)** |
| **PDF**  | POST   | `api/pdf/upload-to-s3` | Triggers background generation. | **Yes (JWT)** |

---

## Installation & Setup

### 1. Environment Configuration

Create a `.env` file in the project root and fill in your credentials:

```env
# --- PostgreSQL ---
POSTGRES_USER=example_user
POSTGRES_PASSWORD=example_password
POSTGRES_DB=example_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# --- JWT / Security ---
SECRET_KEY=example_secret_key_hex_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# --- AWS ---
AWS_ENDPOINT_URL=http://localstack:4566
AWS_ACCESS_KEY_ID=example_aws_access_key_id
AWS_SECRET_ACCESS_KEY=example_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1

# --- Service Specific ---
SQS_QUEUE_NAME=example-pdf-tasks-queue
S3_BUCKET_NAME=example-user-pdfs-bucket
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
# Generate an initial Alembic revision from your SQLAlchemy models
docker compose run --rm auth_service alembic revision --autogenerate -m "initial schema"

# Apply the generated migration to the database
docker compose exec auth_service alembic upgrade head
```

### 4. Interactive API Documentation

Once the services are active, you can explore and test the endpoints via the built-in Swagger UI:

* **Auth Service API:** [http://localhost:8001/docs](http://localhost:8001/docs)
* **PDF Service API:** [http://localhost:8002/docs](http://localhost:8002/docs)