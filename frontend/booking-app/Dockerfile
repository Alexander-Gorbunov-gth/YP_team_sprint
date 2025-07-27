# Этап 1: Сборка React-приложения
FROM node:20-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап 2: Копирование сборки в итоговый образ (на volume)
FROM alpine:latest as export
WORKDIR /frontend-build
COPY --from=build /app/dist ./
