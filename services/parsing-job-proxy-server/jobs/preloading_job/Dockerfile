FROM python:3.11-slim as builder

WORKDIR /app

# Poetry 설치
RUN pip install poetry

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock* README.md /app/

# package 경로 생성 (pyproject.toml의 packages)
COPY proxy_manager/__init__.py /app/proxy_manager/__init__.py

# Poetry를 사용하여 의존성 설치
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

# 작성한 코드에 대한 패키지 추가
ADD proxy_manager/ /app/proxy_manager
ADD jobs/ /app/jobs

ENTRYPOINT ["python", "jobs/preloading_job/main.py"]