# 🎬 Cinema Service

Полный набор микросервисов и вспомогательных компонентов для управления онлайн-кинотеатром: аутентификация пользователей, каталог фильмов, поиск фильмов, UGC-сервис.

---

## 📐 Обзор архитектуры

- **Auth Service** — регистрация, логин, JWT, OAuth (Яндекс), роли.  
- **Catalog Service** — информация о фильмах, жанрах и сеансах.  
- **Booking Service** — бронирование мест, проверка доступности, резерв.  
- **Notifications Service** — рассылка email/SMS-уведомлений.

---

## 🛠️ Технологический стек

- **Python 3.12** + **FastAPI**  
- **SQLAlchemy** + **Alembic**  
- **PostgreSQL**  
- **Redis**  
- **Kafka**
- **Docker** & **Docker Compose**  
- **Nginx** 
- **GitLab CI/CD**  
- **Swagger** 

---
## 🚀 Быстрый старт (локально)

1. **Клонируйте**  
   ```bash
   git clone git@github.com:Alexander-Gorbunov-gth/YP_team_sprint.git
   cd YP_team_sprint
   ```

2. **Создайте и заполните** `.env` файлы  
   ```bash
   cp .env.example .env
   cp services/auth/.env.example services/auth/.env
   # … для остальных сервисов
   ```

3. **Запустите в режиме разработки**  
   ```bash
   docker-compose -f docker-compose.override.yml up --build
   ```
