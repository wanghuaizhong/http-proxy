# -*- coding: utf-8 -*-

import logging
import logging.handlers

import requests
import time
import re

import sys
import os

sys.path.append(os.path.split(os.path.realpath(__file__))[0] + "/../utils/")
import mysqlutil
import timeutil

total_processes = int(sys.argv[1])
cur_processno = int(sys.argv[2])

pattern = re.compile(r'百度一下，你就知道')

theader = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate',
}

logger = logging.getLogger()
hdlr = logging.handlers.RotatingFileHandler('/home/logs/proxy/check_%s.log' % cur_processno, maxBytes=1024*1024*10, backupCount=10)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def deal_invalid(pid):
    sql = 'update proxys set invalid_times = invalid_times + 1, status = -1, last_check_time = now() ' \
          'where id = %s' % (pid)
    mysqlutil.run_update_sql(sql)


def deal_valid(pid):
    sql = 'update proxys set valid_times = valid_times + 1, status = 1, last_check_time = now(), last_valid_time = now() ' \
          'where id = %s' % (pid)
    mysqlutil.run_update_sql(sql)


def is_proxy_usable(ip, port):
    proxy = {'http': 'http://%s:%s' % (ip, port)}
    try:
        content = requests.get("http://www.baidu.com", proxies=proxy, headers=theader, timeout=3)
        if content:
            if re.search(pattern, content.text.encode('utf-8')):
                return True
            else:
                return False
        else:
            return False
    except:
        return False


"""
从proxys中遍历proxy进行校验
"""
def main():
    index = 0
    sleep_time = 1800
    turn_count = 10000

    while 1 > 0:
        sql = 'select id, ip, port, status, last_check_time from proxys where id > %s and status > -2 limit %s' % (index, turn_count)
        results = mysqlutil.run_select_sql(sql)
        if results:
            index = index + turn_count
            for ret in results:
                ip = ret['ip']
                port = ret['port']
                pid = int(ret['id'])
                status = int(ret['status'])
                last_check_time = ret['last_check_time']
                index = pid if pid > index else index
                if pid % total_processes == cur_processno:
                    if status == 1 and timeutil.getDiffTime() < last_check_time :
                        continue

                    is_ok = is_proxy_usable(ip, port)
                    if is_ok:
                        deal_valid(ret['id'])
                    else:
                        deal_invalid(ret['id'])
        else:
            index = 0
            time.sleep(sleep_time)


if __name__ == '__main__':
    main()




