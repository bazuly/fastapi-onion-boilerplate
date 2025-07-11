# FastAPI Application Service

An example microservice built on FastAPI using PostgresSQL, Docker and Kafka.

Goals:
- Complete tests


## 🚀 Quick start

### Requirements

- Docker
- Docker Compose
- Kafka
- Make utils (Does not support Windows)
- Python 3.11+

### Installation and launch

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/fastAPI-kafka-example.git
   cd fastAPI-kafka-example
   cp .env.example .env
   docker-compose up -d --build
   docker-compose exec web alembic upgrade head
   docker-compose exec web alembic revision --autogenerate -m "migration_name"
    
2. Web service will be : http://localhost:8000/docs/

3. Test boilerplate app:
   ```bash
   docker compose - docker-compose-test.yaml up --build

🛠 Techs

    FastAPI - web framework

    PostgreSQL - main database 

    Alembic - magration service

    Kafka - event processing

    Docker - containerization

    AsyncPG - async driver for PostgreSQL


🐳 Docker Compose

Service:

    web - FastAPI app (port 8000)
    db - PostgreSQL (port 5432)
    kafka - Kafka broker (port 9092)
    zookeeper - Zookeeper for Kafka (port 2181)


## 📚 API Documentation

### Authentication Endpoints

#### Register User
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

#### Login
```bash
POST /auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```bash
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

### Applications API

#### Create Application
```bash
POST /applications/applications
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "My Application",
  "description": "This is a sample application"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "My Application",
  "description": "This is a sample application",
  "created_at": "2024-01-15T10:30:00Z",
  "kafka_status": true
}
```

#### Get All Applications (with pagination)
```bash
GET /applications/applications?page=1&size=10
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "My Application",
    "description": "This is a sample application",
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Another App",
    "description": "Another sample application",
    "created_at": "2024-01-15T11:00:00Z"
  }
]
```

#### Get Application by ID
```bash
GET /applications/applications/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": 1,
  "title": "My Application",
  "description": "This is a sample application",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Search Applications by Title
```bash
GET /applications/applications/by-title/My%20Application
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "My Application",
    "description": "This is a sample application",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Update Application
```bash
PATCH /applications/applications/1?new_title=Updated%20Title&new_description=Updated%20description
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Delete Application
```bash
DELETE /applications/applications/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:** `200 OK` (empty body)

### Image Upload API

#### Upload Image
```bash
POST /image_upload/image_upload
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: multipart/form-data

image=@/path/to/your/image.jpg
```

**Response:**
```json
{
  "id": 1,
  "filename": "image.jpg",
  "size": 1024.5,
  "upload_date": "2024-01-15T10:30:00Z",
  "kafka_status": true
}
```

#### Get Image by ID
```bash
GET /image_upload/image_get/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "filename": "image.jpg",
  "size": 1024.5
}
```

#### Delete Image
```bash
DELETE /image_upload/image_delete/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:** `200 OK` (empty body)

## 🔧 Error Responses

### Common Error Formats

#### 401 Unauthorized
```json
{
  "detail": "Unauthorized"
}
```

#### 403 Forbidden
```json
{
  "detail": "Forbidden"
}
```

#### 404 Not Found
```json
{
  "detail": "Not found"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Additional docs:

- https://docs.python.org/3/howto/logging.html Python logger
- https://docs.pydantic.dev/latest/ Pydantic
- https://fastapi-users.github.io/fastapi-users/latest/ FastAPI users
- https://docs.python.org/3/library/asyncio.html asyncio python
