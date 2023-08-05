from typing import Dict

import json

from flask_pay_wx import Const
from flask_pay_wx.v2.Tools import Tools as ToolsV2
from flask_pay_wx.v3.Tools import Tools as ToolsV3


# 返回给微信小程序端参数
class MiniPayBean(object):

    def __init__(self, app_id: str = None, time_stamp: str = None, nonce_str: str = None, package: str = None,
                 sign_type: str = Const.SIGNTYPE_V2_MD5, pay_sign: str = None, out_trade_no: str = None, err_msg: str = None):
        self.app_id = app_id
        self.time_stamp = time_stamp
        self.nonce_str = nonce_str
        self.package = package
        self.sign_type = sign_type
        self.pay_sign = pay_sign
        self.out_trade_no = out_trade_no # 服务端的订单号
        self.err_msg = err_msg

    def to_dict(self) -> Dict:
        if self.err_msg is None:
            data = {
                'timeStamp': self.time_stamp,
                'nonceStr': self.nonce_str,
                'package': self.package,
                'signType': self.sign_type,
                'paySign': self.pay_sign
            }
        else:
            data = {
                'err_msg': self.err_msg
            }
        return data

    def to_string(self) -> str:
        result = json.dumps(self.to_dict(), ensure_ascii=False)
        return result

    # 封好签名
    def sign_data(self, private_key: str = None, api_client_key_path: str = None):
        sort_str = 'appId={0}&nonceStr={1}&package={2}&signType={3}&timeStamp={4}&key={5}'\
            .format(self.app_id, self.nonce_str, self.package, self.sign_type, self.time_stamp, private_key)
        if self.sign_type == Const.SIGNTYPE_V2_MD5:
            # v2支付
            sign = ToolsV2.md5(sort_str)
        elif self.sign_type == Const.SIGNTYPE_V2_SHA256:
            # v2支付
            sign = ToolsV2.hmac_sha256(private_key, sort_str)
        else:
            # v3支付
            sort_str = '{0}\n{1}\n{2}\n{3}\n'.format(self.app_id, self.time_stamp, self.nonce_str, self.package)
            sign = ToolsV3.sign_sha256_with_rsa(sort_str, api_client_key_path)
        self.pay_sign = sign