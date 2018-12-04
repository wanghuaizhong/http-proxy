#!/bin/bash

nohup python check/check.py 10 0 > /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 1 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 2 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 3 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 4 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 5 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 6 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 7 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 8 >> /home/logs/proxy/check.out 2>&1 &
nohup python check/check.py 10 9 >> /home/logs/proxy/check.out 2>&1 &
