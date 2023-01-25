# TODO List

A simple TODO list with GitHub authentication

## Stack used

- [Docker](https://www.docker.com/)
- [Flask](https://flask.palletsprojects.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Caddy](https://caddyserver.com/)
- [Svelte](https://svelte.dev/)
- [tailwindcss](https://tailwindcss.com/)
- [daisyUI](https://svelte.dev/)

## Running

- Clone the repository
- Create a .env following the format of .env.example
    - Get your `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` by creating an [OAuth app](https://github.com/settings/applications/new) on GitHub
    - Fill `BASE_URL` and `API_URL` with public facing or local domains, Caddy will automatically get a certificate for them (defaulting to local certificates, update the `Caddyfile` accordingly to the [docs](https://caddyserver.com/docs/caddyfile/directives/tls#tls) if you want a public certificate). `API_URL` must be a subdomain of `BASE_URL`.
- Run `docker compose up`

