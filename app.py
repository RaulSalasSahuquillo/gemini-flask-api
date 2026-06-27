from google import genai
from dotenv import load_dotenv
import os
import sqlite3
import hashlib
from flask import (
    Flask,
    request,
    render_template_string,
    flash,
    redirect,
    url_for,
    session,
)
import markdown
from training import training  # Library created to separate the training instructions

# Just discovered this way of rendering HTML
index_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='LogoEN.AI.png') }}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EN.AI - ENEI PROJECT</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;1,700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-black: #050505;
            --smoke-light: rgba(200, 200, 200, 0.15);
            --glow-text: rgba(255, 255, 255, 0.8);
            --panel-alpha: rgba(10, 10, 10, 0.7);
        }

        body {
            background-color: var(--bg-black);
            /* Background with radial gradient to simulate depth and smoke */
            background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
            color: #d4d4d4;
            font-family: 'Playfair Display', serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        /* Animated smoke layer (Visual effect) */
        body::before {
            content: "";
            position: absolute;
            width: 200%; height: 200%;
            background: url('https://www.transparenttextures.com/patterns/asfalt-dark.png');
            opacity: 0.2;
            animation: moveSmoke 60s linear infinite;
            pointer-events: none;
        }

        @keyframes moveSmoke {
            from { transform: translate(-10%, -10%); }
            to { transform: translate(0%, 0%); }
        }

        .container {
            width: 95%;
            max-width: 1200px;
            height: 90vh;
            background: var(--panel-alpha);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            flex-direction: column;
            position: relative;
            box-shadow: 0 0 50px rgba(0,0,0,1);
            z-index: 1;
        }

        .chat-header {
            padding: 40px 20px;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .chat-header h1 {
            font-family: 'Cinzel', serif;
            font-size: 2.5rem;
            margin: 0;
            letter-spacing: 8px;
            color: #fff;
            text-shadow: 0 0 15px var(--glow-text), 2px 2px 10px rgba(0,0,0,0.5);
            text-transform: uppercase;
        }

        .chat-header p {
            font-family: 'Cinzel', serif;
            font-size: 0.7rem;
            letter-spacing: 4px;
            opacity: 0.5;
            margin-top: 10px;
        }

        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 30px;
            display: flex;
            flex-direction: column;
            gap: 25px;
            mask-image: linear-gradient(to bottom, transparent, black 10%, black 90%, transparent);
        }

        .msg {
            max-width: 70%;
            padding: 15px 25px;
            position: relative;
            font-size: 1.05rem;
            animation: fadeIn 0.8s ease-in-out;
            border-left: 1px solid rgba(255,255,255,0.1);
        }

        @keyframes fadeIn { from { opacity: 0; filter: blur(5px); } to { opacity: 1; filter: blur(0); } }

        .author {
            display: block;
            font-family: 'Cinzel', serif;
            font-size: 0.6rem;
            margin-bottom: 8px;
            letter-spacing: 2px;
            color: var(--primary-neon);
            opacity: 0.6;
        }

        .user {
            align-self: flex-end;
            text-align: right;
            border-left: none;
            border-right: 1px solid rgba(255,255,255,0.2);
            background: linear-gradient(to left, rgba(255,255,255,0.03), transparent);
        }

        .ai {
            align-self: flex-start;
            background: linear-gradient(to right, rgba(255,255,255,0.03), transparent);
        }

        .input-form {
            padding: 30px;
            display: flex;
            background: rgba(0, 0, 0, 0.4);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        input[type="text"] {
            flex: 1;
            background: transparent;
            border: none;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding: 10px;
            color: #fff;
            font-family: 'Playfair Display', serif;
            font-size: 1.2rem;
            outline: none;
            transition: 0.4s;
        }

        input[type="text"]:focus {
            border-bottom-color: #fff;
            text-shadow: 0 0 5px var(--glow-text);
        }

        button {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #fff;
            padding: 0 30px;
            margin-left: 20px;
            font-family: 'Cinzel', serif;
            cursor: pointer;
            transition: 0.3s;
            letter-spacing: 2px;
        }

        button:hover {
            background: #fff;
            color: #000;
            box-shadow: 0 0 20px #fff;
        }

        .logout-btn {
            position: absolute;
            top: 20px; right: 20px;
            color: rgba(255,255,255,0.3);
            text-decoration: none;
            font-family: 'Cinzel', serif;
            font-size: 0.6rem;
            letter-spacing: 2px;
            transition: 0.3s;
        }

        .logout-btn:hover { color: #fff; }

        /* Invisible scrollbar */
        .chat-box::-webkit-scrollbar { width: 3px; }
        .chat-box::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); }
    </style>
</head>
<body>

<div class="container">
    <a href="{{ url_for('logout') }}" class="logout-btn">LOG OUT</a>
    
    <div class="chat-header">
        <img src="{{ url_for('static', filename='LogoInicio.png') }}" alt="Logo EN.AI" style="height: 60px; margin-bottom: 10px; filter: drop-shadow(0 0 10px var(--glow-text));">
        <h1>EN.AI</h1>
        <p>ENEI PROJECT // OPERATOR: {{ user }}</p>
    </div>

    <div class="chat-box" id="chatBox">
        {% for msg in chat %}
            <div class="msg {% if msg.author == 'You' %}user{% else %}ai{% endif %}">
                <span class="author">{{ msg.author }}</span>
                {{ msg.text | safe }}
            </div>
        {% endfor %}
    </div>

    <form method="POST" class="input-form">
        <input type="text" name="message" placeholder="Type to the system..." required autofocus autocomplete="off">
        <button type="submit">SEND</button>
    </form>
</div>

<script>
    const cb = document.getElementById('chatBox');
    cb.scrollTop = cb.scrollHeight;
</script>

</body>
</html>
"""

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session key

# AI CONFIGURATION
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    exit("Error: GEMINI_API_KEY not found.")

client = genai.Client(api_key=api_key)


# Function to create a new chat session
def create_chat():
    return client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": training(),
            "tools": [{"google_search": {}}],  # Tool for Google Search
        },
    )


# Initialize chat globally (or per session)
chat_session = create_chat()
history = []


# DATABASE
def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)


init_db()  # Call the function on startup


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Simple HTML for login.
login_template = """
<!DOCTYPE html>
<html>
<head><title>Login - EN.AI</title></head>
<body>
    <h2>Log In</h2> 
    <form method="POST">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <button type="submit">Log In</button>
    </form>
    <p><a href="{{ url_for('register') }}">Register</a></p>
    {% with messages = get_flashed_messages() %}{% if messages %}
        <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
    {% endif %}{% endwith %}
</body>
</html>
"""

# Simple HTML for registration
register_template = """
<!DOCTYPE html>
<html>
<head><title>Register - EN.AI</title></head>
<body>
    <h2>User Registration</h2>
    <form method="POST">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <button type="submit">Register</button>
    </form>
    <p><a href="{{ url_for('login') }}">Back to login</a></p>
    {% with messages = get_flashed_messages() %}{% if messages %}
        <ul>{% for msg in messages %}<li>{{ msg }}</li>{% endfor %}</ul>
    {% endif %}{% endwith %}
</body>
</html>
"""


# ROUTES
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = hash_password(request.form["password"])

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password),
            )
            user = cursor.fetchone()

        if user:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            flash("Incorrect username or password.")
    return render_template_string(login_template)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = hash_password(request.form["password"])
        try:
            with sqlite3.connect("users.db") as conn:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password),
                )
            flash("Registration successful. Log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.")
    return render_template_string(register_template)


@app.route("/", methods=["GET", "POST"])
def home():
    global chat_session, history

    # If no user in session, redirect to login
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            try:
                response = chat_session.send_message(user_message)
                history.append({"author": "You", "text": user_message})  # User message
                text_md = markdown.markdown(
                    response.text
                )  # Convert to Markdown for better display in the output
                history.append({"author": "EN.AI", "text": text_md})  # AI response
            except Exception as e:
                if "429" in str(e):  # Error 429 indicates rate limit.
                    error_msg = (
                        "Rate limit reached. Please wait a moment before continuing."
                    )
                else:
                    error_msg = f"An unexpected error occurred: {e}"
                history.append({"author": "System", "text": error_msg})
        return render_template_string(
            index_template, chat=history, user=session["username"]
        )

    # If GET (Reload), restart the chat
    history = []
    chat_session = create_chat()
    return render_template_string(
        index_template, chat=history, user=session["username"]
    )


# Route to log out
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5002)
