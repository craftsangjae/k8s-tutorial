FROM python:3.11-slim as builder

WORKDIR /app

# Poetry 설치
RUN pip install poetry

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock* /app/

# Poetry를 사용하여 의존성 설치. 시스템 라이브러리를 제외하고 Python 패키지만 /app/vendor에 설치합니다.
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

ADD proxy_server/ /app/proxy_server

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "proxy_server.app:app", "--host", "0.0.0.0", "--port", "8000"]