# docker-puller ![License MIT](https://go-shields.herokuapp.com/license-MIT-blue.png)

**Docker Puller** is your solution for in-place docker CI/CD.

Docker Puller complements a single-server container deployment. Traditional CI/CD workflows may involve a separate, standalone build and deploy utility such as Jenkins, but a Jenkins instance can be overkill when all you need is to fetch an updated image and restart a container. With Docker Puller, you can instruct a separate Continuous Integration pipeline (suck as GitHub + Docker.io) to trigger a container redeploy via a webhook.

Docker Puller lives alongside your deployed containers and, using SSH, directs your host docker instance to fetch and redeploy any images when a webhook is triggered - such as after a build has completed!

SSH Setup
=========

You will need to generate a public/private keypair to allow the container to ssh to the host in order to perform commands.

* Create a new user (with sudo rights if necessary)
* Create a keypair:

```ssh-keygen -t ecdsa -b 521```

* Install the public key in your new user's .ssh/authorized_keys
* Mount the private key in the container (see example docker container launch below)

Read more: https://www.ssh.com/ssh/keygen/

Example web hook
================

In docker.io, setup a web hook with an URL like this: https://myserver.com:8000/dockerpuller?token=abc123&hook=server

The token should be the same as in your configuration, and the hook indicates which script Docker Puller should execute. In this case, `server.sh` would be invoked (make sure to whitelist the hook in the configuration as well).

Example configuration
===================================

    {
        "port": 8000,
        "token": "abc123",
        "hooks": ["server","website"],
        "host_user": "user"
    }
    
* port - the port to listen on
* token - the token your webhook will post with (from the URL above)
* hooks - whitelist of hooks
* host_user - the user to ssh into the host with

`server.sh` and `website.sh` should be present in the scripts directory - these scripts will then be available for execution via the webhook.

Example docker restart script
=============================

This example script updates the image, kills the existing container, and starts a replacement with any docker flags as needed. This script will be run on the host via SSH - so you have access to the parent docker environment.

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

Here is how to start a docker-webhook container. Note that you must use `--net=host` because the script will attempt to ssh to the host system at 127.0.0.1.

```bash
docker run -t -i --name webhook --net=host \
 -v ~/scripts:/root/dockerpuller/scripts \
 -v ~/key:/key \
 -v ~/config.json:/root/config.json \
 klazen108/docker-webhook
```

Docker Volumes:
* /root/dockerpuller/scripts - place your docker container rm/pull/restart scripts here
* /key/key - mount your private key here
* /root/config.json - mount your configuration script here
