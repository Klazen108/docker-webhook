FROM python:3.6
ADD dockerpuller /root/dockerpuller
ADD requirements.txt /root/requirements.txt
WORKDIR /root/
RUN pip install -r requirements.txt
RUN apk update && apk add --no-cache docker
WORKDIR /root/dockerpuller
ENTRYPOINT ["python", "app.py"]
