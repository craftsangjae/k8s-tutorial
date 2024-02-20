# Job Simple Proxy Server : K8S Job을 생성 / 조회 / 삭제하는 역할 수행하는 서버

## 목적

Rest API을 통해 Job에 대한 생성 / 조회 / 삭제를 요청하면, 주어진 요청에 따라 K8S ApiServer에 호출해 처리하는 간단한 Proxy Server.

Job은 원주율 계산하는 함수이며, parameter로 넘긴 값이 원주율의 자리수. parameter로 10을 넘기면, 원주율 10자리까지 계산.

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

## Swagger 화면보기

fastapi에서는 swagger를 자동으로 지원해주므로, http://localhost:8000/docs 주소로 api 화면을 확인 가능

### 호출 순서를 통한 동작 확인

1. `POST /jobs`을 통해, 내가 원하는 파라미터를 담은 채로 job이 실행되는지를 확인

원주율 20자리를 생성하는 job 생성

````shell
curl -X POST -H "Content-Type: application/json"  -d '{"name": "pi-20", "namespace": "default", "value": 20}' http://localhost:8000/jobs
````

2. `kubctl`을 통해 해당 job의 출력값 확인

job이 정상적으로 동작했다면, 아래와 같이 출력

````shell
kubectl logs job/pi-20
>>> 3.1415926535897932385
````

3. `GET /jobs`을 통해 해당 job의 현황 조회

아래와 같이 default 네임스페이스에서의 결과가 노출

````shell
curl -X GET  http://localhost:8000/jobs
>>> [{"name":"pi-20","namespace":"default","active":null,"failed":null,"ready":0,"succeeded":1}]
````

4. `DELETE /jobs`을 통해 해당 job 제거

````shell
curl -X DELETE -H "Content-Type: application/json"  -d '{"name": "pi-20", "namespace": "default"}' http://localhost:8000/jobs
````