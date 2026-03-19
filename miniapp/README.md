# Dubai Property Auction — Mini App

## Структура

```
miniapp/
├── backend/
│   ├── main.py          ← FastAPI, все эндпоинты
│   ├── database.py      ← Зеркало моделей из auction_admin_bot
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── public/index.html
    ├── package.json
    └── src/
        ├── App.jsx               ← Роутинг экранов
        ├── index.css             ← Дизайн-система
        ├── index.js
        ├── pages/
        │   ├── LotList.jsx       ← Список лотов (Все / Мои аукционы)
        │   ├── LotDetail.jsx     ← Детальный экран + покупка
        │   └── Help.jsx          ← Помощь + написать администратору
        ├── components/
        │   ├── LotCard.jsx       ← Карточка в списке
        │   └── BuySheet.jsx      ← Bottom sheet подтверждения
        ├── hooks/
        │   ├── useTelegram.js    ← Telegram WebApp SDK
        │   └── useDropTimer.js   ← Таймер до снижения цены
        └── utils/
            ├── api.js            ← Запросы к бэкенду
            └── format.js         ← fmtAed, fmtCountdown
```

## Запуск

### Backend

```bash
cd miniapp/backend
cp .env.example .env
# Заполни DATABASE_URL и ADMIN_BOT_TOKEN в .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

`.env`:
```
DATABASE_URL=sqlite+aiosqlite:///../../auction_admin_bot/auction.db
ADMIN_BOT_TOKEN=<токен_admin_бота>
ADMIN_TG_ID=<telegram_id_администратора>
```

### Frontend

```bash
cd miniapp/frontend
npm install
npm start        # разработка на :3000
npm run build    # продакшн сборка в build/
```

Для разработки проксирование `/api` → `localhost:8000` настроено в `package.json`.

## API

| Метод | Путь              | Описание                              |
|-------|-------------------|---------------------------------------|
| GET   | `/api/lots`       | Все активные/паузные/запланированные  |
| GET   | `/api/lots/mine`  | Лоты где пользователь участвовал      |
| GET   | `/api/lots/{id}`  | Один лот                              |
| POST  | `/api/buy`        | Купить лот по текущей цене `{lot_id}` |
| POST  | `/api/contact`    | Получить ID администратора            |
| GET   | `/api/photo/{id}` | Прокси фото из Telegram               |

## Синхронизация моделей

`backend/database.py` — точная копия `auction_admin_bot/db/database.py`.
При изменении полей в БД обновляй оба файла.

## Деплой

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    root /var/www/miniapp/frontend/build;
    index index.html;
    location / { try_files $uri /index.html; }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

Зарегистрировать Mini App в BotFather:
```
/newapp → выбрать бота → указать URL: https://your-domain.com
```
