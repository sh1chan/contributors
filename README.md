Contributors is a web application designed to streamline open-source contribution by improving how developers discover and share coding tasks.
Built to address the limitations of issue discovery on code hosting platforms with integrated issue trackers,
it enables users to curate, tag, and submit contribution-friendly issues—helping developers quickly find clear,
actionable opportunities to collaborate when they’re ready to contribute.
### Dev
```bash
docker compose -f dev-docker-compose.yml up -d
uv sync
fastapi dev src/main.py
```

### Screenshots
<p align="center"><img src="./docs/_readme/page-issues.png" /></p>