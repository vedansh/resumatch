# resumatch

Django app deployed via Harbor on AWS EC2.

## nginx routing

Harbor proxies requests through nginx at `/resumatch/` → port 8007.

- Health check URL is `/resumatch/health` (through nginx), NOT `/health`
- Do not change the `HEALTH_URL` in `.github/workflows/deploy.yml` — `/health` returns 404
