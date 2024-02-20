# CronJob Proxy Server : K8S CronJob을 생성 / 조회 / 삭제하는 서버

## 목적

Rest API을 통해 Job에 대한 생성 / 조회 / 삭제를 요청하면, 주어진 요청에 따라 K8S ApiServer에 호출해 처리하는 간단한 Proxy Server.

Cron Job은 현재 서버 시각을 echo로 찍는 함수

* `GET /cron-jobs?namespace=<namespace>` : 네임스페이스 내 정의된 cron-job 정보 가져오기
* `POST /cron-jobs` : cron-job 생성하기
* `DELETE /cron-jobs` : cron-job 제거하기

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

## Swagger 화면보기

fastapi에서는 swagger를 자동으로 지원해주므로, http://localhost:8000/docs 주소로 api 화면을 확인 가능
