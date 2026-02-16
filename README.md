# Simple API

This project now includes a tiny runnable HTTP API using only the Python standard library.

## Run

```bash
python main.py
```

Optional environment variables:
- `HOST` (default: `127.0.0.1`)
- `PORT` (default: `8000`)

## Endpoints

- `GET /` -> API status message
- `GET /health` -> `{"status":"ok","service":"simple-api"}`
- `GET /api/hello?name=you` -> `{"message":"Hello, you!"}`
- `POST /api/echo` with JSON body -> returns the same payload inside `received`

Example:

```bash
curl http://127.0.0.1:8000/api/hello?name=alice
curl -H 'Content-Type: application/json' -d '{"x":1}' http://127.0.0.1:8000/api/echo
```
