FROM --platform=linux/amd64 python:3.9

RUN mkdir /opt/fantacc
WORKDIR /opt/fantacc

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
VOLUME ["/opt/fantacc"] 
ENV FLASK_DEBUG=0
EXPOSE 5000
ENTRYPOINT ["/docker-entrypoint.sh"]