# ⚡ QuizMaster Pro - Quick Start Guide

## 🎯 Get Started in 3 Minutes

### Option A: Run Locally (Fastest)

```bash
# 1. Install dependencies
pip install streamlit pandas

# 2. Run the app
streamlit run quiz_app.py
```

That's it! Your browser will open automatically at `http://localhost:8501`

---

### Option B: Deploy to Streamlit Cloud (FREE & Public)

**Perfect for sharing with others!**

#### Step 1: Prepare GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Upload these files:
   - `quiz_app.py`
   - `requirements.txt`
   - `README.md`

#### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository:** Your GitHub repo
   - **Branch:** main
   - **Main file path:** quiz_app.py
5. Click **"Deploy!"**

#### Step 3: Share

Your app will be live at:
```
https://[your-app-name].streamlit.app
```

**Benefits:**
- ✅ 100% FREE forever
- ✅ Automatic HTTPS
- ✅ Auto-updates when you push to GitHub
- ✅ No server management
- ✅ Shareable public URL

---

### Option C: Docker (One Command)

```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8501
```

---

## 🎮 Using the App

### 1. Landing Page
- Enter your name and email
- Choose a quiz topic (8 categories available)
- Click "Start Quiz"

### 2. Take the Quiz
- Answer 10 multiple-choice questions
- Navigate with Next/Previous buttons
- Click "Finish Quiz" when done

### 3. View Results
- See your score and performance feedback
- Check the global leaderboard
- Take another quiz

---

## 🎨 Customization Cheat Sheet

### Add a New Topic

Open `quiz_app.py` and add to `QUIZ_DATA`:

```python
"Your Topic": [
    {
        "question": "What is 2+2?",
        "options": ["2", "3", "4", "5"],
        "correct": 2  # Index: 0=first option, 1=second, etc.
    },
    # Add 9 more questions for a total of 10
]
```

### Change Colors

In `quiz_app.py`, find `load_css()` and modify:

```python
:root {
    --primary: #6366f1;  # Your color here
}
```

### Adjust Passing Score

In `get_feedback()` function:

```python
if percentage >= 90:  # Change threshold
    return "🏆 Outstanding!", "Message", "#color"
```

---

## 📊 File Structure

```
quiz-app/
├── quiz_app.py          ⭐ Main application (this is all you need!)
├── requirements.txt     📦 Dependencies
├── README.md           📖 Full documentation
├── QUICKSTART.md       ⚡ This file
├── Dockerfile          🐳 Docker deployment
├── docker-compose.yml  🐳 Docker orchestration
├── Procfile           🚀 Heroku deployment
└── setup.sh           🚀 Heroku setup script
```

---

## 🐛 Common Issues

**Problem:** Port already in use  
**Solution:** 
```bash
streamlit run quiz_app.py --server.port=8502
```

**Problem:** Module not found  
**Solution:** 
```bash
pip install -r requirements.txt
```

**Problem:** Database locked  
**Solution:** 
```bash
rm quiz_results.db
streamlit run quiz_app.py
```

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Test all quiz topics
- [ ] Verify email validation
- [ ] Check mobile responsiveness
- [ ] Test leaderboard with multiple entries
- [ ] Backup database regularly
- [ ] Monitor application logs

---

## 📱 Sharing Your Quiz

Once deployed, share your quiz by:

1. **Direct Link:** Send the URL to users
2. **QR Code:** Generate a QR code pointing to your URL
3. **Embed:** Use iframe (for Streamlit Cloud apps)
4. **Social Media:** Share on platforms with preview

---

## 💡 Pro Tips

1. **Backup Database:**
   ```bash
   cp quiz_results.db quiz_results_backup_$(date +%Y%m%d).db
   ```

2. **View Database:**
   ```bash
   sqlite3 quiz_results.db "SELECT * FROM results;"
   ```

3. **Reset Leaderboard:**
   ```bash
   sqlite3 quiz_results.db "DELETE FROM results;"
   ```

4. **Export Results:**
   ```bash
   sqlite3 -header -csv quiz_results.db "SELECT * FROM results;" > results.csv
   ```

---

## 🚀 Next Steps

- ✅ Add more quiz questions
- ✅ Create custom themes
- ✅ Add timer to questions
- ✅ Implement difficulty levels
- ✅ Add user authentication
- ✅ Create admin dashboard

---

## 📞 Need Help?

- 📖 Read the full [README.md](README.md)
- 🌐 Check [Streamlit Docs](https://docs.streamlit.io)
- 🐛 Report issues on GitHub

---

**You're all set! Happy quizzing! 🎉**
