# 🕊️ Aleph Bet Foresight Summit Bots Setup Guide

This guide will help you set up both the **Russian** and **English** versions of the Summit registration bot.

---

## 📋 Overview

You now have two versions of the bot:

1. **Russian Version** 🇷🇺 - in folder `summit-registration-bot/`
2. **English Version** 🇬🇧 - in folder `summit-registration-bot-en/`

Both bots have the same functionality but with different language interfaces.

---

## 🤖 Creating Bots in Telegram

You need to create **TWO separate bots** in Telegram via @BotFather.

### Russian Bot:

1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send command: `/newbot`
3. Bot name: `Aleph Bet Foresight Summit RU` (or your choice)
4. Bot username: Must end with `bot`, e.g., `AlephBetForesightSummitRUbot`
5. **Save the token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### English Bot:

1. Again send to @BotFather: `/newbot`
2. Bot name: `Aleph Bet Foresight Summit EN` (or your choice)
3. Bot username: `AlephBetForesightSummitENbot` ✅ (as you specified)
4. **Save the token** (different from the first one!)

---

## 🚀 Quick Local Test

### Test Russian Bot:

```powershell
# Go to Russian bot folder
cd summit-registration-bot

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your RUSSIAN bot token
# TELEGRAM_BOT_TOKEN=your_russian_bot_token_here

# Run bot
python bot.py
```

Open Telegram → Find your Russian bot → Send `/start`

### Test English Bot:

```powershell
# Stop the Russian bot (Ctrl+C)

# Go to English bot folder
cd ..\summit-registration-bot-en

# Use the same venv or create new one
.\venv\Scripts\activate  # If using same venv
# OR
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your ENGLISH bot token
# TELEGRAM_BOT_TOKEN=your_english_bot_token_here

# Run bot
python bot.py
```

Open Telegram → Find your English bot → Send `/start`

---

## 📦 Deploy to Render (Free Hosting)

You need to deploy **TWO separate services** on Render.

### Prerequisites:

1. Create **TWO GitHub repositories**:
   - `alephbet-foresight-summit-ru-bot`
   - `alephbet-foresight-summit-en-bot`

### Deploy Russian Bot:

```powershell
# In summit-registration-bot folder
cd summit-registration-bot
git init
git add .
git commit -m "Initial commit - Russian bot"
git remote add origin https://github.com/YOUR_USERNAME/alephbet-foresight-summit-ru-bot.git
git branch -M main
git push -u origin main
```

**On Render:**
1. New+ → Background Worker
2. Connect repository: `alephbet-foresight-summit-ru-bot`
3. Settings:
   - Name: `alephbet-summit-ru`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
4. Environment Variables:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: **RUSSIAN bot token**
5. Create Background Worker

### Deploy English Bot:

```powershell
# In summit-registration-bot-en folder
cd ..\summit-registration-bot-en
git init
git add .
git commit -m "Initial commit - English bot"
git remote add origin https://github.com/YOUR_USERNAME/alephbet-foresight-summit-en-bot.git
git branch -M main
git push -u origin main
```

**On Render:**
1. New+ → Background Worker
2. Connect repository: `alephbet-foresight-summit-en-bot`
3. Settings:
   - Name: `alephbet-summit-en`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
4. Environment Variables:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: **ENGLISH bot token**
5. Create Background Worker

---

## 🔗 Bot Links for Your Website

After bots are deployed, you can use these links on your website:

**Russian Bot:**
```
https://t.me/YourRussianBotUsername?start=registration
```

**English Bot:**
```
https://t.me/AlephBetForesightSummitENbot?start=registration
```

### Integration with Tilda:

Create two buttons on your website:

**Button 1: "Регистрация (RU)"**
- Link: `https://t.me/YourRussianBotUsername?start=registration`

**Button 2: "Registration (EN)"**
- Link: `https://t.me/AlephBetForesightSummitENbot?start=registration`

See `TILDA_INTEGRATION.md` in each bot folder for detailed instructions.

---

## 📊 Database Separation

**Important:** Each bot has its own separate database (`summit_bot.db`).

- Russian bot stores Russian-speaking participants
- English bot stores English-speaking participants

If you want a unified database, you'll need to:
1. Use PostgreSQL on Render (free tier available)
2. Modify `database.py` to connect to the same PostgreSQL instance
3. Add a `language` field to track user language preference

---

## 🔧 Customization

### Change Available Days:

In both `bot.py` files, line ~69:
```python
while days_added < 6:  # Change 6 to desired number
```

### Change Texts:

All user-facing texts are in `bot.py`:
- Greetings
- Button labels
- Information messages

Just edit and `git push` - Render will auto-deploy!

---

## 📱 Testing Checklist

### For EACH bot:

- [ ] Bot created in @BotFather
- [ ] Token saved
- [ ] `.env` file configured
- [ ] Bot runs locally
- [ ] `/start` command works
- [ ] Both participant types work
- [ ] Date selection works
- [ ] QR code generated
- [ ] `/menu` command works
- [ ] Repository on GitHub
- [ ] Deployed on Render
- [ ] Works in production

---

## 🆘 Common Issues

### Bot responds in wrong language:
- Check you're using the correct bot token in `.env`
- Each bot should have its own token

### Both bots share same database:
- Make sure each bot runs in its own folder
- Each has separate `summit_bot.db` file

### Can't run both bots locally simultaneously:
- **Correct!** You can only run one at a time locally
- For simultaneous operation, deploy both on Render

---

## 📞 Support Files

Each bot folder contains detailed documentation:

- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `DEPLOY_RENDER.md` - Detailed Render deployment
- `RENDER_QUICK_GUIDE.md` - Quick Render reference
- `COMMANDS.md` - Command cheat sheet
- `TILDA_INTEGRATION.md` - Website integration

---

## 🎯 Next Steps

1. ✅ Create both bots in @BotFather
2. ✅ Test both bots locally
3. ✅ Deploy both to Render
4. ✅ Test both in production
5. ✅ Add buttons to your website
6. ✅ Share bot links with participants!

---

## 📊 Monitoring

**Render Dashboard:**
- [Russian Bot Logs](https://dashboard.render.com/) - Monitor Russian bot
- [English Bot Logs](https://dashboard.render.com/) - Monitor English bot

Check logs regularly for:
- New registrations
- Errors
- User activity

---

## 💡 Future Enhancements

Consider adding:
- Admin panel with statistics
- Zoom API integration
- Email notifications
- PostgreSQL for permanent storage
- Multi-language support in single bot
- WhatsApp integration
- Meeting reminders

---

**Good luck with your Aleph Bet Foresight Summit! 🕊️**

---

## 🔑 Quick Reference

| Item | Russian Bot | English Bot |
|------|------------|-------------|
| **Folder** | `summit-registration-bot/` | `summit-registration-bot-en/` |
| **Bot Username** | Your choice | `AlephBetForesightSummitENbot` |
| **Token Variable** | `TELEGRAM_BOT_TOKEN` | `TELEGRAM_BOT_TOKEN` |
| **Database** | `summit_bot.db` (separate) | `summit_bot.db` (separate) |
| **GitHub Repo** | Your choice | `alephbet-foresight-summit-en-bot` |
| **Render Service** | `alephbet-summit-ru` | `alephbet-summit-en` |
