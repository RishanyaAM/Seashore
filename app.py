''''
install mysql by running the command : pip install flask-mysqldb
and this code is just to connect the database and execute basic query
'''
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'user_details'

mysql = MySQL(app)

@app.route('/')
def index():
    return "MySQL Connection Successful"

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return str(users)

if __name__ == '__main__':
    app.run(debug=True)
