# Running Doccano with Docker

This guide explains how to run doccano using Docker and Docker Compose, including the steps needed to ensure export functionality.

## 1. Clone the Repository

```bash
git clone https://github.com/doccano/doccano.git
cd doccano
```

## 2. Build and Start the Containers

```bash
docker compose -f docker/docker-compose.yml up --build
```

This will start:
- The Django backend
- The frontend UI
- The Celery worker (required for export)
- Redis (for task queue)

## 3. Access the Web UI

Open [http://localhost:8000](http://localhost:8000) in your browser.

## 4. Create a Superuser

In a new terminal, run:
```bash
docker compose -f docker/docker-compose.yml exec backend python manage.py createsuperuser
```

## 5. Use Doccano

- Log in with your superuser credentials.
- Create a project, import data, annotate, and export.

## 6. Stopping Doccano

To stop all services:
```bash
docker compose -f docker/docker-compose.yml down
```

---

## Troubleshooting

- **Export not working?**  
  The Celery worker must be running (it is included in the default Docker Compose setup).  
  If you see no exported file, check the logs of the `worker` service:
  ```bash
  docker compose -f docker/docker-compose.yml logs worker
  ```
- **Persistent data:**  
  By default, the database is stored in a Docker volume for persistence between runs.

---

## References

- [Django backend (source)](https://github.com/doccano/doccano/tree/master/backend)
- [Frontend (source)](https://github.com/doccano/doccano/tree/master/frontend)
- [Original README](../README.md)
