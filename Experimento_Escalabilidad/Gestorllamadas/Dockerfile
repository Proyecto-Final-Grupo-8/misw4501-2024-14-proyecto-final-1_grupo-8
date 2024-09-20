FROM alpine:3.14   

RUN apk add py3-pip\
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/

RUN pip install install -r requirements.txt

EXPOSE 5000 

CMD ["python3", "app.py"]