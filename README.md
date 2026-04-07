# 🎯 QuizMaster Pro

A modern, production-ready quiz application built with Python and Streamlit. Features a clean UI, persistent storage, and easy deployment.

## ✨ Features

### User Experience
- 🎨 **Modern UI/UX** - Clean, responsive design with smooth animations
- 📱 **Mobile Responsive** - Works seamlessly on all device sizes
- 🎯 **8 Quiz Categories** - Sports, Geopolitics, Movies, Technology, History, Science, General Knowledge, Business
- 📊 **Real-time Progress** - Visual progress tracking during quiz
- 🏆 **Instant Feedback** - Performance-based feedback upon completion

### Technical Features
- 💾 **Persistent Storage** - SQLite database for results
- 📈 **Leaderboard** - Global ranking system
- ✅ **Input Validation** - Email and name validation
- 🔒 **Session Management** - Proper state handling
- 📊 **Statistics Dashboard** - Overall quiz statistics
- 🚀 **Production Ready** - Optimized for deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. **Clone or download the files:**
   ```bash
   # If using git
   git clone <repository-url>
   cd quiz-app

   # Or create a directory and add the files
   mkdir quiz-app
   cd quiz-app
   # Copy quiz_app.py and requirements.txt to this directory
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run quiz_app.py
   ```

4. **Access the app:**
   - Open your browser and go to: `http://localhost:8501`
   - The app will automatically open in your default browser

## 📦 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

**Easiest and fastest deployment method!**

1. **Prepare your repository:**
   - Create a GitHub account if you don't have one
   - Create a new repository
   - Upload `quiz_app.py` and `requirements.txt`

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and main file (`quiz_app.py`)
   - Click "Deploy"

3. **Share your app:**
   - Your app will be live at: `https://<your-app-name>.streamlit.app`
   - Share this link with anyone!

**Benefits:**
- ✅ Completely FREE
- ✅ Automatic HTTPS
- ✅ Custom domain support
- ✅ Auto-updates on git push
- ✅ No server management

### Option 2: Render (FREE Tier Available)

1. **Create a Render account** at [render.com](https://render.com)

2. **Create `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: quizmaster-pro
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run quiz_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

3. **Deploy:**
   - Push code to GitHub
   - Connect Render to your repository
   - Deploy automatically

### Option 3: Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create additional files:**

   **Procfile:**
   ```
   web: sh setup.sh && streamlit run quiz_app.py
   ```

   **setup.sh:**
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

### Option 4: AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04)

2. **SSH into instance and install:**
   ```bash
   sudo apt update
   sudo apt install python3-pip -y
   git clone <your-repo>
   cd quiz-app
   pip3 install -r requirements.txt
   ```

3. **Run with nohup:**
   ```bash
   nohup streamlit run quiz_app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

4. **Configure security group** to allow port 8501

### Option 5: Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY quiz_app.py .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "quiz_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run:**
   ```bash
   docker build -t quiz-app .
   docker run -p 8501:8501 quiz-app
   ```

## 📊 Database

The application uses SQLite for data persistence. The database file `quiz_results.db` is automatically created on first run.

**Schema:**
```sql
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    topic TEXT NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

**Features:**
- Automatic database initialization
- Persistent storage across sessions
- Leaderboard ranking
- Statistics aggregation

## 🎮 Usage Guide

### For Quiz Takers:

1. **Start Page:**
   - Enter your full name
   - Provide a valid email address
   - Select a quiz topic from 8 categories
   - Click "Start Quiz"

2. **Taking the Quiz:**
   - Answer 10 multiple-choice questions
   - Use "Next" to proceed
   - Use "Previous" to review answers
   - Click "Finish Quiz" after the last question

3. **Results:**
   - View your score and percentage
   - See performance feedback
   - Take another quiz or view leaderboard

4. **Leaderboard:**
   - See top 50 scores globally
   - Compare your performance
   - Filter by date and topic

## 🎨 Customization

### Adding New Quiz Topics

Edit `QUIZ_DATA` dictionary in `quiz_app.py`:

```python
QUIZ_DATA["Your Topic"] = [
    {
        "question": "Your question?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct": 0  # Index of correct answer (0-3)
    },
    # Add 10 questions total
]
```

### Modifying Styling

Update the CSS in the `load_css()` function:

```python
def load_css():
    st.markdown("""
    <style>
    /* Your custom CSS here */
    :root {
        --primary: #6366f1;  /* Change primary color */
    }
    </style>
    """, unsafe_allow_html=True)
```

### Changing Feedback Thresholds

Modify the `get_feedback()` function:

```python
def get_feedback(score: int, total: int) -> Tuple[str, str, str]:
    percentage = (score / total) * 100
    
    if percentage >= 90:  # Adjust threshold
        return "🏆 Outstanding!", "Message", "#color"
    # ... etc
```

## 🔧 Configuration

### Environment Variables

You can configure the app using environment variables:

```bash
# For production deployments
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
```

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f3f4f6"
textColor = "#1f2937"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
```

## 📈 Scaling Considerations

### For High Traffic:

1. **Database:**
   - Migrate from SQLite to PostgreSQL
   - Update database connection in code
   - Use connection pooling

2. **Caching:**
   - Add `@st.cache_data` decorators
   - Cache quiz data loading
   - Cache leaderboard queries

3. **Load Balancing:**
   - Deploy multiple instances
   - Use Nginx as reverse proxy
   - Implement session stickiness

## 🐛 Troubleshooting

### Common Issues:

**Port already in use:**
```bash
# Use a different port
streamlit run quiz_app.py --server.port=8502
```

**Database locked:**
```bash
# Remove the database file and restart
rm quiz_results.db
streamlit run quiz_app.py
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Permission denied:**
```bash
# Run with proper permissions
chmod +x quiz_app.py
```

## 📝 File Structure

```
quiz-app/
├── quiz_app.py          # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── quiz_results.db     # SQLite database (auto-generated)
└── .streamlit/         # Optional config directory
    └── config.toml     # Streamlit configuration
```

## 🔒 Security Notes

### Best Practices Implemented:

- ✅ Input validation (email, name)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Session state management
- ✅ No hardcoded credentials

### For Production:

1. **Add authentication** for admin features
2. **Implement rate limiting** to prevent abuse
3. **Use HTTPS** (automatic with Streamlit Cloud)
4. **Regular backups** of database
5. **Monitor** application logs

## 🎯 Performance Optimization

### Current Optimizations:

- Efficient database queries with indexes
- Minimal re-renders using session state
- Lazy loading of components
- Optimized CSS delivery

### Future Improvements:

- Add caching for static data
- Implement database connection pooling
- Compress images and assets
- Use CDN for static files

## 📱 Browser Support

Tested and working on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

To add features or fix bugs:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
- Check the troubleshooting section above
- Review Streamlit documentation: https://docs.streamlit.io
- Open an issue on GitHub

## 🎉 Credits

Built with:
- [Streamlit](https://streamlit.io) - Web framework
- [SQLite](https://www.sqlite.org) - Database
- [Python](https://www.python.org) - Programming language

---

**Happy Quizzing! 🎯**

Made with ❤️ for learning and fun.
