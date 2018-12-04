# -*- coding: utf-8 -*-

"""
http://www.data5u.com/
"""

import re
import requests
import logging
import logging.handlers
from crawler import Crawler
from items import ProxyItem


class Data5UCrawler(Crawler):

    def __init__(self):
        super(Data5UCrawler, self).__init__()
        self.site = 1
        self.name = 'crawler_data5u'
        self.url = "http://www.data5u.com/"
        self.coder = {'A':'0', 'B':'1', 'C':'2', 'D':'3', 'E':'4', 'F':'5', 'G':'6', 'H':'7', 'I':'8', 'Z':'9'}
        self.pattern1 = re.compile(r'(\d+\.\d+\.\d+\.\d+)</li></span>\s*<span[^>]*><li class="port\s*([A-Z]*)">')

        logger = logging.getLogger()
        hdlr = logging.handlers.RotatingFileHandler('/home/logs/proxy/%s.log' % (self.name), maxBytes=1024 * 1024 * 10,
                                                    backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)

    def _get_port(self, port_str):
        ret = []
        for cha in port_str:
            ret.append(self.coder.get(cha))
        number = int(''.join(ret))
        return number / 8

    def crawl(self, *args, **kwargs):
        theader = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate',
        }

        html = requests.get(self.url, timeout=5, headers=theader).text
        ll = self.pattern1.findall(html)
        for l in ll:
            ip = l[0]
            port_str = l[1]
            port = self._get_port(port_str)
            proxy = ProxyItem(self.site, ip, port)
            self.write(proxy)

if __name__ == '__main__':
    crawler = Data5UCrawler()
    crawler.crawl()