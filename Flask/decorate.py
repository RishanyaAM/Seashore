''''
how to add images and llink CSS and JS files 
'''
from flask import Flask , render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('decor.html')

if __name__ == '__main__':
    app.run(debug=True)