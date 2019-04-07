#!/bin/sh
ssh -i /key/key -oStrictHostKeyChecking=no $1@127.0.0.1 'sudo bash -s' < $2