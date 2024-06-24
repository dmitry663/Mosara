from flask import Flask

app = Flask(__name__)

class Get:
    def __init__(self, x):
        self.x = x 
 
    def __call__(self, func):
        def wrapper(path):
            return app.route(path+self.x, methods=)(func)
        return wrapper 