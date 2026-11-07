# nginx-sticky-app

A Python (Flask) web app running as several identical containers behind an
nginx load balancer, with a MySQL database. nginx keeps each browser on the
same container for 5 minutes, using a cookie that the app itself creates.

## Architecture

```
browser -> nginx :80 -> app (3 replicas, port 5000) -> MySQL
```

- **nginx** - the only service with a port on the host (80). Routes each
  request by the `server_ip` cookie, or round robin when there is none.
- **app** - Flask app, 3 replicas by default. Built from `app/Dockerfile`.
- **db** - MySQL 8.4. Data is kept in the `db_data` volume.
  Tables are created on first start by `db/init.sql`.

## Routes

- `/` - adds 1 to the global counter, logs the visit (time, client IP,
  internal IP) to the `access_log` table, sets a 5-minute `server_ip`
  cookie, and returns the container's internal IP.
- `/showcount` - returns the global counter.

## Run

```
docker compose up -d --build
```

Open http://localhost

## Scale

```
bash scale.sh        # 5 replicas (default)
bash scale.sh 10     # any number
```

The script scales the app and restarts nginx so it routes to the new replicas.

## Test

1. `bash scale.sh 10`
2. Open http://localhost and the browser DevTools -> Application -> Cookies
3. Refresh - the IP stays the same (same as the `server_ip` cookie)
4. Delete the cookie and refresh - a new IP
5. Repeat - 10 different IPs

## How the sticky session works

- No cookie -> nginx uses round robin. The container that answers sets the
  `server_ip` cookie with its own internal IP.
- Cookie present -> nginx sends the request straight to that IP.
- The container in the cookie is gone -> the connection fails within 1s,
  nginx falls back to round robin, and the new container sets a new cookie.

No `ip_hash`, `hash`, or nginx-generated cookie is used.

## Stop

```
docker compose down       # keeps the database volume
docker compose down -v    # also deletes the database volume
```