from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/name', methods=['POST', 'GET'])
def name():
    error = None
    result = get_database()
    if request.method == 'POST':
        result = valid_name(request.form['FirstName'], request.form['LastName'])
        if result:
            return render_template('input.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('input.html', error=error, result=result)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    error = None
    result = get_database()
    if request.method == 'POST':
        result = valid_delete(request.form['FirstName'], request.form['LastName'])
        if result:
            return render_template('delete.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('delete.html', error=error, result=result)


def valid_name(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()

def valid_delete(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);')
    connection.execute('DELETE FROM users WHERE firstname=? AND lastname=?;', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()

def get_database():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()

if __name__ == "__main__":
    app.run()


