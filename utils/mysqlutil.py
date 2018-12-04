# -*- coding: utf-8 -*-

import time
import logging
import MySQLdb.cursors

# mysql_host = '192.168.1.73'
mysql_host = '101.251.206.73'
mysql_port = 3306
mysql_user = 'stock'
mysql_pass = '360yahoo'
mysql_db = '91z'

mysql_conn = MySQLdb.connect(
            host=mysql_host,
            port=mysql_port,
            db=mysql_db,
            user=mysql_user,
            passwd=mysql_pass,
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            init_command='set names utf8',
)


def run_update_sql(sql):
    logging.info('[sql]:%s' % sql)
    cursor = mysql_conn.cursor()
    try:
        cursor.execute(sql)
        mysql_conn.commit()
    except Exception as e:
        logging.info(e)
    finally:
        cursor.close()


def re_connect (num=5, stime=1):
    global mysql_conn
    _number = 0
    _down = True
    while _down and _number <= num:
        try:
            mysql_conn.ping()
            _down = False
            break
        except:
            mysql_conn = MySQLdb.connect(
                host=mysql_host,
                port=mysql_port,
                db=mysql_db,
                user=mysql_user,
                passwd=mysql_pass,
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                init_command='set names utf8',
            )
            if mysql_conn:
                break
            _number += 1
            time.sleep(stime)


def run_select_sql(sql):
    logging.info('[sql]:%s' % sql)
    re_connect()
    cursor = mysql_conn.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        logging.info(e)
        return None
    finally:
        cursor.close()

