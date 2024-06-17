FROM --platform=linux/amd64 python:3.9

RUN mkdir /opt/fantacc
WORKDIR /opt/fantacc

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ADD . /opt/fantacc  
ENV FLASK_DEBUG=0
EXPOSE 5000
CMD ["python3","-m","flask","--app","/opt/fantacc/app.py","run","--host=0.0.0.0"]