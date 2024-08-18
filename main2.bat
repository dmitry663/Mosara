@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 현재 배치 파일이 위치한 디렉토리의 절대 경로 얻기
set "SCRIPT_DIR=%~dp0"
echo "%SCRIPT_DIR%"