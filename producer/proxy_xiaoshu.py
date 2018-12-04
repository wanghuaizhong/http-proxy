# -*- coding: utf-8 -*-

"""
http://www.xsdaili.com/
"""

import re
import requests
import logging
import logging.handlers
from crawler import Crawler
from items import ProxyItem


class XiaoShuCrawler(Crawler):

    def __init__(self):
        super(XiaoShuCrawler, self).__init__()
        self.site = 7
        self.name = 'crawler_xiaoshu'
        self.base_url = 'http://www.xsdaili.com'
        self.base_pattern = re.compile(r'<a href="(/dayProxy/ip/\d+.html)">')
        self.proxy_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)')
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

        url_map = {}
        html = requests.get(self.base_url, timeout=5, headers=theader).text
        ll = self.base_pattern.findall(html)
        for l in ll:
            url_map[l] = 1

        for k,v in url_map.items():
            proxy_url = self.base_url + k
            proxy_html = requests.get(proxy_url, timeout=5, headers=theader).text
            matchers = self.proxy_pattern.findall(proxy_html)
            for proxy in matchers:
                print proxy
                ip = proxy[0]
                port = proxy[1]
                proxy = ProxyItem(self.site, ip, port)
                self.write(proxy)


if __name__ == '__main__':
    crawler = XiaoShuCrawler()
    crawler.crawl()
