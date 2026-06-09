# 🤖 AI Telegram Bot — Railway Deploy

## Kerakli narsalar
- Telegram Bot Token (@BotFather dan)
- Anthropic API Key (console.anthropic.com)
- GitHub akkaunt
- Railway akkaunt (railway.app)

---

## 📋 Qadamlar

### 1. Bot Token olish
1. Telegramda @BotFather ga yozing
2. `/newbot` yuboring
3. Bot nomini kiriting (masalan: `MyAIBot`)
4. Username kiriting (masalan: `myai_bot`)
5. Token nusxalab oling: `123456789:ABCdef...`

### 2. Anthropic API Key olish
1. https://console.anthropic.com ga kiring
2. API Keys bo'limiga o'ting
3. "Create Key" bosing
4. Kalitni nusxalab oling: `sk-ant-...`

### 3. GitHub ga yuklash
1. GitHub.com da yangi repo yarating
2. Barcha fayllarni yuklang:
   - bot.py
   - requirements.txt
   - Procfile
   - railway.toml

### 4. Railway da Deploy
1. https://railway.app ga kiring
2. "New Project" → "Deploy from GitHub repo"
3. Repongizni tanlang
4. **Variables** bo'limiga o'ting va qo'shing:
   ```
   TELEGRAM_TOKEN = sizning_token
   ANTHROPIC_API_KEY = sizning_api_key
   ```
5. Deploy tugmani bosing

### 5. Tekshirish
Telegramda botingizni toping va `/start` yuboring!

---

## Buyruqlar
- `/start` — Botni ishga tushirish
- `/help` — Yordam
- `/clear` — Tarixni tozalash
