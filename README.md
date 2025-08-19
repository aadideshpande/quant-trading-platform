# Real-Time Portfolio Dashboard (Docker)

React UI + microservices for a trading system. The dashboard shows holdings, total value, and recent trades; the **Trade Ticket** lets you place BUY/SELL orders via the order service.

---

## Quick Start

```bash
# 1) Build & run all services
docker compose up --build

# 2) Open the UI
# (React dev server inside container maps to your host)
http://localhost:3000
```

> This README matches the provided `docker-compose.yml` (paths under `./services/...` and a single Postgres for the order service).

---

## Services (from compose)

| Service               | Build Context                  | Ports (host→container) | Notes                                                                       |
| --------------------- | ------------------------------ | ---------------------- | --------------------------------------------------------------------------- |
| **dashboard-ui**      | `./services/dashboard-ui`      | `3000:3000`            | React dev server; hot reload enabled (volume + `CHOKIDAR_USEPOLLING=true`). |
| **order-service**     | `./services/order-service`     | `8000:8000`            | Exposes `POST /order`. Depends on `order-db` and `rabbitmq`.                |
| **portfolio-service** | `./services/portfolio-service` | `8002:8002`            | Should expose `GET /portfolio` and `GET /trades`. Depends on `rabbitmq`.    |
| **price-service**     | `./services/price-service`     | `8001:8001`            | Price publisher/HTTP. Depends on `rabbitmq`.                                |
| **rabbitmq**          | image `rabbitmq:3-management`  | `5672`, `15672`        | AMQP + management UI at `http://localhost:15672` (guest/guest).             |
| **order-db**          | image `postgres:15`            | `5433:5432`            | DB for order-service only. Data volume: `order-db-data`.                    |

> If portfolio/price services also need databases, add them similarly to compose.

---

## Environment

Your compose uses **per-service `.env` files** (via `env_file`) for the three backend services. Create these files if they don't exist.

### `./services/order-service/.env`

```
DATABASE_URL=postgresql://order_user:password@order-db:5432/order_db
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
CORS_ORIGINS=http://localhost:3000
```

### `./services/portfolio-service/.env`

```
# Example variables; adjust to your service code
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
PRICE_API_URL=http://price-service:8001
# DATABASE_URL=... (add if portfolio-service persists state)
```

### `./services/price-service/.env`

```
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
# DATABASE_URL=... (add if price-service persists state)
```

### UI configuration (`dashboard-ui`)

React reads variables prefixed with `REACT_APP_` at **build** time. Since the UI runs in a container and your browser talks to published host ports, point the UI to `localhost`:

Create `./services/dashboard-ui/.env`:

```
REACT_APP_ORDER_API_URL=http://localhost:8000
REACT_APP_PORTFOLIO_API_URL=http://localhost:8002
```

Then make sure compose mounts it (either via `env_file:` or keep it auto-read by CRA if your Dockerfile copies `.env`). Easiest is to add to the `dashboard-ui` service in compose:

```yaml
dashboard-ui:
  environment:
    - CHOKIDAR_USEPOLLING=true
    - REACT_APP_ORDER_API_URL=http://localhost:8000
    - REACT_APP_PORTFOLIO_API_URL=http://localhost:8002
```

---

## Endpoints & Contract

### Order Service

```http
POST /order
Content-Type: application/json
{
  "symbol": "<string>",
  "side": "BUY" | "SELL",
  "quantity": <number>
}
```

**Smoke test**

```bash
curl -X POST http://localhost:8000/order \
  -H 'Content-Type: application/json' \
  -d '{"symbol":"GOOG","side":"BUY","quantity":4}'
```

### Portfolio Service (expected)

```http
GET /portfolio   # returns { portfolio: [...], total_value: <number> }
GET /trades      # returns array of recent trades
```

---

## Development Notes

* **Hot reload (UI):** your compose mounts `./services/dashboard-ui:/app` and uses `npm start` with polling to ensure changes reflect.
* **Trade Ticket:** `src/components/TradeTicket.tsx` posts to `REACT_APP_ORDER_API_URL + /order` (the component currently defaults to `http://localhost:8000`).
* **Auto-refresh:** `App.tsx` fetches portfolio/trades every 5s.

---

## Troubleshooting

* **Blank dashboard / CORS:** Ensure `REACT_APP_*` URLs are set and `CORS_ORIGINS` includes `http://localhost:3000` on backends.
* **RabbitMQ UI not reachable:** Confirm `15672:15672` mapping and container is healthy.
* **DB connection errors:** Verify `order-db` is up and the `DATABASE_URL` host is `order-db` (container name), not `localhost`.
* **Network from browser vs. containers:** The browser hits `localhost:8xxx`. Inside containers, services talk to each other via their **service names** (e.g., `http://order-service:8000`).

---

## Commands Cheat Sheet

```bash
# Build & run
docker compose up --build

# Rebuild a single service
docker compose build order-service && docker compose up -d order-service

# View logs
docker compose logs -f order-service

# RabbitMQ UI
open http://localhost:15672
```

---

## License

