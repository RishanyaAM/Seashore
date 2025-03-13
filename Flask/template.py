""""
The following code is an example of how to use render template in Flask.
The template is written in HTML file and stored inside Templates folder.
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('first.html')

if __name__ == '__main__':
    app.run(debug=True)