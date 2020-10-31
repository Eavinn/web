# coding=utf-8
from typing import Any

from ihome.libs.yuntongxun.CCPRestSDK import REST

# 主帐号
accountSid = '8aaf0708635e4ce001636d4699060a6f'
# 主帐号Token
accountToken = '029cfdb158cc4af3a87d2618859694ca'

# 应用Id
appId = '8aaf0708635e4ce001636d4699610a76'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


class CCP(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            obj = super().__new__(cls, *args, **kwargs)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.__instance = obj
        return cls.__instance

    def send_template_sms(self, to, datas, tempId):
        """
        发送模板短信
        @param to 手机号码
        @param datas 内容数据
        @param $tempId 模板Id
        """
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        print(result)
        if result.get('statusCode') == '000000':
            return True
        else:
            return False


if __name__ == '__main__':
    CCP().send_template_sms("13534240218", ["8888", "6"], 1)


