# Parsing-Job-Proxy-Server

## 목적

K8S 리소스(job)을 제어하는 WAS 서버 구축

## 시나리오

Proxy-Server는 유저의 요청에 따라, K8S에서 특정한 Job을 대신 생성해주는 역할을 수행하는 Web Application Server 입니다.

## 구성

### webapp 구성

* `proxy-server` : 유저의 요청에 따라 job을 생성하는 proxy 서버
    * 경로 : [webapp](webapp/README.md)

### Job 유형

* `Preloading Job` : 데이터를 시스템에 적재하는 job
    * 경로 : [jobs/parsing_job](jobs/parsing_job/README.md)

* `Parsing Job` : 파싱한 데이터를 적재하는 Job
    * 경로 : [jobs/preloading_job](jobs/preloading_job/README.md)

#### Infrastructure 구성

* `minio` : 데이터를 적재할 Object Storage
