import json
import subprocess
from pathlib import Path
import threading

# 홈 디렉토리 설정
home_dir = Path(__file__).resolve().parent.parent.parent
print(f"홈 디렉토리: {home_dir}")

# 설정 파일 경로 설정
config_file_path = home_dir / "systems/data/config/app_list.json"
print(f"설정 파일 경로: {config_file_path}")

def is_parent_path(parent, child):
    """부모 경로가 자식 경로의 부모인지 확인하는 함수"""
    try:
        parent_path = Path(parent).resolve()
        child_path = Path(child).resolve()
        return parent_path in child_path.parents
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def is_home_exists(file_path):
    """파일 경로가 홈 디렉토리 내에 존재하는지 확인하는 함수"""
    if not is_parent_path(home_dir, file_path):
        print(f"홈 디렉토리({home_dir}) 내에 파일({file_path})이 존재하지 않습니다.")
        return False
    if not file_path.exists():
        print(f"파일({file_path})이 존재하지 않습니다.")
        return False
    return True

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
            self.executable = app_data['executable']
            self.path = home_dir / Path(app_data['path'])
            
            if not is_home_exists(self.path):
                print(f"파일({self.path})이 존재하지 않습니다.")
                raise Exception(f"파일({self.path})이 존재하지 않습니다.")

            self.command = f"{self.executable} {self.path}"
            print(self.command)

        except KeyError as e:
            print(f"앱 데이터{self.name}에 키워드 '{e.args[0]}'가 없습니다.")
            raise Exception(f"앱 데이터{self.name}에 키워드 '{e.args[0]}'가 없습니다.")

        def subprocess_run():
            subprocess.run(self.command, shell=True)
        
        self.thread = threading.Thread(target = subprocess_run) 

    def run(self):
        self.thread.start()

def main():

    if not is_home_exists(config_file_path):
        return

    config_data = read_json_file(config_file_path)
    if not config_data:
        print(f"설정 파일{config_file_path} 설정 데이터를 읽지 못했습니다.")
        return
    try:
        apps = config_data['apps']
    except KeyError as e:
        print(f"앱 데이터 리스트('{e.args[0]}')가 없습니다.")
        return

    app_list = []
    for app_data in apps:
        try:
            ape = AppEntity(app_data)
            ape.run()
            app_list.append(ape)
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()