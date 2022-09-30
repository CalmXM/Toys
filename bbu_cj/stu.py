import execjs
import hashlib
import requests
import base64
import re
import os
import json


def MD5_HEX(str):
    m = hashlib.md5()
    m.update(str.encode("utf-8"))
    return m.hexdigest()


def get_js():
    f = open("./des.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


class BBU:

    def __init__(self, username, password, config_path) -> None:
        self.__session__ = requests.session()
        self.__username__ = username
        self.__password__ = password
        self.__config_path__ = config_path

    def login(self):
        with open(self.__config_path__, "r", encoding="utf-8") as f:
            config = json.load(f)

        login_url = config["login_url"]
        logon_url = config["logon_url"]
        enc_url = config["enc_url"]
        cj_url = config["cj_url"]
        login_header = config["login_header"]
        enc_header = config["enc_header"]
        logon_header = config["logon_header"]
        cj_header = config["cj_header"]

        # 获取必要参数
        _sessionid = self.__session__.get(login_url, headers=login_header).cookies.get("JSESSIONID")
        username = self.__username__
        password = self.__password__
        txt_mm_expression = '13'
        txt_mm_length = str(len(password))
        txt_mm_userzh = '0'

        # params的第一次加密
        password = MD5_HEX(MD5_HEX(password)+MD5_HEX(""))
        username = username + ';;' + _sessionid
        username = str(base64.b64encode(username.encode("utf-8")), "utf-8")
        p_username = "_u"
        p_password = "_p"
        params = p_username+"="+username+"&"+p_password+"="+password+"&randnumber="+"&isPasswordPolicy=1" + "&txt_mm_expression="+txt_mm_expression+"&txt_mm_length="+txt_mm_length+"&txt_mm_userzh="+txt_mm_userzh+"&hid_flag=1"+"&hidlag=1"

        # params的第二次加密
        rep = self.__session__.get(enc_url, headers=enc_header)
        text = rep.text
        _deskey = re.search(r"var _deskey = '(.*?)';", text)
        _nowtime = re.search(r"var _nowtime = '(.*?)';", text)
        token = MD5_HEX(MD5_HEX(params) + MD5_HEX(_nowtime.group(1)))
        # 调用des.js
        js_str = get_js()
        ctx = execjs.compile(js_str)
        params = str(base64.b64encode(ctx.call('strEnc', params, _deskey.group(1)).encode("utf-8")), "utf-8")

        # params的最终值
        params = 'params='+params+'&token='+token+"&timestamp="+_nowtime.group(1)

        # 正式登陆
        res = self.__session__.post(logon_url, headers=logon_header, data=params)
        print(res.text)

        # 查询入学以来的成绩
        cj_para = "sjxz=sjxz1&ysyx=yxcj&zx=1&fx=1&btnExport=%B5%BC%B3%F6&xn1=2023&ysyxS=on&sjxzS=on&zxC=on&fxC=on&menucode_current=S40303"
        cj = self.__session__.post(cj_url, headers=cj_header, data=cj_para)

        # 将返还的成绩写入html文件
        f = open("./cj.html", "w", encoding="utf-8")
        # 替换网页的字符集消除乱码
        f.write(cj.text.replace("GBK", "utf-8"))

        # os.system(r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')
        os.startfile("D:\\Code\\Python\\cj.html")

    def run(self):
        self.login()
        # self.evaluate()


if __name__ == '__main__':
    # username = input('请输入用户名:\n')
    # password = input('请输入密码:\n')
    spider = BBU("", "", "./config.json")
    spider.run()
