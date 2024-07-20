# program_files/server_router/app.py
from flask import Flask, request, Response
from pathlib import Path
import requests
import json

routing_list_file_path = Path(__file__).resolve().parent / "routing_list.json"
app_list = []

def read_json_file(file_path):
    """JSON 파일을 읽어 딕셔너리로 반환하는 함수"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from the file {file_path}: {e}")
    return None

class AppEntity:
    def __init__(self, app_data):
        try:
            self.name = app_data['name']
        except KeyError as e:
            self.name = None

        try:
            self.host = app_data['host']
            self.port = app_data['port']
            self.expath = app_data['External path']
            self.inpath = app_data['Internal path']
        except KeyError as e:
            print(f"앱 데이터{self.name}에 키워드 '{e.args[0]}'가 없습니다.")
            raise Exception(f"앱 데이터{self.name}에 키워드 '{e.args[0]}'가 없습니다.")

def get_url(path):
    search = [app_data for app_data in app_list if app_data.expath.startswith(path)]
    if not len(search):
        return None
    app_data= search[0]
    return f"http://{app_data.host}:{app_data.port}/{app_data.inpath + path[len(app_data.expath):]}"

app = Flask(__name__)

def host_request(target_url):
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


@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def proxy(path):
    target_url = get_url(path)

    if target_url == None:
        return 

    return host_request(target_url)

def main():
    if not routing_list_file_path.exists():
        print(f"파일({routing_list_file_path})이 존재하지 않습니다.")
        return

    config_data = read_json_file(routing_list_file_path)
    if not config_data:
        print(f"설정 파일{routing_list_file_path} 설정 데이터를 읽지 못했습니다.")
        return
    try:
        apps = config_data['apps']
    except KeyError as e:
        print(f"앱 데이터 리스트('{e.args[0]}')가 없습니다.")
        return

    
    for app_data in apps:
        try:
            ape = AppEntity(app_data)
            app_list.append(ape)
        except Exception as e:
            print(e)
            continue

    app.run(port=5000)

if __name__ == '__main__':
    main()

