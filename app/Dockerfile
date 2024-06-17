FROM --platform=linux/amd64 ubuntu/bind9

RUN mkdir /opt/fantacc
WORKDIR /opt/fantacc

RUN apt update && apt install python3-flask -y

COPY app/ .
ENV FLASK_DEBUG=0
EXPOSE 5000
CMD ["python3","-m","flask","--app","/opt/fantacc/app","run","--host=0.0.0.0"]