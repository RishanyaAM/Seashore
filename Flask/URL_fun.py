""""
This code allows user to play with the url the name give in the url is printeed on the screen.
output can be observed ussing the url : localhost:5000/user/test this gives hello test as the output.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hi Flaskers!"

@app.route('/user/<name>')
def user(name):
    return "<b><i>Hello {}</b></i>".format(name)


if __name__ == '__main__':
    app.run(debug=True,port=5000)
