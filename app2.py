'''''
to add user from webpage
to delete user from webpage
to edit user information
'''

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'user_details'

mysql = MySQL(app)


# Display Users
@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('users1.html', users=users)

# Add User
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('users'))

# Update User
@app.route('/edit_user/<int:id>', methods=['POST'])
def edit_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('users'))

# Delete User
@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True)
