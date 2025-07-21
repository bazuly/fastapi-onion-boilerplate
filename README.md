# Fastapi onion architecture boilerplate

> **This repository is an architectural example of a modern FastAPI application.**
> 
> The main goal is to demonstrate a clean, maintainable backend structure (Onion Architecture) and integration with popular technologies. **All technologies are optional** — use only what fits your needs!

---

## 🛠️ Technologies Used

- **FastAPI** — Modern, async Python web framework
- **SQLAlchemy** — Async ORM for PostgreSQL
- **Kafka** — Event streaming platform (via aiokafka)
- **MongoDB** — NoSQL database for logging and caching
- **Redis** — Caching layer (via fastapi-cache2)
- **fastapi-users** — User authentication and management
- **uv** — Fast dependency management and runner
- **Makefile** — Unified commands for development, testing, and deployment
- **factory_boy** — Factories for robust and isolated testing

---

## 🧅 Onion Architecture

The project follows the principles of Onion (Clean) Architecture:
- **Domain Layer** — Business logic and models
- **Service Layer** — Application use cases
- **Infrastructure Layer** — Database, external services, Kafka, Redis, MongoDB
- **API Layer** — FastAPI routers and endpoints

This separation ensures testability, scalability, and maintainability.

---

## 🚀 Quick Start (with Makefile)

1. **Clone the repository:**
   ```sh
   git clone <repo_url>
   cd fastapi-kafka-example
   ```
2. **Copy and edit environment variables:**
   ```sh
   cp .env.example .env
   # Edit .env as needed
   ```
3. **Run the application (all services):**
   ```sh
   make build         # Build and start all containers
   # or
   make build-background  # Start in background
   ```
4. **Stop all containers:**
   ```sh
   make down
   ```
5. **Run tests:**
   ```sh
   make test
   ```
6. **Database migrations:**
   ```sh
   make migrate-create MIGRATION="message"  # Create new migration
   make migrate-apply                        # Apply migrations
   ```

---

## 📚 Main Endpoints

### Applications
- `POST   /applications` — Create new application
- `GET    /applications` — List applications (pagination)
- `GET    /applications/by-title/{title}` — Find by title
- `GET    /applications/{application_id}` — Get by ID
- `PATCH  /applications/{application_id}` — Update application
- `DELETE /applications/{application_id}` — Delete application

### Image Upload
- `POST   /image_upload/image_upload` — Upload image
- `GET    /image_upload/image_get/{image_id}` — Get image info
- `DELETE /image_upload/image_delete/{image_id}` — Delete image

### Authentication & Users (fastapi-users)
- `POST   /auth/register` — Register new user
- `POST   /auth/jwt/login` — Login (JWT)
- `GET    /users/me` — Get current user info
- `PATCH  /users/{id}` — Update user

---

## 📦 Project Structure (Onion Example)

```
app/
  applications/      # Business logic (domain, service, repository, schemas)
  image_upload/      # Image upload logic
  users/             # User management & auth
  broker/            # Kafka consumer/producer
  infrastructure/    # DB, MongoDB, Redis access
  main.py            # FastAPI app, routers
```

---

## 📝 Notes
- This is a **learning/architecture example** — not production ready out of the box.
- All integrations (Kafka, MongoDB, Redis, etc.) are optional and can be swapped or removed.
- The codebase is designed for easy testing and extension.

---

## 🤝 Contributing
Pull requests and suggestions are welcome! If you spot a bug or want to improve the architecture, feel free to open an issue or PR.

