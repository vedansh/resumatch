# resumatch

Django app deployed via Harbor on AWS EC2.

## nginx routing

Harbor proxies requests through nginx at `/resumatch/` → port 8002.

- Health check URL is `/resumatch/health` (through nginx), NOT `/health`
- Do not change the `HEALTH_URL` in `deploy.yml` — `/health` returns 404
