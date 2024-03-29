# K8S Sample Codes

## 목적

K8S에 관련된 기술 노트 레포입니다. (1) K8S에 관련된 **기술적인 이슈**, (2) 그에 관련된 **해결방안** 을 간단한 샘플 코드들로 구성해서 정리하였습니다.

## 실행 환경

가급적이면 쉬운 재현과 테스트를 위해, 로컬 환경 쿠버네티스인 [minikube](https://minikube.sigs.k8s.io/docs/start/)를 활용하였습니다. 실제 배포 상황에서와 차이가 발생할 수
있는 부분은 별도로 기술합니다.

**세팅 환경**

* K8S Version : v1.26.3

## 목차

- [Local S3 구축하기](docs/001_local_s3_구성하기.md)

    - **기술 이슈**
        - 외부 클라이언트에서 클러스터 내에서만 접근 가능하도록 되어 있는 `Pod`에 생성된 `내부 포트`로 어떻게 접근할 수 있는가?

    - **해결 방안**
        - kubectl의 `port-forward`을 통해 외부 포트와 내부 포트를 포워딩하여 해결

    - **예제 상황**
        - 클러스터 내 S3의 Service 타입이 내부 클러스터에게만 포트가 열려있는 `clusterIp`로 되어 있는 경우, 외부 클라이언트에서 어떻게 S3에 호출할 수 있는가?

- [Job을 생성하는 Pod 구성하기](docs/002_job을_생성하는_pod_구성하기.md)

    - **기술 이슈**
        - 유저가 각기 다른 요청에 따라 배치 처리(ex: 모델 학습 / 데이터 전처리)을 생성해야 하는 상황에서, 어떤 식으로 요청 때마다 Job을 만들어 줄 수 있는가?
        - 호출 순서 : <유저> --> (K8S 내 웹 서버) --> (K8S API-Server) --> (K8S Job)

    - **해결 방안**
        - K8S 내 웹 서버에서 K8S API-Server로는 API 통신이 가능. 특히 클라이언트 라이브러리들이 잘 조성되어
          있어, [kubernetes-client](https://github.com/kubernetes-client/python)을 설치해서 호출해서 Job을 생성 가능

        - K8S API-Server로의 호출은 RBAC을 통해 권한을 열어주어야 함

    - **예제 상황**
        - 유저가 요청 시, N 자리 수에 대한 원주율을 계산하는 Job이 있다고 하자. 외부 API를 통해 서버를 호출하면 서버에서 K8S을 통해 원주율을 계산.

- [CronJob을 생성하는 Pod 구성하기](docs/003_cronjob을_생성하는_pod_구성하기.md)

    - **기술 이슈**
        - 유저가 각기 다른 요청에 따라 배치 처리(ex: 모델 학습 / 데이터 전처리)에 대한 스케쥴링 잡을 생성할 수 있는가?
        - 호출 순서 : <유저> --> (K8S 내 웹 서버) --> (K8S API-Server) --> (K8S CronJob)

    - **해결 방안**
        - Airflow의 대안책으로 Kubernetes에 CronJob이 존재. 이를 활용해서 처리 가능

    - **예제 상황**
        - 유저가 요청 시, N 자리 수에 대한 원주율을 계산하는 Job이 있다고 하자. 외부 API를 통해 서버를 호출하면 서버에서 K8S을 통해 원주율을 계산.

- [standalone_object_storage_구축](docs/004_standalone_object_storage_구축.md)

    - 목적 : K8S에 standalone object storage 구축