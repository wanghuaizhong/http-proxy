# -*- coding: utf-8 -*-

"""
http://www.httpsdaili.com/?page=1
"""

import re
import requests
import logging
import logging.handlers
from crawler import Crawler
from items import ProxyItem


class YaoYaoCrawler(Crawler):

    def __init__(self):
        super(YaoYaoCrawler, self).__init__()
        self.site = 2
        self.name = 'crawler_yaoyao'
        self.url = "http://www.httpsdaili.com/?page="
        self.pattern1 = re.compile(r'<td[^>]*>(\d+\.\d+\.\d+\.\d+)</td>\s*<td[^>]*>(\d+)</td>')

        logger = logging.getLogger()
        hdlr = logging.handlers.RotatingFileHandler('/home/logs/proxy/%s.log' % (self.name), maxBytes=1024 * 1024 * 10,
                                                    backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)

    def crawl(self, *args, **kwargs):
        for page in range(1, 20):
            html = requests.get(self.url + str(page), timeout=5).text
            ll = self.pattern1.findall(html)
            for l in ll:
                ip = l[0]
                port = l[1]
                proxy = ProxyItem(self.site, ip, port)
                self.write(proxy)

if __name__ == '__main__':
    crawler = YaoYaoCrawler()
    crawler.crawl()