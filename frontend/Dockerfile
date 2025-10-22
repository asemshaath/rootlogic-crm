# Stage 1: Build the app
FROM node:20 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:1.27-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Cloud Run listens on 8080, not 80
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
