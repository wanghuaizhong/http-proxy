#!/bin/bash


DATE_1=$(date +'%Y-%m-%d' -d"-1days")
DATE_2=$(date +'%Y-%m-%d' -d"-7days")
DATE_3=$(date +'%Y-%m-%d' -d"-15days")


SQL_1="update proxys set status = -2 where status = -1 and valid_times = 0 and invalid_times > 100 and created_at < '$DATE_1'"
SQL_2="update proxys set status = -2 where status = -1 and valid_times < 5 and invalid_times > 500 and last_valid_time < '$DATE_2'"
SQL_3="update proxys set status = -2 where status = -1 and last_valid_time < '$DATE_3'"

mysql -utest -p123456 proxy -e "$SQL_1"
mysql -utest -p123456 proxy -e "$SQL_2"
mysql -utest -p123456 proxy -e "$SQL_3"
