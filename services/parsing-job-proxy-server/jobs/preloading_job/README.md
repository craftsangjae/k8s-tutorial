# preloading_job

## 목적

raw 데이터 스토리지에서 원 데이터를 적재 수행. 현재는 Raw 데이터로 yfinance로부터 주가 정보를 받아오도록 설계되어 있음

## 실행 방식

````shell
# parsing-job-proxy-server에서 실행
python jobs/preloading_job/main.py < TICKER > < start_date_str > < end_date_str >
````