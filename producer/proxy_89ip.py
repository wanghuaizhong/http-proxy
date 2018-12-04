# -*- coding: utf-8 -*-

"""
http://www.66ip.cn
"""

import re
import requests
import logging
import logging.handlers
from crawler import Crawler
from items import ProxyItem


class Ip89Crawler(Crawler):

    def __init__(self):
        super(Ip89Crawler, self).__init__()
        self.site = 5
        self.name = 'crawler_89ip'
        self.pattern1 = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)')
        self.url = "http://www.89ip.cn/tqdl.html?num=1000&address=&kill_address=&port=&kill_port=&isp="

        logger = logging.getLogger()
        hdlr = logging.handlers.RotatingFileHandler('/home/logs/proxy/%s.log' % (self.name),
                                                    maxBytes=1024 * 1024 * 10,
                                                    backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)

    def crawl(self, *args, **kwargs):
        theader = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
        }

        html = requests.get(self.url, timeout=5, headers=theader).text
        ll = self.pattern1.findall(html)
        for l in ll:
            ip = l[0]
            port = l[1]
            proxy = ProxyItem(self.site, ip, port)
            self.write(proxy)

if __name__ == '__main__':
    crawler = Ip89Crawler()
    crawler.crawl()
