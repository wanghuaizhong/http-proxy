# -*- coding: utf-8 -*-

"""
http://www.ajshw.net/news/?list_9.html
"""

import re
import requests
import logging
import logging.handlers
from crawler import Crawler
from items import ProxyItem


class AjshwCrawler(Crawler):

    def __init__(self):
        super(AjshwCrawler, self).__init__()
        self.site = 0
        self.name = 'crawler_ajshw'
        self.host = "http://www.ajshw.net/"
        self.url = "http://www.ajshw.net/news/?list_9.html"
        self.pattern1 = re.compile(r"<a href='([^>]*?\d+/\d+.html)'[^>]*?>")
        self.pattern2 = re.compile(r"(\d+\.\d+\.\d+\.\d+):\d*<a[^>]*data-cfemail=\"(.*?)\".")
        self.pattern3 = re.compile(r'(\d+)@HTTP')
        self.pattern4 = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)')

        logger = logging.getLogger()
        hdlr = logging.handlers.RotatingFileHandler('/home/logs/proxy/%s.log' % (self.name), maxBytes=1024 * 1024 * 10, backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)


    def _get_port(self, portstr):
        ret = []
        length = len(portstr)
        base = int(portstr[0:2], 16)
        index = 2
        while index < (length - 1):
            number = int(portstr[index:(index + 2)], 16)
            number = number ^ base
            index += 2
            ret.append(str(chr(number)))
        decode_port = ''.join(ret)
        port = re.search(self.pattern3, decode_port)
        if not port:
            logging.info('portstr:%s' % portstr)
            return None
        return port.group(1)

    def crawl(self, *args, **kwargs):

        theader = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
        }

        html = requests.get(self.url, timeout=5, headers=theader).text
        ll = self.pattern1.findall(html)
        for l in ll:
            detail_url = l
            detail_html = requests.get(self.host + detail_url[2:], timeout=10, headers=theader).text
            if detail_html:
                ips = self.pattern2.findall(detail_html)
                if len(ips) == 0:
                    ips = self.pattern4.findall(detail_html)
                for proxy in ips:
                    ip = proxy[0]
                    port = proxy[1]
                    if not str(port).isdigit() or len(port) > 5:
                        port = self._get_port(port)
                    if port:
                        proxy = ProxyItem(self.site, ip, port)
                        self.write(proxy)

if __name__ == '__main__':
    crawler = AjshwCrawler()
    crawler.crawl()