FROM --platform=linux/amd64 python:3.9

RUN mkdir /opt/fantacc
WORKDIR /opt/fantacc

COPY * .
RUN pip install requirements.txt
ENV FLASK_DEBUG=0
EXPOSE 5000
CMD ["python3","-m","flask","--app","/opt/fantacc/app","run","--host=0.0.0.0"]