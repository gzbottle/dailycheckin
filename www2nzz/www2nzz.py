# -*- coding: utf-8 -*-
import json
import os
import re

import requests
import urllib3
from requests import utils

urllib3.disable_warnings()


class WWW2nzzCheckIn:
    def __init__(self, www2nzz_cookie_list):
        self.www2nzz_cookie_list = www2nzz_cookie_list

    @staticmethod
    def sign(session):
        response = session.get(url="http://www.2nzz.com/index.php", verify=False)
        formhash = re.findall(r'<input type="hidden" name="formhash" value="(.*?)"', response.text)[0]
        params = (
            ("id", "dsu_paulsign:sign"),
            ("operation", "qiandao"),
            ("infloat", "1"),
            ("sign_as", "1"),
            ("inajax", "1"),
        )
        data = {"formhash": formhash, "qdxq": "kx", "qdmode": "2", "todaysay": "", "fastreply": "0"}
        response = session.post(url="http://www.2nzz.com/plugin.php", params=params, data=data, verify=False)
        user_rep = session.get(url="http://www.2nzz.com/home.php")
        uid = re.findall(r"uid=(\d+)\"", user_rep.text)
        uid = uid[0] if uid else "未获取到 UID"
        if "您今天已经签到过了或者签到时间还未开始" in response.text:
            msg = f"用户信息: {uid}\n签到信息: 您今天已经签到过了或者签到时间还未开始"
        else:
            check_msg = re.findall(r"<div class=\"c\">(.*?)</div>", response.text, re.S)
            check_msg = check_msg[0].strip() if check_msg else "签到失败"
            msg = f"用户信息: {uid}\n签到信息: {check_msg}"
        return msg

    def main(self):
        msg_list = []
        for www2nzz_cookie in self.www2nzz_cookie_list:
            www2nzz_cookie = {
                item.split("=")[0]: item.split("=")[1] for item in www2nzz_cookie.get("www2nzz_cookie").split("; ")
            }
            session = requests.session()
            requests.utils.add_dict_to_cookiejar(session.cookies, www2nzz_cookie)
            session.headers.update(
                {
                    "Origin": "http://www.2nzz.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Referer": "http://www.2nzz.com/index.php",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                }
            )
            sign_msg = self.sign(session=session)
            msg = f"【咔叽网单】\n{sign_msg}"
            msg_list.append(msg)
        return msg_list


if __name__ == "__main__":
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/config.json"), "r", encoding="utf-8"
    ) as f:
        datas = json.loads(f.read())
    _www2nzz_cookie_list = datas.get("WWW2NZZ_COOKIE_LIST", [])
    WWW2nzzCheckIn(www2nzz_cookie_list=_www2nzz_cookie_list).main()
