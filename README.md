### Dev
```bash
docker compose -f dev-docker-compose.yml up -d
uv sync
fastapi dev src/main.py
```