MIT

# Real-Time Portfolio Dashboard (Docker)

React UI + microservices for a trading system. The dashboard shows holdings, total value, and recent trades; the **Trade Ticket** lets you place BUY/SELL orders via the order service.

---

## Quick Start

```bash
# 1) Build & run all services
docker compose up --build

# 2) Open the UI
# (React dev server inside container maps to your host)
http://localhost:3000
```

> This README matches the provided `docker-compose.yml` (paths under `./services/...` and a single Postgres for the order service).

---

## Services (from compose)

| Service               | Build Context                  | Ports (host→container) | Notes                                                                       |
| --------------------- | ------------------------------ | ---------------------- | --------------------------------------------------------------------------- |
| **dashboard-ui**      | `./services/dashboard-ui`      | `3000:3000`            | React dev server; hot reload enabled (volume + `CHOKIDAR_USEPOLLING=true`). |
| **order-service**     | `./services/order-service`     | `8000:8000`            | Exposes `POST /order`. Depends on `order-db` and `rabbitmq`.                |
| **portfolio-service** | `./services/portfolio-service` | `8002:8002`            | Should expose `GET /portfolio` and `GET /trades`. Depends on `rabbitmq`.    |
| **price-service**     | `./services/price-service`     | `8001:8001`            | Price publisher/HTTP. Depends on `rabbitmq`.                                |
| **rabbitmq**          | image `rabbitmq:3-management`  | `5672`, `15672`        | AMQP + management UI at `http://localhost:15672` (guest/guest).             |
| **order-db**          | image `postgres:15`            | `5433:5432`            | DB for order-service only. Data volume: `order-db-data`.                    |

> If portfolio/price services also need databases, add them similarly to compose.

---

## Environment

Your compose uses **per-service `.env` files** (via `env_file`) for the three backend services. Create these files if they don't exist.

### `./services/order-service/.env`

```
DATABASE_URL=postgresql://order_user:password@order-db:5432/order_db
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
CORS_ORIGINS=http://localhost:3000
```

### `./services/portfolio-service/.env`

```
# Example variables; adjust to your service code
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
PRICE_API_URL=http://price-service:8001
# DATABASE_URL=... (add if portfolio-service persists state)
```

### `./services/price-service/.env`

```
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
# DATABASE_URL=... (add if price-service persists state)
```

### UI configuration (`dashboard-ui`)

React reads variables prefixed with `REACT_APP_` at **build** time. Since the UI runs in a container and your browser talks to published host ports, point the UI to `localhost`:

Create `./services/dashboard-ui/.env`:

```
REACT_APP_ORDER_API_URL=http://localhost:8000
REACT_APP_PORTFOLIO_API_URL=http://localhost:8002
```

Then make sure compose mounts it (either via `env_file:` or keep it auto-read by CRA if your Dockerfile copies `.env`). Easiest is to add to the `dashboard-ui` service in compose:

```yaml
dashboard-ui:
  environment:
    - CHOKIDAR_USEPOLLING=true
    - REACT_APP_ORDER_API_URL=http://localhost:8000
    - REACT_APP_PORTFOLIO_API_URL=http://localhost:8002
```

---

## Endpoints & Contract

### Order Service

```http
POST /order
Content-Type: application/json
{
  "symbol": "<string>",
  "side": "BUY" | "SELL",
  "quantity": <number>
}
```

**Smoke test**

```bash
curl -X POST http://localhost:8000/order \
  -H 'Content-Type: application/json' \
  -d '{"symbol":"GOOG","side":"BUY","quantity":4}'
```

### Portfolio Service (expected)

```http
GET /portfolio   # returns { portfolio: [...], total_value: <number> }
GET /trades      # returns array of recent trades
```

---

## Development Notes

* **Hot reload (UI):** your compose mounts `./services/dashboard-ui:/app` and uses `npm start` with polling to ensure changes reflect.
* **Trade Ticket:** `src/components/TradeTicket.tsx` posts to `REACT_APP_ORDER_API_URL + /order` (the component currently defaults to `http://localhost:8000`).
* **Auto-refresh:** `App.tsx` fetches portfolio/trades every 5s.

---

## Troubleshooting

* **Blank dashboard / CORS:** Ensure `REACT_APP_*` URLs are set and `CORS_ORIGINS` includes `http://localhost:3000` on backends.
* **RabbitMQ UI not reachable:** Confirm `15672:15672` mapping and container is healthy.
* **DB connection errors:** Verify `order-db` is up and the `DATABASE_URL` host is `order-db` (container name), not `localhost`.
* **Network from browser vs. containers:** The browser hits `localhost:8xxx`. Inside containers, services talk to each other via their **service names** (e.g., `http://order-service:8000`).

---

## Commands Cheat Sheet

```bash
# Build & run
docker compose up --build

# Rebuild a single service
docker compose build order-service && docker compose up -d order-service

# View logs
docker compose logs -f order-service

# RabbitMQ UI
open http://localhost:15672
```

---

## License

MIT
Test trigger on Tue Aug 19 15:21:27 CDT 2025
