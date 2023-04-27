import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from BrainModule import chatGPT
import sys
import argparse
import webview
import os
import threading

"""
Copyright (c) 2023 Boris Burgarella

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""




# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    conn.text_factory = str
    c = conn.cursor()
    # Create users table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT NOT NULL UNIQUE, 
                 password TEXT NOT NULL)''')
    # Create messages table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 message TEXT NOT NULL,
                 response TEXT NOT NULL,
                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

# Delete message history for a user
def delete_user_message_history(username):
    conn = sqlite3.connect('users.db')
    conn.text_factory = str
    c = conn.cursor()

    # Get the user_id for the provided username
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()

    if user_id is not None:
        # Delete messages with the corresponding user_id
        c.execute("DELETE FROM messages WHERE user_id = ?", (user_id[0],))
        conn.commit()
        print(f"Message history for user {username} has been deleted.")
    else:
        print(f"No user found with username {username}.")

    conn.close()

# Add a new user to the users table
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    conn.text_factory = str
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
              (username, generate_password_hash(password)))
    conn.commit()
    conn.close()

# Verify a user's credentials
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    conn.text_factory = str
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[2], password):
        return user
    else:
        return None

# Add a message and its response to the messages table
def add_message(user_id, message, response):
    conn = sqlite3.connect('users.db')
    conn.text_factory = str
    c = conn.cursor()
    c.execute('INSERT INTO messages (user_id, message, response) VALUES (?, ?, ?)', 
              (user_id, message, response))
    conn.commit()
    conn.close()

# Get the conversation history for a user
def get_messages(user_id, systemprompt):
    conn = sqlite3.connect('users.db')
    conn.text_factory = str
    conversation = []
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE user_id = ? ORDER BY timestamp', (user_id,))
    messages = c.fetchall()
    conversation.append({"role":"system", "content":systemprompt})
    for message in messages:
        conversation.append({"role":"user", "content":message[2]})
        conversation.append({"role":"assistant", "content":message[3]})
    conn.close()
    return conversation


# Create a Flask app instance and set a secret key for session management
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Define a route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    # Handle POST request for login or signup
    if request.method == 'POST':
        # Handle login request
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = verify_user(username, password)
            if user:
                # Set session variables and show success message
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash('You have successfully logged in.', 'success')
                return redirect(url_for('chat'))
            else:
                flash('Invalid username or password.', 'error')
        # Handle signup request
        elif 'signup' in request.form:
            return redirect(url_for('register'))
    return render_template('login.html')

# Define a route for the chat page
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    env_var = os.environ.get('OPENAI_API_KEY')
    # Show a popup if the API key is not set
    if env_var is None:
        show_popup = True
    else:
        show_popup = True

    # Get the conversation history
    conversation = get_messages(session['user_id'], chatBot.agent_data["PrePrompt"])

    # Redirect to login page if not logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Handle POST request for new message
    if request.method == 'POST':
        message = request.form['message']
        if "model" in request.form:
            model = request.form['model']
        else:
            model = "gpt-3.5-turbo"
        conversation = chatBot.thinkAbout(message, conversation, model=model)
        response = conversation[-1]["content"]
        user_id = session['user_id']
        add_message(user_id, message, str(response))

    return render_template('chat.html', username=session['username'], messages=conversation)

# Define a route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle POST request for registration or login
    if request.method == 'POST':
        # Handle registration request
        if 'register' in request.form:
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return redirect(url_for('register'))
            existing_user = verify_user(username, password)
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect(url_for('register'))
            add_user(username, password)
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        # Handle login request
        elif 'login' in request.form:
            return redirect(url_for('login'))

    return render_template('register.html')

# Define a route for the logout functionality
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove user session variables and show success message
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Define a route to reset the database for the current user
@app.route('/reset_database', methods=['GET', 'POST'])
def reset_db():
    delete_user_message_history(session['username'])
    return redirect(url_for('chat'))

# Function to run the Flask app
def run_flask():
    app.run(debug=False, host='127.0.0.1', port=5000)

# Definition of the parser
parser = argparse.ArgumentParser()
# The choice of agent
parser.add_argument("-a", "--agent", required=False, 
                    help="File with the preprompt to configure the agent")
# Choice of hosting (Azure or openAI)
parser.add_argument("-hst", "--host", required=False, 
                    help="Hosting service for chatGPT",
                    choices=["OpenAI", "Azure"], default="OpenAI")



if __name__ == '__main__':



    args = parser.parse_args()
    # Initialize chat bot instance
    chatBot = chatGPT(agent=args.agent, host=args.host)
    init_db()
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    webview.create_window('ChatBot', 'http://127.0.0.1:5000', width=960, height=800)
    webview.start()
