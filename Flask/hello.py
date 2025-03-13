""""
This is the firsth progra wherein Hi flaskers! is printed on the screen.
The output can be observed on the webscreen.
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hi Flaskers!"

if __name__ == '__main__':
    app.run(debug=True)

