from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/json')
def get_json():
    with open('static/src/site.json', 'r') as f:
        file = f.read()
    data = json.loads(file)
    return data

@app.route('/')
def home():
    with open('static/src/site.json', 'r') as f:
        file = f.read()
    data = json.loads(file)
    return render_template('home.html', content = data)

if __name__ == '__main__':
    app.run(port=8008, debug=True)