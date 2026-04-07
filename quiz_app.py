"""
QuizMaster Pro - A Modern Quiz Application
Built with Streamlit for clean UI/UX and easy deployment
"""

import streamlit as st
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Tuple
import re

# Page configuration
st.set_page_config(
    page_title="QuizMaster Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
def load_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
    
    /* Option buttons */
    div[data-testid="stRadio"] > div {
        gap: 0.75rem;
    }
    
    div[data-testid="stRadio"] label {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div[data-testid="stRadio"] label:hover {
        border-color: #6366f1;
        background: #f0f9ff;
        transform: translateX(4px);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Cards */
    .quiz-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .score-card {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Leaderboard table */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# Database setup
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('quiz_results.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

# Quiz data
QUIZ_DATA = {
    "Sports": [
        {
            "question": "Which country won the FIFA World Cup 2022?",
            "options": ["Brazil", "Argentina", "France", "Germany"],
            "correct": 1
        },
        {
            "question": "How many players are there in a cricket team?",
            "options": ["10", "11", "12", "13"],
            "correct": 1
        },
        {
            "question": "In which year were the first modern Olympic Games held?",
            "options": ["1892", "1896", "1900", "1904"],
            "correct": 1
        },
        {
            "question": "What is the diameter of a basketball hoop in inches?",
            "options": ["16", "18", "20", "22"],
            "correct": 1
        },
        {
            "question": "Which tennis tournament is played on grass courts?",
            "options": ["US Open", "French Open", "Wimbledon", "Australian Open"],
            "correct": 2
        },
        {
            "question": "How many points is a touchdown worth in American football?",
            "options": ["5", "6", "7", "8"],
            "correct": 1
        },
        {
            "question": "What sport is known as 'The Sport of Kings'?",
            "options": ["Polo", "Horse Racing", "Cricket", "Golf"],
            "correct": 1
        },
        {
            "question": "In which sport would you perform a 'slam dunk'?",
            "options": ["Volleyball", "Tennis", "Basketball", "Badminton"],
            "correct": 2
        },
        {
            "question": "How many Grand Slam tournaments are there in tennis?",
            "options": ["3", "4", "5", "6"],
            "correct": 1
        },
        {
            "question": "What is the maximum break in snooker?",
            "options": ["147", "155", "167", "180"],
            "correct": 0
        }
    ],
    "Geopolitics": [
        {
            "question": "Which organization has China, Russia, and India as members?",
            "options": ["NATO", "BRICS", "ASEAN", "EU"],
            "correct": 1
        },
        {
            "question": "What is the capital of Australia?",
            "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
            "correct": 2
        },
        {
            "question": "How many permanent members are in the UN Security Council?",
            "options": ["3", "5", "7", "10"],
            "correct": 1
        },
        {
            "question": "Which country was formerly known as Persia?",
            "options": ["Iraq", "Iran", "Turkey", "Syria"],
            "correct": 1
        },
        {
            "question": "The European Union was established by which treaty?",
            "options": ["Treaty of Paris", "Treaty of Rome", "Treaty of Versailles", "Treaty of Maastricht"],
            "correct": 3
        },
        {
            "question": "Which country is not a member of NATO?",
            "options": ["Turkey", "Poland", "Sweden", "Switzerland"],
            "correct": 3
        },
        {
            "question": "What is the largest country in Africa by area?",
            "options": ["Algeria", "Congo", "Sudan", "Libya"],
            "correct": 0
        },
        {
            "question": "Which city is home to the International Court of Justice?",
            "options": ["Geneva", "Brussels", "The Hague", "Vienna"],
            "correct": 2
        },
        {
            "question": "How many countries are in the G7?",
            "options": ["5", "7", "10", "12"],
            "correct": 1
        },
        {
            "question": "Which strait separates Europe from Africa?",
            "options": ["Strait of Hormuz", "Strait of Gibraltar", "Bosphorus Strait", "Strait of Malacca"],
            "correct": 1
        }
    ],
    "Movies": [
        {
            "question": "Who directed 'The Shawshank Redemption'?",
            "options": ["Steven Spielberg", "Frank Darabont", "Christopher Nolan", "Martin Scorsese"],
            "correct": 1
        },
        {
            "question": "Which movie won the Oscar for Best Picture in 2020?",
            "options": ["1917", "Joker", "Parasite", "Once Upon a Time in Hollywood"],
            "correct": 2
        },
        {
            "question": "In which year was the first 'Star Wars' movie released?",
            "options": ["1975", "1977", "1979", "1981"],
            "correct": 1
        },
        {
            "question": "Who played Iron Man in the Marvel Cinematic Universe?",
            "options": ["Chris Evans", "Chris Hemsworth", "Robert Downey Jr.", "Mark Ruffalo"],
            "correct": 2
        },
        {
            "question": "Which film features the character 'Jack Dawson'?",
            "options": ["Pearl Harbor", "Titanic", "The Great Gatsby", "Catch Me If You Can"],
            "correct": 1
        },
        {
            "question": "What is the highest-grossing film of all time (not adjusted for inflation)?",
            "options": ["Avengers: Endgame", "Avatar", "Titanic", "Star Wars: The Force Awakens"],
            "correct": 1
        },
        {
            "question": "Who composed the music for 'The Lion King'?",
            "options": ["Hans Zimmer", "John Williams", "Alan Menken", "Elton John"],
            "correct": 0
        },
        {
            "question": "Which actress played Hermione Granger in Harry Potter films?",
            "options": ["Emma Watson", "Emma Stone", "Emily Blunt", "Emma Roberts"],
            "correct": 0
        },
        {
            "question": "What is the name of the fictional African country in 'Black Panther'?",
            "options": ["Wakanda", "Zamunda", "Genovia", "Sokovia"],
            "correct": 0
        },
        {
            "question": "Who directed 'Inception'?",
            "options": ["Ridley Scott", "Denis Villeneuve", "Christopher Nolan", "David Fincher"],
            "correct": 2
        }
    ],
    "Technology": [
        {
            "question": "Who is known as the father of computers?",
            "options": ["Alan Turing", "Charles Babbage", "Steve Jobs", "Bill Gates"],
            "correct": 1
        },
        {
            "question": "What does 'HTTP' stand for?",
            "options": ["HyperText Transfer Protocol", "High Transfer Text Protocol", "HyperText Transmission Protocol", "High Text Transfer Protocol"],
            "correct": 0
        },
        {
            "question": "In what year was the first iPhone released?",
            "options": ["2005", "2006", "2007", "2008"],
            "correct": 2
        },
        {
            "question": "What does 'AI' stand for in technology?",
            "options": ["Automated Intelligence", "Artificial Intelligence", "Advanced Intelligence", "Augmented Intelligence"],
            "correct": 1
        },
        {
            "question": "Which company developed the Python programming language?",
            "options": ["Microsoft", "Google", "None - it was created by Guido van Rossum", "Apple"],
            "correct": 2
        },
        {
            "question": "What does 'RAM' stand for?",
            "options": ["Random Access Memory", "Read Access Memory", "Rapid Access Memory", "Remote Access Memory"],
            "correct": 0
        },
        {
            "question": "Which company owns YouTube?",
            "options": ["Facebook", "Amazon", "Google", "Microsoft"],
            "correct": 2
        },
        {
            "question": "What is the main function of a GPU?",
            "options": ["Store data", "Process graphics", "Cool the system", "Connect to internet"],
            "correct": 1
        },
        {
            "question": "Which programming language is known for web development?",
            "options": ["Python", "JavaScript", "C++", "Swift"],
            "correct": 1
        },
        {
            "question": "What does 'VPN' stand for?",
            "options": ["Virtual Private Network", "Virtual Public Network", "Verified Private Network", "Visual Private Network"],
            "correct": 0
        }
    ],
    "History": [
        {
            "question": "In which year did World War II end?",
            "options": ["1943", "1944", "1945", "1946"],
            "correct": 2
        },
        {
            "question": "Who was the first President of the United States?",
            "options": ["Thomas Jefferson", "George Washington", "John Adams", "Benjamin Franklin"],
            "correct": 1
        },
        {
            "question": "Which empire built Machu Picchu?",
            "options": ["Aztec", "Maya", "Inca", "Olmec"],
            "correct": 2
        },
        {
            "question": "The Great Wall of China was built primarily to protect against which group?",
            "options": ["Mongols", "Japanese", "Europeans", "Indians"],
            "correct": 0
        },
        {
            "question": "Who painted the Mona Lisa?",
            "options": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"],
            "correct": 1
        },
        {
            "question": "In which year did the Berlin Wall fall?",
            "options": ["1987", "1988", "1989", "1990"],
            "correct": 2
        },
        {
            "question": "Who discovered America in 1492?",
            "options": ["Ferdinand Magellan", "Christopher Columbus", "Amerigo Vespucci", "Vasco da Gama"],
            "correct": 1
        },
        {
            "question": "Which ancient wonder is still standing today?",
            "options": ["Hanging Gardens of Babylon", "Colossus of Rhodes", "Great Pyramid of Giza", "Lighthouse of Alexandria"],
            "correct": 2
        },
        {
            "question": "Who was the first emperor of Rome?",
            "options": ["Julius Caesar", "Augustus", "Nero", "Caligula"],
            "correct": 1
        },
        {
            "question": "The French Revolution began in which year?",
            "options": ["1776", "1789", "1799", "1804"],
            "correct": 1
        }
    ],
    "Science": [
        {
            "question": "What is the chemical symbol for gold?",
            "options": ["Go", "Gd", "Au", "Ag"],
            "correct": 2
        },
        {
            "question": "What is the speed of light in vacuum?",
            "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"],
            "correct": 0
        },
        {
            "question": "How many bones are in the adult human body?",
            "options": ["186", "206", "226", "246"],
            "correct": 1
        },
        {
            "question": "What is the largest planet in our solar system?",
            "options": ["Saturn", "Jupiter", "Neptune", "Uranus"],
            "correct": 1
        },
        {
            "question": "What is the powerhouse of the cell?",
            "options": ["Nucleus", "Ribosome", "Mitochondria", "Chloroplast"],
            "correct": 2
        },
        {
            "question": "What gas do plants absorb from the atmosphere?",
            "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
            "correct": 2
        },
        {
            "question": "What is the hardest natural substance on Earth?",
            "options": ["Gold", "Iron", "Diamond", "Platinum"],
            "correct": 2
        },
        {
            "question": "At what temperature does water boil at sea level (Celsius)?",
            "options": ["90°C", "95°C", "100°C", "105°C"],
            "correct": 2
        },
        {
            "question": "How many chromosomes do humans have?",
            "options": ["23", "46", "92", "184"],
            "correct": 1
        },
        {
            "question": "What is the smallest unit of life?",
            "options": ["Atom", "Molecule", "Cell", "Organ"],
            "correct": 2
        }
    ],
    "General Knowledge": [
        {
            "question": "What is the largest ocean on Earth?",
            "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
            "correct": 3
        },
        {
            "question": "How many continents are there?",
            "options": ["5", "6", "7", "8"],
            "correct": 2
        },
        {
            "question": "What is the capital of Japan?",
            "options": ["Osaka", "Kyoto", "Tokyo", "Hiroshima"],
            "correct": 2
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "correct": 1
        },
        {
            "question": "How many days are in a leap year?",
            "options": ["364", "365", "366", "367"],
            "correct": 2
        },
        {
            "question": "What is the tallest mountain in the world?",
            "options": ["K2", "Mount Everest", "Kangchenjunga", "Lhotse"],
            "correct": 1
        },
        {
            "question": "Which country is known as the Land of the Rising Sun?",
            "options": ["China", "Thailand", "Japan", "South Korea"],
            "correct": 2
        },
        {
            "question": "How many colors are in a rainbow?",
            "options": ["5", "6", "7", "8"],
            "correct": 2
        },
        {
            "question": "What is the largest desert in the world?",
            "options": ["Sahara", "Arabian", "Gobi", "Antarctic"],
            "correct": 3
        },
        {
            "question": "Which language has the most native speakers?",
            "options": ["English", "Spanish", "Mandarin Chinese", "Hindi"],
            "correct": 2
        }
    ],
    "Business": [
        {
            "question": "What does 'CEO' stand for?",
            "options": ["Chief Executive Officer", "Chief Executive Official", "Central Executive Officer", "Corporate Executive Officer"],
            "correct": 0
        },
        {
            "question": "Which company is the largest by market capitalization (as of 2023)?",
            "options": ["Apple", "Microsoft", "Amazon", "Google"],
            "correct": 0
        },
        {
            "question": "What does 'ROI' stand for in business?",
            "options": ["Rate of Interest", "Return on Investment", "Revenue of Industry", "Risk of Investment"],
            "correct": 1
        },
        {
            "question": "Who founded Amazon?",
            "options": ["Elon Musk", "Jeff Bezos", "Bill Gates", "Mark Zuckerberg"],
            "correct": 1
        },
        {
            "question": "What is a 'startup'?",
            "options": ["A new business venture", "A computer program", "A marketing strategy", "A type of investment"],
            "correct": 0
        },
        {
            "question": "What does 'B2B' stand for?",
            "options": ["Business to Business", "Business to Buyer", "Brand to Business", "Back to Business"],
            "correct": 0
        },
        {
            "question": "Which company owns Instagram?",
            "options": ["Google", "Meta (Facebook)", "Twitter", "Microsoft"],
            "correct": 1
        },
        {
            "question": "What is the stock market index for the 30 largest US companies?",
            "options": ["S&P 500", "NASDAQ", "Dow Jones", "Russell 2000"],
            "correct": 2
        },
        {
            "question": "What does 'IPO' stand for?",
            "options": ["Initial Public Offering", "International Public Offer", "Internal Private Offering", "Investment Portfolio Option"],
            "correct": 0
        },
        {
            "question": "Who is the founder of Tesla?",
            "options": ["Jeff Bezos", "Elon Musk", "Bill Gates", "Steve Jobs"],
            "correct": 1
        }
    ]
}

# Validation functions
def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_name(name: str) -> bool:
    """Validate name (at least 2 characters, letters only)"""
    return len(name.strip()) >= 2 and name.replace(" ", "").isalpha()

# Database operations
def save_result(conn, name: str, email: str, topic: str, score: int, total: int):
    """Save quiz result to database"""
    c = conn.cursor()
    c.execute('''
        INSERT INTO results (name, email, topic, score, total_questions)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, topic, score, total))
    conn.commit()

def get_leaderboard(conn, limit: int = 50) -> List[Tuple]:
    """Get top scores from database"""
    c = conn.cursor()
    c.execute('''
        SELECT name, email, topic, score, total_questions, 
               ROUND(CAST(score AS FLOAT) / total_questions * 100, 1) as percentage,
               timestamp
        FROM results
        ORDER BY percentage DESC, timestamp DESC
        LIMIT ?
    ''', (limit,))
    return c.fetchall()

def get_user_stats(conn) -> Dict:
    """Get overall statistics"""
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM results')
    total_attempts = c.fetchone()[0]
    
    c.execute('SELECT AVG(CAST(score AS FLOAT) / total_questions * 100) FROM results')
    avg_score = c.fetchone()[0] or 0
    
    c.execute('SELECT topic, COUNT(*) as count FROM results GROUP BY topic ORDER BY count DESC LIMIT 1')
    result = c.fetchone()
    popular_topic = result[0] if result else "N/A"
    
    return {
        "total_attempts": total_attempts,
        "avg_score": round(avg_score, 1),
        "popular_topic": popular_topic
    }

# Feedback function
def get_feedback(score: int, total: int) -> Tuple[str, str, str]:
    """Get feedback based on score"""
    percentage = (score / total) * 100
    
    if percentage >= 90:
        return "🏆 Outstanding!", "Excellent work! You're a quiz master!", "#10b981"
    elif percentage >= 70:
        return "🌟 Great Job!", "Very good performance! Keep it up!", "#3b82f6"
    elif percentage >= 50:
        return "👍 Good Effort!", "Not bad! Room for improvement.", "#f59e0b"
    else:
        return "📚 Keep Learning!", "Don't give up! Practice makes perfect.", "#ef4444"

# Main app logic
def main():
    load_css()
    
    # Initialize database
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = init_database()
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    
    # Page routing
    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'quiz':
        show_quiz_page()
    elif st.session_state.page == 'results':
        show_results_page()
    elif st.session_state.page == 'leaderboard':
        show_leaderboard_page()

def show_landing_page():
    """Display landing page with user input"""
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 2rem;'>🎯 QuizMaster Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #6b7280; margin-bottom: 3rem;'>Test your knowledge across multiple topics!</p>", unsafe_allow_html=True)
    
    # Main form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='quiz-card'>", unsafe_allow_html=True)
        
        # User inputs
        name = st.text_input("📝 Your Name", placeholder="Enter your full name", key="name_input")
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com", key="email_input")
        
        # Topic selection
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎓 Select Quiz Topic")
        topic = st.selectbox(
            "Choose a category:",
            options=list(QUIZ_DATA.keys()),
            key="topic_select"
        )
        
        # Display topic info
        if topic:
            st.info(f"📊 This quiz contains 10 multiple-choice questions about {topic}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Start button
        if st.button("🚀 Start Quiz", type="primary"):
            # Validation
            errors = []
            if not validate_name(name):
                errors.append("❌ Please enter a valid name (at least 2 letters)")
            if not validate_email(email):
                errors.append("❌ Please enter a valid email address")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Initialize quiz
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.session_state.quiz_topic = topic
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.session_state.page = 'quiz'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Leaderboard button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏆 View Leaderboard"):
            st.session_state.page = 'leaderboard'
            st.rerun()
    
    # Stats footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    stats = get_user_stats(st.session_state.db_conn)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Quizzes", stats['total_attempts'])
    with col2:
        st.metric("📈 Average Score", f"{stats['avg_score']}%")
    with col3:
        st.metric("🔥 Popular Topic", stats['popular_topic'])
    with col4:
        st.metric("📚 Categories", len(QUIZ_DATA))

def show_quiz_page():
    """Display quiz questions"""
    
    topic = st.session_state.quiz_topic
    questions = QUIZ_DATA[topic]
    current_q = st.session_state.current_question
    
    # Progress bar
    progress = (current_q / len(questions))
    st.progress(progress)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## 📖 {topic} Quiz")
    with col2:
        st.markdown(f"### Question {current_q + 1}/{len(questions)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Question
    question_data = questions[current_q]
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("<div class='quiz-card'>", unsafe_allow_html=True)
        st.markdown(f"### {question_data['question']}")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Options
        answer = st.radio(
            "Select your answer:",
            options=question_data['options'],
            key=f"q_{current_q}",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation buttons
        col_a, col_b = st.columns(2)
        
        with col_a:
            if current_q > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col_b:
            if answer:
                button_text = "✅ Finish Quiz" if current_q == len(questions) - 1 else "Next ➡️"
                if st.button(button_text, type="primary", use_container_width=True):
                    # Save answer
                    selected_index = question_data['options'].index(answer)
                    is_correct = selected_index == question_data['correct']
                    
                    if current_q < len(st.session_state.answers):
                        st.session_state.answers[current_q] = is_correct
                    else:
                        st.session_state.answers.append(is_correct)
                    
                    # Calculate score
                    st.session_state.score = sum(st.session_state.answers)
                    
                    # Navigate
                    if current_q == len(questions) - 1:
                        # Quiz finished
                        save_result(
                            st.session_state.db_conn,
                            st.session_state.user_name,
                            st.session_state.user_email,
                            st.session_state.quiz_topic,
                            st.session_state.score,
                            len(questions)
                        )
                        st.session_state.page = 'results'
                        st.rerun()
                    else:
                        st.session_state.current_question += 1
                        st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_results_page():
    """Display quiz results"""
    
    score = st.session_state.score
    total = len(QUIZ_DATA[st.session_state.quiz_topic])
    percentage = (score / total) * 100
    
    title, message, color = get_feedback(score, total)
    
    # Header
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    
    # Score card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class='score-card'>
            <h1 style='font-size: 4rem; margin: 0; color: white;'>{score}/{total}</h1>
            <h2 style='color: white; margin: 1rem 0;'>{percentage:.1f}%</h2>
            <p style='font-size: 1.2rem; color: white;'>{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Details
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='quiz-card'>", unsafe_allow_html=True)
        
        st.markdown("### 📊 Quiz Summary")
        st.markdown(f"**Name:** {st.session_state.user_name}")
        st.markdown(f"**Topic:** {st.session_state.quiz_topic}")
        st.markdown(f"**Correct Answers:** {score} out of {total}")
        st.markdown(f"**Accuracy:** {percentage:.1f}%")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Take Another Quiz", use_container_width=True):
                st.session_state.page = 'landing'
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.rerun()
        
        with col_b:
            if st.button("🏆 View Leaderboard", type="primary", use_container_width=True):
                st.session_state.page = 'leaderboard'
                st.rerun()

def show_leaderboard_page():
    """Display leaderboard"""
    
    st.markdown("<h1 style='text-align: center;'>🏆 Leaderboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 2rem;'>Top performers across all quizzes</p>", unsafe_allow_html=True)
    
    # Get leaderboard data
    results = get_leaderboard(st.session_state.db_conn, limit=50)
    
    if results:
        # Convert to display format
        import pandas as pd
        df = pd.DataFrame(results, columns=['Name', 'Email', 'Topic', 'Score', 'Total', 'Percentage', 'Date'])
        df['Rank'] = range(1, len(df) + 1)
        df['Score'] = df['Score'].astype(str) + '/' + df['Total'].astype(str)
        df['Percentage'] = df['Percentage'].astype(str) + '%'
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Reorder columns
        df = df[['Rank', 'Name', 'Topic', 'Score', 'Percentage', 'Date']]
        
        # Display table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=600
        )
    else:
        st.info("No quiz results yet. Be the first to take a quiz!")
    
    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()

if __name__ == "__main__":
    main()
