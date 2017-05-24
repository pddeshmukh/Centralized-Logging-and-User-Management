#!/bin/sh

ssh -X root@$1 usermod -c $2 -s $3 -m --home $4 $5 &> usermoderror.txt


