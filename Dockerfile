FROM python:3.6
ADD dockerpuller /root/dockerpuller
ADD requirements.txt /root/requirements.txt
WORKDIR /root/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install openssh-client
RUN chmod +x /root/dockerpuller/execute_remote.sh
WORKDIR /root/dockerpuller
ENTRYPOINT ["python", "app.py"]
