from os import environ
from flask import Flask

app = Flask(__name__)
@app.route("/")

app.run(host= '0.0.0.0', port=environ.get('PORT'))

print('trees-planted Web Server in Flask')
print('Deployed on Heroku\n')