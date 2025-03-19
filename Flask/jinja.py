from flask import Flask, render_template

app = Flask(__name__)
'''
to pass parameters to html template and get dynamic value for variables from web page
'''
@app.route('/')
def index():
    name = "Rishu"
    my_list = ['good', 'Lit', 25]
    return render_template('jinja.html', name=name, lis = my_list)
'''
passing variables and demonstration of filters
'''
@app.route('/user/<name>')
def user(name):
    return render_template('jinja.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)