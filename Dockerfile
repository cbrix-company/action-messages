# Container image that runs your code
FROM python:3.8-alpine3.13

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt --no-cache-dir && chmod +x entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
