# 🔥 Roast Bot - Deployment Guide

## Quick Start (Local Testing)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   Go to `http://localhost:5000`

---

## Deploy Online

### Option 1: Heroku (FREE with limitations)

1. **Create Heroku account:** https://www.heroku.com/

2. **Install Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli

3. **Login and deploy:**
   ```bash
   heroku login
   heroku create your-roast-bot-name
   git push heroku main
   ```

4. **Share link:** `https://your-roast-bot-name.herokuapp.com`

---

### Option 2: Railway (EASIEST - $5/month)

1. **Create Railway account:** https://railway.app

2. **Connect GitHub:**
   - Push your code to GitHub
   - Connect your repo to Railway
   - Railway auto-detects Python & deploys

3. **Share link:** Get from Railway dashboard (auto-generated)

---

### Option 3: Render (FREE with limitations)

1. **Create Render account:** https://render.com

2. **Create Web Service:**
   - Select GitHub repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

3. **Deploy:** Click "Deploy"

---

### Option 4: PythonAnywhere (FREE Tier)

1. **Create account:** https://www.pythonanywhere.com

2. **Upload files:**
   - Upload `app.py`, `templates/index.html`, `requirements.txt`

3. **Create Flask web app:**
   - Use their web app setup wizard
   - Point to `app:app`

4. **Share link:** `your-username.pythonanywhere.com`

---

## Recommended: Railway 🚀

**Why Railway?**
- Easiest setup (just connect GitHub)
- Supports custom domains
- Good free tier & affordable paid
- No credit card required for free tier
- Instant updates on each git push

**Steps:**
1. Push code to GitHub
2. Go to railway.app
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Done! Your app is live in 2-3 minutes

**Share:** `your-app-name.up.railway.app` (or custom domain)

---

## Making It Shareable

### GitHub Link:
```
https://github.com/YOUR_USERNAME/YOUR_REPO
```
Others can:
- View your code
- Fork it
- Deploy their own version

### Live Web Link (after deployment):
```
https://your-roast-bot-name.railway.app
```
Share this - no installation needed!

### QR Code Generator (Optional):
- Use https://qr-code-generator.com
- Generate QR for your live URL
- People can scan to use instantly

---

## Custom Domain (Optional)

If deployed on Railway/Heroku:
1. Buy domain from Namecheap/GoDaddy
2. Configure CNAME to point to your app
3. Set custom domain in platform settings

Example: `roastbot.yourname.com`

---

## Environment Variables

For production, set in your platform's dashboard:
```
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## File Structure for Deployment

```
your-repo/
├── app.py                 (Main Flask app)
├── requirements.txt       (Dependencies)
├── Procfile              (Deployment config)
├── templates/
│   └── index.html        (Web interface)
├── README.md
└── .git/                 (Git repo)
```

---

## Troubleshooting

**App won't start:**
- Check `requirements.txt` has `flask` and `gunicorn`
- Ensure `app.py` has `app.run()` at the end

**Templates not loading:**
- Check `templates/index.html` exists
- Flask auto-finds templates folder

**404 errors:**
- Make sure route is `/` in `app.py`

---

## Share Your App! 🎉

Once deployed, share:
- Direct link: `https://your-app.railway.app`
- GitHub repo: `https://github.com/you/python`
- QR code (using QR generator)
- Social media: "Check out my roast bot!"

Enjoy! 🔥
