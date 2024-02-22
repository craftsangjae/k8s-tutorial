# parsing_job

## 목적

raw 데이터 스토리지에서 데이터를 읽어서, 데이터를 파싱하는 작업을 거친 후, parquet 형태로 변환하여 prep 데이터 스토리지에 적재하는 로직

## 실행 방식

````shell
# parsing-job-proxy-server에서 실행
python jobs/parsing_job/main.py < TICKER > < start_date_str > < end_date_str > < save_path >
````