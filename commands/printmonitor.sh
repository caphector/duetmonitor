#!/bin/sh
#
# Print Logger - logs print jobs on a minute by minute basis
#

config=~/.duet
. $config

while true
do
	log=mylog.$$

	date=$(date)
	gstatus=$(statusparser)
	pdate=$(date)
	wget --quiet http://localhost:8080/?action=snapshot -O pics/$(echo $pdate | tr ' ' -).jpg
	status=$(curl -s http://$ip/rr_status?type=3)

	echo $date
	echo $gstatus

	echo $date >> $log

	echo $status >> $log
	echo $gstatus >> $log

	sleep 60
done
