# http-proxy
处理http 代理抓取、自动检测、接口构建

## run_app.sh 
```
构建代理接口地址, e.g http://127.0.0.1:8888/proxy/2000 ; 2000 代表要提取的代理数量

修改interface/application.py 端口配置和数据库连接配置
define("port", default=8888, help="run port", type=int)  
define("mysql_host", default="127.0.0.1:3306", help="db host")
define("mysql_database", default="proxy", help="db name")
define("mysql_user", default="test", help="db user")
define("mysql_password", default="123456", help="db password")
```

## run_check.sh
检测代理是否可用

## update_proxy_status.sh
简单几种策略更新proxy状态

## run_consumer.sh
处理抓取的代理

## crawler (定时任务驱动)
```
30 */2 * * * cd /home/g/proxy/producer; python proxy_ajshw.py > /home/logs/proxy/ajshw.out 2>&1
35 */1 * * * cd /home/g/proxy/producer; python proxy_data5u.py > /home/logs/proxy/data5u.out 2>&1
39 */2 * * * cd /home/g/proxy/producer; python proxy_xici.py > /home/logs/proxy/xici.out 2>&1
40 */1 * * * cd /home/g/proxy/producer; python proxy_yaoyao.py > /home/logs/proxy/yaoyao.out 2>&1
15 */3 * * * cd /home/g/proxy/producer; python proxy_ip66.py > /home/logs/proxy/ip66.out 2>&1
30 */3 * * * cd /home/g/proxy/producer; python proxy_kuaidaili.py > /home/logs/proxy/kuaidaili.out 2>&1
10 */2 * * * cd /home/g/proxy/producer; python proxy_89ip.py > /home/logs/proxy/ip89.out 2>&1
00 12 * * * cd /home/g/proxy/producer; python proxy_xiaoshu.py > /home/logs/proxy/xiaoshu.out 2>&1
```
