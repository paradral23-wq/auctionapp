# Деплой Dubai Property Auction

## Структура файлов

```
auction2/
├── Dockerfile.bot          ← контейнер для бота
├── Dockerfile.api          ← контейнер для FastAPI + React
├── docker-compose.yml      ← оркестрация всех сервисов
├── nginx.conf              ← конфиг веб-сервера
├── .env                    ← секреты (не в git!)
├── .env.example            ← шаблон .env
├── .gitignore
├── .github/workflows/
│   └── deploy.yml          ← автодеплой при git push
├── auction_admin_bot/
├── miniapp/
└── texts.py
```

---

## Первый деплой (один раз)

### 1. Подготовь VPS (Ubuntu 22.04+)

```bash
# Установи Docker
curl -fsSL https://get.docker.com | sh
usermod -aG docker $USER

# Установи Certbot для SSL
apt install -y certbot
```

### 2. Получи SSL сертификат

```bash
# Останови nginx если запущен
certbot certonly --standalone -d your-domain.com
```

### 3. Залей проект на сервер

```bash
# Через git (рекомендуется)
git clone git@github.com:your-user/auction2.git ~/auction2
cd ~/auction2

# Или через scp (разово)
# scp -r ./auction2 user@server:~/
```

### 4. Создай .env

```bash
cp .env.example .env
nano .env  # заполни токены и домен
```

### 5. Замени домен в nginx.conf

```bash
sed -i 's/YOUR_DOMAIN/your-domain.com/g' nginx.conf
```

### 6. Запусти

```bash
docker compose up -d --build
```

### 7. Зарегистрируй Mini App в BotFather

```
/newapp → выбрать бота → URL: https://your-domain.com
```

---

## Обновление кода

### Вариант A — вручную

```bash
cd ~/auction2
git pull
docker compose up -d --build
docker image prune -f   # очистить старые образы
```

### Вариант B — автоматически через GitHub Actions

1. Добавь секреты в репозитории (Settings → Secrets):
   - `VPS_HOST` — IP сервера
   - `VPS_USER` — пользователь (обычно `root`)
   - `VPS_SSH_KEY` — приватный SSH ключ

2. Теперь каждый `git push main` → автодеплой.

---

## Полезные команды

```bash
# Логи бота
docker compose logs -f bot

# Логи API
docker compose logs -f api

# Статус всех сервисов
docker compose ps

# Перезапустить только бота
docker compose restart bot

# Зайти в контейнер бота
docker compose exec bot bash

# Бэкап БД
docker compose exec bot sqlite3 /data/auction.db ".backup /data/auction_backup.db"
cp $(docker volume inspect auction2_db_data --format '{{.Mountpoint}}')/auction.db ./backup.db
```

---

## Структура volumes

- `db_data` — SQLite файл, общий для бота и API
- `videos` — загруженные видео файлы, общие для бота и API
- `frontend_build` — собранный React, передаётся в Nginx

---

## Обновление SSL сертификата (автоматически)

```bash
# Добавь в crontab
0 3 * * * certbot renew --quiet && docker compose exec nginx nginx -s reload
```
