# Docker Private Registry 구성

## 1. htpasswd

### 1.1. 도커 파일 빌드

```bash
docker build -t htpasswd -f htpasswd.Dockerfile .
```

### 1.2. htpasswd 생성

````shell
 docker run --rm -ti htpasswd <username> <password> > ./auth/htpasswd
````

## 2. SSL 인증서 생성하기

### 2.1. 개인키 생성

````shell
openssl genrsa -out ./certs/domain.key 2048
````

### 2.1. crt 파일 생성

````shell
openssl req -new -x509 -key ./certs/domain.key -out ./certs/domain.crt -days 3650 -subj "/C=KR/ST=seoul/L=seoul/O=publicai/OU=dev/CN=publicai.com"
````