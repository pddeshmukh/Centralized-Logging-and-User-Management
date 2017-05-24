#!/bin/bash
s="/var/log"
#d="/root/aaa"
BACKUPFILE=scripts.backup.`date +%F`.tar.gz
#scp -r root@$1:$s $2
rsync -chavzP --stats root@$1:$s $2


#filename=ug-$(date +%-Y%-m%-d)-$(date +%-T).tgz
tar -czvf $2/$BACKUPFILE $s
#tar --create --gzip --file=$d$filename $s
#rm -rf /root/aaa/log
#-chavzP



