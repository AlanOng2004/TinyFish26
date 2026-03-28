## Cloudflare Tunnel Setup

This folder contains templates for publishing the local frontend and backend through a
single Cloudflare Tunnel.

Recommended public hostnames:

- `stocks.thealan.net` -> frontend
- `api-stocks.thealan.net` -> backend

Before starting the tunnel:

1. Run the backend locally on `127.0.0.1:8000`
2. Build the frontend with `VITE_API_BASE_URL=https://api-stocks.thealan.net`
3. Run the frontend preview server on `127.0.0.1:4173`
4. Copy `cloudflare/config.yml.example` to `~/.cloudflared/config.yml`
5. Replace `<TUNNEL-UUID>` with the UUID from `cloudflared tunnel create stocks-site`

Useful commands:

```bash
cloudflared tunnel login
cloudflared tunnel create stocks-site
cloudflared tunnel route dns stocks-site stocks.thealan.net
cloudflared tunnel route dns stocks-site api-stocks.thealan.net
cloudflared tunnel run stocks-site
```
