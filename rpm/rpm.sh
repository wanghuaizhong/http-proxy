#!/bin/bash

/usr/bin/fpm -s dir -t rpm -n cproxy -v 0.0.1 -f -C /home/wzhiju/workspace/  proxy/producer proxy/utils  proxy/check  proxy/consumer  proxy/interface  proxy/run_check.sh  proxy/run_consumer.sh 
