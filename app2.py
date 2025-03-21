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
'''
Good question! Let's go deeper into why **using `GET` for deleting users is a security risk** and how to fix it.  

---

## **🔴 Why Is `GET` Dangerous for Deleting Users?**
Currently, your delete route is:
```python
@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('users'))
```
### **🚨 Security Issues:**
1. **Accidental Deletions**  
   - Since `GET` requests are made just by **visiting a URL**, a user could accidentally delete a record just by clicking a link like:
     ```
     http://yourwebsite.com/delete_user/5
     ```
   - Even search engines **automatically crawl** links, which could trigger unwanted deletions.

2. **CSRF (Cross-Site Request Forgery) Attack**  
   - An attacker could trick an **authenticated admin** into clicking a malicious link:
     ```html
     <img src="http://yourwebsite.com/delete_user/10" />
     ```
   - This would send a `GET` request and delete user **ID 10**, without admin's knowledge.

3. **No Confirmation Before Deletion**  
   - If a user clicks a delete link, there's **no confirmation** step.

---

## **✅ How to Fix It: Use `POST` Instead**
A better approach is to **change the method from `GET` to `POST`** so that deletions require a **form submission** instead of just visiting a link.

### **🔹 Fix the Route**
Modify the route to accept only `POST`:
```python
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('users'))
```
- Now, the **user must submit a form** to delete a record.

### **🔹 Update the HTML Form**
Instead of using a simple `<a>` tag, use a form with a **POST** method:
```html
<form action="{{ url_for('delete_user', id=user[0]) }}" method="POST" onsubmit="return confirm('Are you sure?');">
    <button type="submit">Delete</button>
</form>
```
✔️ **This prevents accidental deletions** and adds a **confirmation prompt**.

---

## **✅ Even Better: Use `DELETE` Instead of `POST`**
RESTful APIs recommend using the **`DELETE` method** for deleting resources.

Modify your route:
```python
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User deleted successfully'}), 200
```
And in the frontend (JavaScript example):
```js
fetch('/delete_user/10', {
    method: 'DELETE'
}).then(response => response.json())
  .then(data => console.log(data.message));
```
✔️ This **follows RESTful principles** and is more secure.

---

## **🚀 Summary**
❌ **Bad Practice (Insecure):**  
```python
@app.route('/delete_user/<int:id>', methods=['GET'])
```
- Can be triggered **accidentally** by visiting a URL.
- Vulnerable to **CSRF attacks**.

✅ **Better Practice (Secure):**  
```python
@app.route('/delete_user/<int:id>', methods=['POST'])
```
- Requires an **explicit form submission**.
- Adds **confirmation prompts**.

🔥 **Best Practice (RESTful API):**  
```python
@app.route('/delete_user/<int:id>', methods=['DELETE'])
```
- Uses the correct **HTTP method (`DELETE`)**.
- Can be triggered securely via **AJAX requests**.

'''
