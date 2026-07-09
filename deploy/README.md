# Deploy Assets

This directory contains container and hosted deployment assets for `open-geoserver-mcp`.

## Files

- `Dockerfile`: container image build definition
- `docker-compose.yml`: local or hosted Compose deployment
- `.env.example`: environment template used with Compose

## Typical Usage

Copy the environment template:

```bash
cp deploy/.env.example deploy/.env
```

Start with Compose:

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up --build -d
```

Build only:

```bash
docker build -f deploy/Dockerfile -t open-geoserver-mcp:local .
```
