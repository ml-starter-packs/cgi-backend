FROM python:3.9.7-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY main.py /app/
COPY scripts/start.sh /app/

EXPOSE 1337
CMD ./start.sh
