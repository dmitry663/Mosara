# systems/boot/start_app_batch.py
import os
import sys
from pathlib import Path

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../program_files/utilities/execution'))

sys.path.append(project_root)

from execution import Command
from utils import read_json_file, DotDict

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

class AppEntity:
    def __init__(self, app_data):
        self.command = Command(DotDict(app_data))

    def run(self):
        self.command.run_command_threading()

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
            app_list.append(ape)
        except Exception as e:
            print(e)

    for ape in app_list:
        try:
            ape.run()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()