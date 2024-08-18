@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 현재 배치 파일이 위치한 디렉토리의 절대 경로 얻기
set "SCRIPT_DIR=%~dp0"

REM Python 설치 여부 확인
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python이 설치되어 있지 않습니다.
    echo Python을 먼저 설치해 주십시오.
    echo 스크립트를 종료합니다.
    exit /b 1
)

REM 가상 환경 디렉토리 설정
set "VENV_DIR=%SCRIPT_DIR%venv"
set "VENV_ACTIVATE_SCRIPT=%VENV_DIR%\Scripts\activate.bat"

REM 가상 환경 생성
if exist "%VENV_ACTIVATE_SCRIPT%" (
    echo 가상 환경이 이미 존재합니다.
) else (
    echo 가상 환경을 생성합니다...
    python -m venv %VENV_DIR%
    IF ERRORLEVEL 1 (
        echo 가상 환경 생성에 실패했습니다.
        exit /b 1
    ) ELSE (
        echo 가상 환경이 성공적으로 생성되었습니다.
    )
)

REM 가상 환경 활성화
call "%VENV_ACTIVATE_SCRIPT%"
IF ERRORLEVEL 1 (
    echo 가상 환경 활성화에 실패했습니다.
    exit /b 1
)

REM 요구 사항 파일 경로 설정
set "REQUIREMENTS_FILE=%SCRIPT_DIR%systems\data\python\requirements.txt"
set "INSTALLED_PACKAGES_FILE=%SCRIPT_DIR%systems\data\python\installed_packages.txt"

REM 설치된 패키지 목록을 요구 사항 파일과 비교
if exist "%REQUIREMENTS_FILE%" (
    echo 설치된 패키지를 확인하고 필요시 패키지를 설치합니다...

    REM 현재 설치된 패키지 목록을 요구 사항 파일과 동일한 위치에 저장
    pip freeze > "%INSTALLED_PACKAGES_FILE%"

    REM 패키지 목록을 requirements.txt와 비교하여 필요한 패키지 설치
    set "packages_to_install="
    for /f "delims=" %%i in ('type "%REQUIREMENTS_FILE%"') do (
        set "package=%%i"
        set "found=0"
        for /f "delims=" %%a in ('type "%INSTALLED_PACKAGES_FILE%"') do (
            set "packageaver=%%a"
            if /i "!packageaver:%package%=!" neq "!packageaver!" (
                set "found=1"
                REM goto break
            )
        )
        REM :break
        if !found! equ 0 (
            echo 패키지 !package!가 설치되어 있지 않거나 차이가 있습니다.
            set "packages_to_install=!packages_to_install! !package!"
        )
    )
    if defined packages_to_install (
        echo 다음 패키지를 설치합니다: %packages_to_install%
        pip install %packages_to_install%
        IF ERRORLEVEL 1 (
            echo 패키지 설치에 실패했습니다.
            exit /b 1
        ) ELSE (
            echo 패키지가 성공적으로 설치되었습니다.
        )
    ) ELSE (
        echo 모든 패키지가 이미 설치되어 있습니다.
    )
) ELSE (
    echo 요구 사항 파일이 존재하지 않습니다: %REQUIREMENTS_FILE%
    exit /b 1
)

REM Python 스크립트 실행
echo Python 스크립트를 실행합니다: %SCRIPT_DIR%systems\boot\start_app_batch.py
python "%SCRIPT_DIR%systems\boot\start_app_batch.py"
IF ERRORLEVEL 1 (
    echo Python 스크립트 실행에 실패했습니다.
    exit /b 1
) ELSE (
    echo Python 스크립트가 성공적으로 실행되었습니다.
)

REM 가상 환경 비활성화
deactivate

pause
