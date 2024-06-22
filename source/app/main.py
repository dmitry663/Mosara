from flask import Flask, request, redirect
import ssl
import os
import threading 

app = None
domain = "dmiry.shop"
SSL = False
SSL_CERTFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../ssl/certificate.crt")
SSL_KEYFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../ssl/private.key")
HTTP_PORT = 80
HTTPS_PORT = 443

app = Flask(__name__)

@app.before_request
def before_request():
    if SSL:
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
    else:
        if request.url.startswith('https://'):
            url = request.url.replace('https://', 'http://', 1)
            code = 301
            return redirect(url, code=code)

def run_http():
    app.run(host='0.0.0.0', port=HTTP_PORT)

def run_https():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile=SSL_CERTFILE, keyfile=SSL_KEYFILE)
    
    app.run(host='0.0.0.0', port=HTTPS_PORT, ssl_context=ssl_context)

@app.route('/')
def hello():
    return "Hello, World!"

class APP:
    def run(self):
        global SSL
        global HTTP_PORT
        global HTTPS_PORT
        global SSL_CERTFILE
        global SSL_KEYFILE

        if self.SSL:
            SSL = self.SSL
        if self.SSL:
            HTTP_PORT = self.HTTP_PORT
        if self.SSL:
            HTTPS_PORT = self.HTTPS_PORT
        if self.SSL:
            SSL_CERTFILE = self.SSL_CERTFILE
        if self.SSL:
            SSL_KEYFILE = self.SSL_KEYFILE

        if SSL:
            thread = threading.Thread(target = run_http)
        else:
            thread = threading.Thread(target = run_https)

        thread.start()

        if SSL:
            run_https()
        else:
            run_http()

        exit(0)
      
        



    






