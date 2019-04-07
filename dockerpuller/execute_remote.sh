#!/bin/sh
ssh -i /key/key -oStrictHostKeyChecking=no $1@127.0.0.1 'sudo bash -s' < $2

#sudo docker run -ti --net=host --rm -v /home/core/webhook/keys:/keys ubuntu /bin/bash
#apt-get update && apt-get install openssh-client
#echo "echo hello" > test.sh
#ssh -i /keys/temp webhook@127.0.0.1 < test.sh
#exit + ctrl+d to quit