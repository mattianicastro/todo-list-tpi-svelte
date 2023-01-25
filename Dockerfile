FROM node:19 as frontend_build

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend .

RUN npm run build

FROM caddy:2.6.2

COPY --from=frontend_build /app/dist /srv
