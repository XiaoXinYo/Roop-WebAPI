FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y ffmpeg

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir

COPY . .

CMD ["gunicorn", "main:APP", "-c", "gunicorn.py"]