# MinIO를 통한 object Storage 구축

## 목적

S3 API와 호환되는 Object Storage 구축하는 작업 수행. 클러스터 내 단일 노드에 설치하고, 해당 노드의 volume에 마운트해서 동작시키도록 설계하였음
(standalone Object Storage)

## 환경구성

#### 1. username / password 세팅

minio console UI에 사용할 username와 password를 생성합니다.

````shell
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: minio-config
data:
  MINIO_ROOT_USER: <username> # minio console UI의 username
  MINIO_ROOT_PASSWORD: <password> # minio console UI의 password 
````

#### 2. minio 컨테이너가 올라갈 node 지정하기

K8S 클러스터 내 노드를 지정합니다.

````shell
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minio-deployment
  ...
    spec:
      nodeSelector:
        kubernetes.io/hostname: <노드 이름> # <- minio 컨테이너가 운영될 노드 지정 
````

#### 3. minio를 k8s에 배포하기

````shell
kubectl apply -f resources/standalone_minio.yaml
````

#### 4. 포트포워딩 진행

테스트를 위해, 외부 호스트에서 접근할 수 있도록 포트포워딩을 엽니다.

* 9000 : minio main port로 해당 포트를 통해 통신 진행
* 9001 : minio console port로 minIO console 화면으로 접근

````shell
kubectl port-forward service/minio 9000 9001
````

## 동작확인

#### 1. 로그인하기

위에서 설정한 super user 계정으로 들어갑니다.

![minio_login.png](../images/minio_login.png)

#### 2. minio access key 생성하기

`create access key`를 통해, access key와 secret key를 발번합니다.

![](../images/minio%20Access%20Key.png)

#### 3. minio에 데이터를 올리고 제거하는 로직 구현하기

````shell
import boto3

ACCESS_KEY = <발번받은 access key>
SECRET_KEY = <발번받은 secret key>

# LocalStack S3 서비스의 엔드포인트 설정
s3_endpoint_url = 'http://localhost:9000' 

# Boto3 클라이언트 설정
s3 = boto3.resource('s3', 
                    endpoint_url=s3_endpoint_url,
                    aws_access_key_id=ACCESS_KEY, 
                    aws_secret_access_key=SECRET_KEY)

#### 버킷 생성하기
bucket = s3.create_bucket(
    ACL="private",
    Bucket="hello"
)
print("버킷 : ", bucket)

# 오브젝트 생성
with open("./example.txt", 'w') as f:
    f.write("hello")
    
bucket.upload_file(Filename="example.txt", Key="data/example.txt")    

# 오브젝트 조회 및 삭제
for obj in bucket.objects.all():
    print("오브젝트 : ", obj.key)
    obj.delete()


# 버킷 삭제하기
bucket = s3.Bucket(name="hello")
bucket.delete()
````