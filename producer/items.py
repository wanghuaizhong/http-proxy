# -*- coding: utf-8 -*-


class ProxyItem(object):

    def __init__(self, site, ip, port):
        self.site = site
        self.ip = ip
        self.port = port

    def get_value(self):
        return '%s|%s|%s' % (self.site, self.ip, self.port)