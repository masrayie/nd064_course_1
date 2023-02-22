import sqlite3
import logging
import json
import datetime
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

def count_connection(conn, action):
    countConn = conn.execute('INSERT INTO dbconn (action, connect) VALUES (?, ?)',
                (action, True))

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

dateandtime = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info(dateandtime + ", Article with id=" + str(post_id) + " is not found. 404 Page is returned.")
        return render_template('404.html'), 404
    else:
        app.logger.info(dateandtime + ', Article "' + post['title'] + '" retrieved!')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info(dateandtime + ', About Us page is retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(dateandtime + ', New Article "'+ title + '" is created!')
            return redirect(url_for('index'))

    return render_template('create.html')

# Define Healthcheck endpoint
@app.route('/healtz')
def healtz():
    response = app.response_class(
        response=json.dumps({
            "result": "OK-Healthy"
        }),
        status=200,
        mimetype='application/json'
    )
    app.logger.info(dateandtime + ', Healthz Endpoint request is succcess')
    return response

# Define Healthcheck endpoint
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    allPost = connection.execute('SELECT COUNT(*) as totalPost FROM posts').fetchall()
    connectionCount = connection.execute("SELECT COUNT(*) as totalCount FROM sqlite_master WHERE type='table'").fetchall()
    connection.close()
    response = app.response_class(
        response=json.dumps({
            "db_connection_count": connectionCount[0]['totalCount'],
            "post_count": allPost[0]['totalPost']
        }),
        status=200,
        mimetype='application/json'
    )
    app.logger.info(dateandtime + ', Metrics Endpoint request is succcess.')
    return response

# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    app.run(host='0.0.0.0', port='3111')
