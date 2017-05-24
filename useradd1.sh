#!/bin/sh

ssh -X root@$1 useradd -c $2 -p $3 -s $4 -d $5 $6 &> error.txt
