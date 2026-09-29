# 🤖 Kaloriya Hisoblagich Telegram Bot

**AI yordamida ovqat va mahsulotlar kaloriyasini hisoblash boti**

---

## 📋 Loyiha tuzilmasi

```
bot/
├── bot.py            # Asosiy bot fayli
├── ai_analyzer.py    # Gemini AI tahlil moduli
├── config.py         # Konfiguratsiya va API kalitlar
├── requirements.txt  # Kerakli kutubxonalar
├── bot.log           # Log fayli (avtomatik yaratiladi)
└── README.md         # Bu fayl
```

---

## ⚙️ O'rnatish va Ishga Tushirish

### 1️⃣ API Kalitlarini Oling

**Telegram Bot Token:**
1. Telegramda [@BotFather](https://t.me/BotFather) ga yozing
2. `/newbot` buyrug'ini bajaring
3. Bot uchun nom va username bering
4. Token ni nusxalab oling

**Google Gemini API Key:**
1. [https://aistudio.google.com](https://aistudio.google.com) saytiga kiring
2. Google akkauntingiz bilan kiring
3. "Get API Key" tugmasini bosing
4. Yangi API kalit yarating va nusxalab oling

---

### 2️⃣ config.py ni Sozlang

```python
TELEGRAM_BOT_TOKEN = "7123456789:AAFxxx..."   # Sizning tokeningiz
GEMINI_API_KEY = "AIzaSyXxx..."                # Sizning Gemini kalitingiz
```

---

### 3️⃣ Kutubxonalarni O'rnating

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Botni Ishga Tushiring

```bash
python bot.py
```

---

## 🌟 Imkoniyatlar

| Xususiyat | Tavsif |
|-----------|--------|
| 📸 Rasm tahlili | Har qanday ovqat rasmini taniydi |
| 🔢 Kaloriya hisob | 100g va umumiy porsiya uchun |
| 🧬 Ozuqa tarkibi | Oqsil, Yog', Uglevod, Tola |
| 💡 Maslahat | Dietolog tavsiyalari |
| 📁 Ko'p format | JPEG, PNG, WEBP, GIF |
| 📝 Loglar | bot.log faylida saqlanadi |

---

## 🤖 Bot Buyruqlari

- `/start` — Botni ishga tushirish
- `/help` — Yordam va ko'rsatmalar
- `/about` — Bot haqida ma'lumot

---

## 📦 Texnologiyalar

- **Python** 3.10+
- **python-telegram-bot** 20.7 (async)
- **Google Gemini 1.5 Flash** (AI Vision)
- **aiohttp** (async HTTP)

---

## ⚠️ Muhim Eslatmalar

- Gemini API bepul, lekin kunlik limit bor (bepul: 15 so'rov/daqiqa)
- Kaloriya hisoblari **taxminiy** bo'ladi
- Bot 24/7 ishlashi uchun serverga (VPS/Heroku) joylashtirish tavsiya qilinadi
