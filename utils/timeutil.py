#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
时间处理通用类
"""

from datetime import datetime, timedelta

def getDiffTime(diff_hours=-12):
    today = datetime.today()
    return today + timedelta(hours=diff_hours)









