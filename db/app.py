from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'boat_reservation_db'

mysql = MySQL(app)

@app.route('/')
def index():
    if 'sailor_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sailor_id = request.form['sailor_id']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sailors WHERE sailor_id = %s AND password = %s", (sailor_id, password))
        sailor = cur.fetchone()
        cur.close()
        
        if sailor:
            session['sailor_id'] = sailor[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'sailor_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    
    # Fetch available boats
    cur.execute("SELECT * FROM boats WHERE boat_id NOT IN (SELECT boat_id FROM reserves)")
    boats = cur.fetchall()
    
    # Fetch reservations with sailor names
    cur.execute('''SELECT r.reserve_id, s.name, b.name, r.reserve_date
                   FROM reserves r
                   JOIN sailors s ON r.sailor_id = s.sailor_id
                   JOIN boats b ON r.boat_id = b.boat_id''')
    reservations = cur.fetchall()
    
    cur.close()
    
    return render_template('dashboard.html', boats=boats, reservations=reservations)

@app.route('/reserve/<int:boat_id>', methods=['POST'])
def reserve(boat_id):
    if 'sailor_id' not in session:
        return redirect(url_for('login'))

    sailor_id = session['sailor_id']
    reservation_date = request.form['reservation_date']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO reserves (sailor_id, boat_id, reserve_date) VALUES (%s, %s, %s)",
                (sailor_id, boat_id, reservation_date))
    mysql.connection.commit()
    cur.close()

    flash('Boat reserved successfully!')
    return redirect(url_for('dashboard'))

@app.route('/add_sailor', methods=['GET', 'POST'])
def add_sailor():
    if request.method == 'POST':
        sailor_name = request.form['sailor_name']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sailors (name, password) VALUES (%s, %s)", (sailor_name, password))
        mysql.connection.commit()
        cur.close()

        flash('Sailor added successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add_sailor.html')

@app.route('/add_boat', methods=['GET', 'POST'])
def add_boat():
    if request.method == 'POST':
        boat_name = request.form['boat_name']
        capacity = request.form['capacity']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO boats (name, capacity) VALUES (%s, %s)", (boat_name, capacity))
        mysql.connection.commit()
        cur.close()

        flash('Boat added successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add_boat.html')

@app.route('/reservations')
def reservations():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT r.reserve_id, s.name, b.name, r.reserve_date 
                   FROM reserves r 
                   JOIN sailors s ON r.sailor_id = s.sailor_id 
                   JOIN boats b ON r.boat_id = b.boat_id''')
    reservations = cur.fetchall()
    cur.close()

    return render_template('reservations.html', reservations=reservations)

@app.route('/logout')
def logout():
    session.pop('sailor_id', None)
    flash('Logged out successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)