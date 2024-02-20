# cronJob을 생성하는 Pod 구성하기

* related works
    - [resources/cronjob-proxy-server.yaml](../resources/cronjob-proxy-server.yaml)
    - [services/cronjob-proxy-server](../services/cronjob-proxy-server/README.md)

## 목표

1. K8S 내의 팟에서 유저의 요청 때마다, 새로운 CronJob을 생성 / 삭제 하는 로직 구현

## 구현

### 1. CronJob 생성 / 조회 / 삭제하기 위한 프록시 서버 구현

[cronjob-proxy-server 레포](../services/cronjob-proxy-server/proxy_server/app.py)는 FastAPI와 kubernetes client을
통해,
cronjob을 자유롭게 생성 / 조회 / 삭제 할 수 있는 WAS 코드입니다. 이를 Dockerfile을 통해 이미지를 빌드한
후, [Dockerhub](https://hub.docker.com/repository/docker/craftsangjae/cronjob-proxy-server)에 푸시했습니다.

프록시 서버의 API 목록

* `GET /cron-jobs` : 크론잡 정보 가져오기
* `POST /cron-jobs` : 크론잡 생성하기
* `DELETE /cron-jobs` : 크론잡 삭제하기

### 2. 권한 제공

[cronjob-proxy-server.yaml](../resources/cronjob-proxy-server.yaml)
에는 [RBAC](https://ko.wikipedia.org/wiki/%EC%97%AD%ED%95%A0_%EA%B8%B0%EB%B0%98_%EC%A0%91%EA%B7%BC_%EC%A0%9C%EC%96%B4)에 대한
설정이 있습니다. RBAC은 역할 기반 접근 제어로, 시스템 보안을 위한 주요한 방식입니다.
K8S에서는 내부 팟에서 악의적으로 K8S의 리소스를 변경하는 것을 방지하기 위해, RBAC을 통해 권한을 제어합니다.

K8S 클러스터 내 팟이 새로운 Job을 생성하기 위해서는, 그에 대한 권한을 할당받아야 합니다. 이를 수행하기 위한 간단한 방법으로서 `ServiceAccount`을 지정한 후, `ServiceAccount`에
Job에 관련된 권한을 binding하는 것입니다. 아래 코드에서는 `cronjob-creator`라는 ServiceAccount를 생성하고, CRUD권한을 바인딩을 시켰습니다.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cronjob-creator

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: cronjob-creator-role
rules:
  - apiGroups: [ "batch" ]
    resources: [ "cronjobs" ]
    verbs: [ "create", "get", "list", "watch", "delete", "update" ]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: job-creator-rolebinding
  namespace: default
subjects:
  - kind: ServiceAccount
    name: job-creator
    namespace: default
roleRef:
  kind: Role
  name: job-creator-role
  apiGroup: rbac.authorization.k8s.io
```

그리고 deployment 코드 내에는 `ServiceAccountName` 필드를 통해 지정하여, 우리의 서비스 팟이 Job을 생성할 수 있도록 권한을 제어했습니다.

````yaml
# job-simple-proxy-server.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cronjob-proxy-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cronjob-proxy-server
  template:
    metadata:
      labels:
        app: cronjob-proxy-server
    spec:
      serviceAccountName: cronjob-creator # <- serviceAccountName 지정
      containers:
        - name: cronjob-proxy-server
          image: craftsangjae/cronjob-proxy-server:0.0.1
          ports:
            - containerPort: 8000
````

## 실행

1. `proxy server` 생성하기

````shell
kubectl apply -f ./resources/job-simple-proxy-server.yaml
````

2. 포트바인딩을 통해 외부에서 접근가능하도록 하기

````shell
kubectl port-forward services/job-simple-proxy-server 8011:8001
````

3. swagger를 통해, API 호출해보기

* 주소 : http://localhost:8011/docs