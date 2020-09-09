# -*- coding: utf-8 -*-
# @Author: wujiyu
# @Date:   2017-02-26 22:49:03
# @Last Modified by:   wujiyu
# @Last Modified time: 2017-03-27 12:25:07
import requests
import logging
# requests.packages.urllib3.disable_warnings()

import datetime
import time
import os
import traceback

from util.configutil import ConfigUtil
from util.mylog import install_log, info, critical
from util.cookie_util import has_cookies
from util.date_util import DateUtil
from util.utils import clear_output

import schedule
from src.meican import MeiCan
from src.errcode import desc as Desc

import sys


reload(sys)
sys.setdefaultencoding('utf8')


def order(meican):
    try:
        order_week = ConfigUtil.instance().order_week
        cur_week = str(DateUtil.curr_week())
        if cur_week not in order_week:
            critical("meican | order week not in config!!!!!!!!!!!!, cur_week:<%s>"%cur_week)
            return
        info("meican |begin order")
        meican.order()
    except Exception as e:
        info(traceback.format_exc())

def do_job():
    try:
        info("I'm working on : <%s>"%datetime.datetime.now())
    except Exception as e:
        info(traceback.format_exc())

if __name__ == '__main__':
    install_log()
    info("start meican robot")

    meican = None
    login_ok = False
    if has_cookies():
        meican = MeiCan('','')
        login_ok = meican.login()
    else:
        while not login_ok:
            username = raw_input('[ Enter meican email ]:')
            password = raw_input('[ Enter meican password ]:')
            meican = MeiCan(username,password)
            login_ok = meican.login()
        clear_output()

    schedule.every(1).day.at("06:20").do(order, meican)
    schedule.every(1).day.at("06:40").do(order, meican)
    schedule.every(1).day.at("07:20").do(order, meican)
    schedule.every(1).day.at("07:40").do(order, meican)
    schedule.every(1).day.at("12:20").do(order, meican)
    schedule.every(1).day.at("13:20").do(order, meican)
    schedule.every(1).day.at("14:20").do(order, meican)
    schedule.every(1).day.at("15:20").do(order, meican)
    schedule.every(1).day.at("16:20").do(order, meican)
    schedule.every(1).day.at("16:50").do(order, meican)
    info("meican | next order time: | [[%s]]"%schedule.next_run())

    # meican.order()

    # schedule.every(1).hour.do(do_job)
    while True:
        schedule.run_pending()
        time.sleep(1)
