from flask import Flask, render_template, request, redirect, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Database configuration
db_con = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "websitedata"
}

# Home page route
@app.route('/')
def index():
    logged_in = 'user_id' in session
    return render_template('index.html', logged_in=logged_in)

# About page route
@app.route('/about')
def about():
    logged_in = 'user_id' in session
    return render_template('about.html', logged_in=logged_in)

# Contact page route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    logged_in = 'user_id' in session
    
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        query = request.form['query']

        try:
            # Connect to the database
            con = pymysql.connect(**db_con)
            cur = con.cursor()

            # Insert the data into the `contact_queries` table
            cur.execute("""
                INSERT INTO contact_queries (name, email, query)
                VALUES (%s, %s, %s)
            """, (name, email, query))
            
            con.commit()
            message = "Thank you! Your query has been submitted successfully."

        except Exception as e:
            message = f"An error occurred: {e}"

        finally:
            con.close()

        return render_template('contact.html', logged_in=logged_in, message=message)

    # Render the form if the request method is GET
    return render_template('contact.html', logged_in=logged_in)


# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # Connect to the database
            con = pymysql.connect(**db_con)
            cur = con.cursor()

            # Query both tables
            cur.execute("""
                SELECT l.id, l.password 
                FROM login l
                JOIN signup s ON l.username = s.username
                WHERE l.username = %s
            """, (username,))
            user = cur.fetchone()

            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                return redirect('/')
            else:
                return 'Invalid username or password'

        finally:
            con.close()

    return render_template('login.html')

# Signup page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        if password != confirm_password:
            return 'Passwords do not match'

        try:
            # Connect to the database
            con = pymysql.connect(**db_con)
            cur = con.cursor()

            # Check if the user already exists in either table
            cur.execute("SELECT id FROM signup WHERE username=%s OR email=%s", (username, email))
            existing_user_signup = cur.fetchone()
            cur.execute("SELECT id FROM login WHERE username=%s", (username,))
            existing_user_login = cur.fetchone()

            if existing_user_signup or existing_user_login:
                return 'Username or email already exists'

            # Insert into the `signup` table
            hashed_password = generate_password_hash(password)
            cur.execute("INSERT INTO signup (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, hashed_password))
            
            # Insert into the `login` table
            cur.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, hashed_password))
            
            con.commit()
            
            # Redirect to login page after successful signup
            return redirect('/login')

        finally:
            con.close()

    return render_template('signup.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/quiz')
def quiz():
    # Check if the user is logged in
    if 'user_id' not in session:
        # Redirect to login page if not logged in
        return redirect('/login')
    
    # If logged in, render the quiz page
    logged_in = True
    return render_template('quiz.html', logged_in=logged_in)

@app.route('/submit', methods=['POST'])
def submit_quiz():
    if request.method == 'POST':
        try:
            # Connect to the database
            con = pymysql.connect(**db_con)
            cur = con.cursor()

            # Fetch the correct answers from the database
            cur.execute("SELECT question_number, correct_answer FROM quiz_answers")
            correct_answers = dict(cur.fetchall())

            # Calculate the score
            score = 0
            total_questions = len(correct_answers)
            user_answers = {}

            for question, correct_answer in correct_answers.items():
                user_answer = request.form.get(f'question{question}')
                user_answers[question] = user_answer
                if user_answer == correct_answer:
                    score += 1

            # Optionally, you can log the user's score to the database or session
            return render_template('result.html', score=score, total_questions=total_questions, user_answers=user_answers)

        except Exception as e:
            return f"An error occurred: {e}"

        finally:
            con.close()



if __name__ == '__main__':
    app.run(debug=True)
