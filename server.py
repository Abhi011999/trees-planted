from os import environ
from flask import Flask

app = Flask(__name__)
@app.route("/")

def server():
    return "trees-planted Web Server in Flask.\nDeployed on Heroku\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=environ.get('PORT'))