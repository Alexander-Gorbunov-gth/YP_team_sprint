FROM python:3.12
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN apt update && apt install -y netcat-openbsd

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

CMD ["/wait-for.sh", "rabbitmq:5672", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8060"]
