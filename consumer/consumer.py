# -*- coding: utf-8 -*-

import logging
import logging.handlers

import time
import redis

import sys
import os
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + "/../utils/")
import mysqlutil

redis_key = 'proxy:list'
redis_host = '101.251.206.73'
redis_port = 6379

redis_conn = redis.Redis(host=redis_host, port=redis_port)

logger = logging.getLogger()
hdlr = logging.handlers.RotatingFileHandler('/home/logs/proxy/consumer.log', maxBytes=1024*1024*10, backupCount=10)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def main():
    while 1 > 0:
        item = redis_conn.rpop(redis_key)
        if not item:
            logging.info('waiting...')
            time.sleep(20)
            continue

        logging.info('get proxy:[%s]' % item)
        item_values = item.split('|')

        sql = "select id,status from proxys where ip = '%s' and port = '%s' " % (item_values[1], item_values[2])
        results = mysqlutil.run_select_sql(sql)
        if not results:
            sql = "insert into proxys(ip, port,site, created_at) values ('%s', %s, %s, now())" % (item_values[1], item_values[2], item_values[0])
            mysqlutil.run_update_sql(sql)
        else:
            result = results[0]
            status = result['status']
            if status != 1:
                sql = "update proxys set status = 0,site=%s where ip = '%s' and port = '%s' " % (item_values[0], item_values[1], item_values[2])
                logging.info("update sql:%s" % sql)
                mysqlutil.run_update_sql(sql)


if __name__ == '__main__':
    main()