# Dockerfile

# Python 이미지 기반
FROM python:3.12

RUN apt-get update && apt-get install -y \
    vim

# 작업 디렉토리 설정
WORKDIR /app

COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

# 필요 라이브러리 복사
COPY requirements.txt requirements.txt

# 라이브러리 설치
RUN pip install --upgrade pip
RUN cat requirements.txt
RUN pip install -r requirements.txt

# 앱 소스 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 서버 실행
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ./start.sh
