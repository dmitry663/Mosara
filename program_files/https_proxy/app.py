# program_files/https_proxy/app.py
from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    # 원본 서버 URL
    target_url = f"http://127.0.0.1:5000/{path}"

    # 원본 서버로 요청 보내기
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    # 원본 서버의 응답을 클라이언트로 전달
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    # SSL 인증서 파일 경로 설정
    SSL_CERTFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssl/certificate.crt")
    SSL_KEYFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssl/private.key")
    
    # SSL 설정 로드
    ssl_context = (SSL_CERTFILE, SSL_KEYFILE)
    
    # 앱 실행
    app.run(host='0.0.0.0', port=443, ssl_context=ssl_context)
