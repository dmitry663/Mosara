### 서버 접속
명령 프로토콜
```
"C:\Program Files\Git\bin\bash.exe" -c "ssh -i 'note_pro.pem' ec2-user@ec2-15-165-77-85.ap-northeast-2.compute.amazonaws.com"
```
### git 설치
Fedora 계열
```
sudo dnf install git-all -y
```
데비안 계열
```
sudo apt install git-all -y
```
### Mosara 앱 다운로드
```
git clone https://github.com/dmitry663/Mosara.git
```
### Mosara 앱 변경 내용 가져오기
```
cd Mosara
git pull origin main
cd ..
```
### Mosara 앱 환경설정
python3 설치 여부 확인
```
python3 --version
```
가상 환경 생성
```
python3 -m venv Mosara/venv
```
#### Mosara 앱 환경설정 (Windows)
```
# 가상 환경 활성화 (Windows)
Mosara\venv\Scripts\activate

#
pip install -r Mosara/systems/data/python/requirements.txt

# 가상 환경 비활성화
deactivate
```
#### Mosara 앱 환경설정 (macOS/Linux)
```
# 가상 환경 활성화 (macOS/Linux)
source Mosara/venv/bin/activate

# 
pip install -r Mosara/systems/data/python/requirements.txt

# 가상 환경 비활성화
deactivate
```
### Mosara 앱 실행
#### Mosara 앱 실행 (Windows)
```
# 가상 환경 활성화 (Windows)
Mosara\venv\Scripts\activate

# Mosara 앱 실행
python Mosara/systems/boot/start_app_batch.py

# 가상 환경 비활성화
deactivate
```
#### Mosara 앱 실행 (macOS/Linux)
```
# 가상 환경 활성화 (macOS/Linux)
source Mosara/venv/bin/activate

# Mosara 앱 실행
python Mosara/systems/boot/start_app_batch.py

# 가상 환경 비활성화
deactivate
```