# -*- coding: utf-8 -*-

"""
http://www.66ip.cn
"""

import re
import time
import requests
import logging
import logging.handlers
from crawler import Crawler
from items import ProxyItem


class Ip66Crawler(Crawler):

    def __init__(self):
        super(Ip66Crawler, self).__init__()
        self.site = 5
        self.name = 'crawler_ip66'
        self.pattern1 = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)')
        self.url = "http://www.66ip.cn/nmtq.php?getnum=1000&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip"

        self.pattern2 = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>')
        self.url2 = [
            "http://www.66ip.cn/",
            "http://www.66ip.cn/2.html",
            "http://www.66ip.cn/3.html",
            "http://www.66ip.cn/4.html",
            "http://www.66ip.cn/5.html",
            "http://www.66ip.cn/areaindex_1/1.html",
            "http://www.66ip.cn/areaindex_2/1.html",
            "http://www.66ip.cn/areaindex_3/1.html",
            "http://www.66ip.cn/areaindex_4/1.html",
            "http://www.66ip.cn/areaindex_5/1.html",
            "http://www.66ip.cn/areaindex_6/1.html",
            "http://www.66ip.cn/areaindex_7/1.html",
            "http://www.66ip.cn/areaindex_8/1.html",
            "http://www.66ip.cn/areaindex_9/1.html",
            "http://www.66ip.cn/areaindex_10/1.html",
            "http://www.66ip.cn/areaindex_11/1.html",
            "http://www.66ip.cn/areaindex_12/1.html",
            "http://www.66ip.cn/areaindex_13/1.html",
            "http://www.66ip.cn/areaindex_14/1.html",
            "http://www.66ip.cn/areaindex_15/1.html",
            "http://www.66ip.cn/areaindex_16/1.html",
            "http://www.66ip.cn/areaindex_17/1.html",
            "http://www.66ip.cn/areaindex_18/1.html",
            "http://www.66ip.cn/areaindex_19/1.html",
            "http://www.66ip.cn/areaindex_20/1.html",
            "http://www.66ip.cn/areaindex_21/1.html",
            "http://www.66ip.cn/areaindex_22/1.html",
            "http://www.66ip.cn/areaindex_23/1.html",
            "http://www.66ip.cn/areaindex_24/1.html",
            "http://www.66ip.cn/areaindex_25/1.html",
            "http://www.66ip.cn/areaindex_26/1.html",
            "http://www.66ip.cn/areaindex_27/1.html",
            "http://www.66ip.cn/areaindex_28/1.html",
            "http://www.66ip.cn/areaindex_29/1.html",
            "http://www.66ip.cn/areaindex_30/1.html",
            "http://www.66ip.cn/areaindex_31/1.html",
            "http://www.66ip.cn/areaindex_32/1.html",
            "http://www.66ip.cn/areaindex_33/1.html",
            "http://www.66ip.cn/areaindex_34/1.html",
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

        html = requests.get(self.url, timeout=5, headers=theader).text
        ll = self.pattern1.findall(html)
        for l in ll:
            ip = l[0]
            port = l[1]
            proxy = ProxyItem(self.site, ip, port)
            self.write(proxy)

        for curl in self.url2:
            time.sleep(10)
            html = requests.get(curl, timeout=5, headers=theader).text
            ll = self.pattern2.findall(html)
            for l in ll:
                ip = l[0]
                port = l[1]
                proxy = ProxyItem(self.site, ip, port)
                self.write(proxy)


if __name__ == '__main__':
    crawler = Ip66Crawler()
    crawler.crawl()
