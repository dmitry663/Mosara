@echo off
REM Python 가상 환경 생성
python -m venv myvenv

REM 가상 환경 활성화
call myvenv\Scripts\activate

REM 패키지 설치
pip install -r requirements.txt

REM 가상 환경 비활성화
deactivate