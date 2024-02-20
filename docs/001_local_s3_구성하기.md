# Local S3 구성하기

## 목표

1. On-Premise 내 Object Storage가 있는 상황 재현을 위해, 유사한 도구인 localstack을 활용해서, on-premise s3을 구축합니다.
2. k8s에서 해당 팟에 호출이 가능한지 확인하기 위해, 포트포워딩을 통해 호출 테스트를 수행합니다.

## 셋업 과정

### 1. `local-s3.yaml` 작성

localstack은 AWS을 내부에서 테스트할 수 있도록 Local 환경용으로 구현한 솔루션입니다.
빠르게 AWS 환경을 재현해볼 수 있다는 것이 큰 장점입니다.
localstack 이미지를 가져온 후, `SERVICES` 환경변수에 s3로 지정하여 생성합니다.
yaml에는 (1) Deployment와 (2) Service로 구성되어 있고, Localstack의 Service는 ClusterIp로 지정했습니다.
Port는 4566으로 지정되어 있습니다.

````shell
kubectl apply -f resources/local-s3.yaml
````

## 테스트 수행

### 1. 외부에서 접근하기 위해, 포트포워딩 수행하기

minikube의 클러스터는 독립적인 네트워크를 가집니다.
클러스터 내의 **Port**와 호스트 컴퓨터(로컬 컴퓨터)의 **Port**를 연결시켜 주어야 합니다.
이를 이어주기 위해서는 포트포워딩을 수행해야 합니다.

````shell
# 4566을 31500으로 포워딩하기
# kubectl port-forward <resource name> <host port>:<pod port>
kubectl port-forward service/localstack-s3-service 31500:4566
````

### 2. 버킷 만들기 호출

호스트 컴퓨터에서 boto3를 통해 올바르게 버킷이 생성, 조회, 삭제 되는지를 확인합니다.
아래코드를 실행시키면, 정상적으로 버킷이 생성 / 조회 / 삭제가 되는지를 확인해볼수 있습니다.

````python
import boto3

# LocalStack S3 서비스의 엔드포인트 설정
S3_ENDPOINT_URL = 'http://localhost:31500'

AWS_ACCESS_KEY_ID = "test"  # localstack에서는 임의의 값을 넣으면 됨.
AWS_SECRET_ACCESS_KEY = "test"  # localstack에서는 임의의 값을 넣으면 됨.
RESION_NAME = 'ap-northeast-2'

# Boto3 클라이언트 설정
s3_client = boto3.client('s3',
                         endpoint_url=S3_ENDPOINT_URL,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=RESION_NAME)

#####
# 호출 테스트
#####

# 버킷 생성
response = s3_client.create_bucket(
    ACL="private",
    Bucket="hello",
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-northeast-2'
    }
)
if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("(1) 버킷 생성 : `hello` 버킷 생성")

# 버킷 조회
print("(2) 버킷 목록 조회")
buckets = s3_client.list_buckets()

for bucket in buckets['Buckets']:
    print(" - 버킷 이름 : ", bucket['Name'])

# 버킷 삭제
response = s3_client.delete_bucket(Bucket='hello')
print("(3) 버킷 삭제 완료")
````

