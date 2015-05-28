#!/bin/bash

CN=10

case "$1" in
    start)
	for i in `seq -w 1 ${CN}`; do
          echo "docker run -d -p 100${i}:8080 --name stu${i} java-testing"
        done
	;;
    stop)
        for i in `seq -w 1 ${CN}`; do
          echo "docker stop stu${i}"
          echo "docker rm stu${i}"
        done
        ;;
    *)
	echo $1
	echo "Usage: setup.sh {start|stop}"
	exit 2
esac
