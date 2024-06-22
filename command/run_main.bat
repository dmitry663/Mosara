@echo off
REM 가상 환경 활성화
call myvenv\Scripts\activate

REM main.py 실행
python source\main.py

REM 가상 환경 비활성화
deactivate