# Pharma Classifier

## Docker Compose Ports
- API exposed on host port **18000** (mapped to container 8000)
- Frontend exposed on host port **18100** (mapped to container 5173)

Update `docker-compose.yml` if different ports are required, and make sure `VITE_API_URL` matches the API host port.
