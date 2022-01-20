FROM python:3.9.7-slim
WORKDIR /app
# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the  serve program is found when the container is invoked.
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/app:${PATH}"

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY main.py /app/
COPY scripts/start.sh /app/

EXPOSE 1337
CMD ./start.sh
