# Parsing-Job-Proxy-Server

## 목적

K8S 리소스(job)을 제어하는 WAS 서버 구축

## 시나리오

Proxy-Server는 유저의 요청에 따라,
K8S에서 특정한 Job을 대신 생성해주는 역할을 수행하는 Web Application Server.

### 구성

* [proxy_manager](proxy_manager/)
    * 프록시서버와 jobs에서 필요한 제어 로직 구현
    * 주요 로직
        * [settings](proxy_manager/settings.py) : Configuration에 대한 제어 로직
        * [storage](proxy_manager/storage.py) : object storage에 대한 제어 로직
        * [job_controller](proxy_manager/job_controller.py) : k8s job에 대한 제어 로직

* [webapp](webapp/README.md)
    * 유저의 요청에 따라 job을 생성하는 proxy 서버, fastAPI로 구성되어 있음

* [jobs](jobs/README.md)
    * 여러 유형의 job을 정의한 job script
    * 종류
        * [jobs/parsing_job](jobs/parsing_job/README.md) : 데이터를 시스템에 적재하는 job
        * [jobs/preloading_job](jobs/preloading_job/README.md) : 데이터를 시스템에 적재하는 job

