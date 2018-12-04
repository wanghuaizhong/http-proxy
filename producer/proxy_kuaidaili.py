# -*- coding: utf-8 -*-

"""
https://www.kuaidaili.com/ops/proxylist/1/
"""

import re
import requests
import logging
import time
import logging.handlers
from crawler import Crawler
from items import ProxyItem


class KuaiDaiLi(Crawler):

    def __init__(self):
        super(KuaiDaiLi, self).__init__()
        self.site = 6
        self.name = 'crawler_kuaidaili'

        self.pattern1 = re.compile(r'<td[^<]*>(\d+\.\d+\.\d+\.\d+)</td>\s*<td[^<]*>(\d+)</td>')
        self.url = [
            "https://www.kuaidaili.com/ops/proxylist/1/",
            "https://www.kuaidaili.com/ops/proxylist/2/",
            "https://www.kuaidaili.com/ops/proxylist/3/",
            "https://www.kuaidaili.com/ops/proxylist/4/",
            "https://www.kuaidaili.com/ops/proxylist/5/",
            "https://www.kuaidaili.com/ops/proxylist/6/",
            "https://www.kuaidaili.com/ops/proxylist/7/",
            "https://www.kuaidaili.com/ops/proxylist/8/",
            "https://www.kuaidaili.com/ops/proxylist/9/",
            "https://www.kuaidaili.com/ops/proxylist/10/",
        ]

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

        for curl in self.url:
            time.sleep(10)
            html = requests.get(curl, timeout=5, headers=theader).text
            ll = self.pattern1.findall(html)
            for l in ll:
                ip = l[0]
                port = l[1]
                proxy = ProxyItem(self.site, ip, port)
                self.write(proxy)

if __name__ == '__main__':
    crawler = KuaiDaiLi()
    crawler.crawl()
