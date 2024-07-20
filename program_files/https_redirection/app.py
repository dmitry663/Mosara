# program_files/https_redirection/app.py
from flask import Flask, request, redirect, url_for, Response
import requests

app = Flask(__name__)

@app.before_request
def enforce_https_in_production():
    # HTTP 요청을 HTTPS로 리디렉션
    if not request.is_secure:
        url = url_for(request.endpoint, _scheme='https', _external=True, **request.view_args)
        return redirect(url)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)