# Job Simple Proxy Server : K8S Job을 생성 / 조회 / 삭제하는 역할 수행하는 서버

## 목적

Rest API을 통해 Job에 대한 생성 / 조회 / 삭제를 요청하면, 주어진 요청에 따라 K8S ApiServer에 호출해 처리하는 간단한 Proxy Server

* `GET /jobs?namespace=<namespace>` : 네임스페이스 내 정의된 job 정보 가져오기
* `POST /jobs` : job 생성하기
* `DELETE /jobs` : job 제거하기

## 환경 설치하기

````shell
# 1. poetry 설치 
pip install poetry

# 2. 가상환경 구성 및 실행
poetry env use 3.11 
source .venv/bin/activate

# 3. 패키지 의존성 설치
python -m poetry install
````

## 서버 실행하기

````shell
python -m uvicorn proxy_server.app:app --host 0.0.0.0 --port 8000
````


