from flask import Flask, render_template, request, session, flash, redirect, url_for
import os
import openai
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import json

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret  # set the secret key

def save_users(users):
    with open('users2.json', 'w') as f:
        json.dump(users, f)

def load_users():
    try:
        with open('users2.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

users = load_users()

# This function checks if the user is logged in
def is_logged_in():
    return 'username' in session

@app.route('/index', methods=['GET', 'POST'])
def index():
    image_url0 = None
    image_url1 = None
    image_url2 = None
    if request.method == 'POST':
        description = request.form['desc']
        style = request.form['style']

        client = openai.OpenAI(api_key='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')

        try:
            response1 = client.images.generate(
                model="dall-e-3",
                prompt=description + " in " + style + " style",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            response2 = client.images.generate(
                model="dall-e-2",
                prompt=description + " in " + style + " style",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            response3 = client.images.generate(
                model="dall-e-2",
                prompt=description + " in " + style + " style",
                size="1024x1024",
                quality="standard",
                n=1,
            )

            if response1 and response1.data:
                image_url0 = response1.data[0].url
            if response2 and response2.data:
                image_url1 = response2.data[0].url
            if response3 and response3.data:
                image_url2 = response3.data[0].url
             
        except Exception as e:
            print(f"An error occurred: {e}")

    return render_template('index.html', url0=image_url0,url1=image_url1,url2=image_url2)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rePassword = request.form['rePassword']

        # Check if passwords match
        if password != rePassword:
            error = 'Passwords do not match! Please try again.'
        elif username in users:  # Check if username already exists
            error = 'Username already exists! Please choose a different username.'
        else:
            # Store the username and hashed password
            users[username] = generate_password_hash(password)
            save_users(users)  # Save users to file
            flash('Signup successful! You can now log in.')
            return redirect(url_for('Login'))  # Redirect to login page after successful signup

    return render_template('SignUp.html', error=error)


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists and password is correct
        if username in users and check_password_hash(users[username], password):
            session['username'] = username  # log the user in by setting a session variable
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            error = 'Invalid username or password! Please try again.'
    return render_template('Login.html', error=error)

@app.route('/navbar', methods=['GET', 'POST'])
def navbar():
    return render_template('navbar.html')

@app.route('/Logout')
def Logout():
    session.pop('username', None)  # Clear the 'username' key from the session
    flash('You have been logged out.')
    return redirect(url_for('Login'))

if __name__ == '__main__':
    app.run(debug=True)


    