from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates')


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/register')
def register():
    return render_template('register.html')
