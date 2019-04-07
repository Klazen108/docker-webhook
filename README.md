# docker-puller ![License MIT](https://go-shields.herokuapp.com/license-MIT-blue.png)

Listen for web hooks (i.e: from docker.io builds) and run a command after that.

Introduction
============

If you use docker.io (or any similar service) to build your Docker container, it may be possible that, once the new image is generated, you want your Docker host to automatically pull it and restart the container.

Docker.io gives you the possibility to set a web hook after a successful build. Basically it does a POST on a defined URL and send some informations in JSON format.

docker-puller listen to these web hooks and can be configured to run a particular script, given a specific hook.

Example web hook
================

In docker.io setup a web hook with an URL like this: https://myserver.com/dockerpuller?token=abc123&hook=server

Example configuration
===================================

    {
        "port": 8000,
        "token": "abc123",
        "hooks": ["server","website"]
    }

server.sh and website.sh should be present in the scripts directory.

Example docker restart script
=============================

This script updates the image, kills the existing container, and starts a replacement with any docker flags as needed.

```bash
#pull the latest
docker pull repo/image-name
#wipe out any existing instances
docker kill container-name
docker rm container-name
#start the new container
docker run -d --name=container-name repo/image-name
echo server started.
```

Example docker container launch
===============================
```bash
docker run -t -i --name webhook -p 8000:8000 \
 -v ~/scripts:/root/dockerpuller/scripts \
 -v ~/key:/key \
 -v ~/config.json:/root/config.json \
 klazen108/docker-webhook
```

Docker Volumes:
* /root/dockerpuller/scripts - place your docker continer rm/pull/restart scripts here
* /key/key - mount your private key here
* /root/config.json - mount your configuration script here