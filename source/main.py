from app.main import APP
import os

app = APP()

app.domain = "dmiry.shop"
app.SSL = True
app.SSL_CERTFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ssl/certificate.crt")
app.SSL_KEYFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ssl/private.key")
app.HTTP_PORT = 80
app.HTTPS_PORT = 443

if __name__ == '__main__':
    app.run()