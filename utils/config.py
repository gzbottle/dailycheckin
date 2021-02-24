# -*- coding: utf-8 -*-
import json
import os

from acfun import AcFunCheckIn
from baidu_url_submit import BaiduUrlSubmit
from bilibili import BiliBiliCheckIn
from cloud189 import Cloud189CheckIn
from fmapp import FMAPPCheckIn
from iqiyi import IQIYICheckIn
from kgqq import KGQQCheckIn
from liantong import LianTongCheckIn
from mimotion import MiMotion
from music163 import Music163CheckIn
from oneplusbbs import OnePlusBBSCheckIn
from pojie import PojieCheckIn
from samsung import SamsungCheckIn
from smzdm import SmzdmCheckIn
from tieba import TiebaCheckIn
from v2ex import V2exCheckIn
from vqq import VQQCheckIn
from weather import Weather
from wps import WPSCheckIn
from www2nzz import WWW2nzzCheckIn
from xmly import XMLYCheckIn
from youdao import YouDaoCheckIn

checkin_map = {
    "IQIYI_COOKIE_LIST": IQIYICheckIn,
    "VQQ_COOKIE_LIST": VQQCheckIn,
    "KGQQ_COOKIE_LIST": KGQQCheckIn,
    "MUSIC163_ACCOUNT_LIST": Music163CheckIn,
    "BILIBILI_COOKIE_LIST": BiliBiliCheckIn,
    "YOUDAO_COOKIE_LIST": YouDaoCheckIn,
    "FMAPP_ACCOUNT_LIST": FMAPPCheckIn,
    "BAIDU_URL_SUBMIT_LIST": BaiduUrlSubmit,
    "LIANTONG_ACCOUNT_LIST": LianTongCheckIn,
    "ONEPLUSBBS_COOKIE_LIST": OnePlusBBSCheckIn,
    "SMZDM_COOKIE_LIST": SmzdmCheckIn,
    "TIEBA_COOKIE_LIST": TiebaCheckIn,
    "V2EX_COOKIE_LIST": V2exCheckIn,
    "WWW2NZZ_COOKIE_LIST": WWW2nzzCheckIn,
    "ACFUN_ACCOUNT_LIST": AcFunCheckIn,
    "MIMOTION_ACCOUNT_LIST": MiMotion,
    "CLOUD189_ACCOUNT_LIST": Cloud189CheckIn,
    "SAMSUNG_COOKIE_LIST": SamsungCheckIn,
    "WPS_COOKIE_LIST": WPSCheckIn,
    "POJIE_COOKIE_LIST": PojieCheckIn,
    "CITY_NAME_LIST": Weather,
    "XMLY_COOKIE_LIST": XMLYCheckIn,
}


def env2json(key):
    try:
        value = json.loads(os.getenv(key, [])) if os.getenv(key) else []
        if isinstance(value, list):
            value = value
        else:
            value = []
    except Exception as e:
        print(e)
        value = []
    return value


def get_checkin_info(data):
    result = {}
    if isinstance(data, dict):
        for one in checkin_map.keys():
            result[one.lower()] = data.get(one, [])
    else:
        for one in checkin_map.keys():
            result[one.lower()] = env2json(one)
    return result
