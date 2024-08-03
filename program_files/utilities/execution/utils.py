# utilities/utils.py

import json
from pathlib import Path

home_dir = Path(__file__).resolve().parent.parent.parent.parent
now_dir = Path(__file__).resolve().parent
print(home_dir)
# 홈 디렉토리 설정
def read_json_file(file_path):
    """JSON 파일을 읽어 딕셔너리로 반환하는 함수"""
    try:
        with open(now_dir/file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from the file {file_path}: {e}")
    return None

class DotDict(dict):
    """Dictionary that supports dot notation as well as dictionary access notation."""
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        try:
            del self[attr]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{attr}'")

    def __getitem__(self, key):
        if isinstance(key, str) and key in self:
            return super().__getitem__(key)
        else:
            raise KeyError(f"Key '{key}' not found in DotDict")

    def __setitem__(self, key, value):
        if isinstance(key, str):
            super().__setitem__(key, value)
        else:
            raise KeyError(f"Key '{key}' not found in DotDict")

    def __delitem__(self, key):
        if isinstance(key, str) and key in self:
            super().__delitem__(key)
        else:
            raise KeyError(f"Key '{key}' not found in DotDict")

def to_dotdict(d):
    if isinstance(d, dict):
        return DotDict({k: to_dotdict(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [to_dotdict(i) for i in d]
    else:
        return d