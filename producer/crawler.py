# -*- coding: utf-8 -*-

import redis
import logging


class Crawler(object):

    def __init__(self):
        self.name = 'base'
        self.redis_key = 'proxy:list'
        self.redis_host = '101.251.206.73'
        self.redis_port = 6379
        self.redis_conn = redis.Redis(host=self.redis_host, port=self.redis_port)

    def crawl(self, *args, **kwargs):
        pass

    def write(self, proxy):
        value = proxy.get_value()
        logging.info('proxy value:%s' % value)
        self.redis_conn.rpush(self.redis_key, value)
