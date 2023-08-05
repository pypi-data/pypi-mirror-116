import json
from typing import Dict


# 支付签名
class SignData(object):

    def __init__(self, mchid: str, serial_no: str, time_stamp: str, nonce_str: str, signature: str,
                 auth_type: str = "WECHATPAY2-SHA256-RSA2048"):
        self.mchid = mchid
        self.serial_no = serial_no
        self.time_stamp = time_stamp
        self.nonce_str = nonce_str
        self.signature = signature
        self.auth_type = auth_type

    def to_dict(self) -> Dict:
        data = {
            'mchid': self.mchid,
            'nonce_str': self.nonce_str,
            'signature': self.signature,
            'timestamp': self.time_stamp,
            'serial_no': self.serial_no
        }
        return data

    def to_string(self) -> str:
        auth_str = '{0} mchid="{1}",nonce_str="{2}",signature="{3}",timestamp="{4}",serial_no="{5}"'.\
            format(self.auth_type, self.mchid, self.nonce_str, self.signature, self.time_stamp, self.serial_no)
        return auth_str


class PayOrder(object):

    def __init__(self, app_id: str = None, mch_id: str = None, description: str = None,
                 out_trade_no: str = None, total_fee: str = None, notify_url: str = None, open_id: str = None):
        self.app_id = app_id
        self.mch_id = mch_id
        self.description = description
        self.out_trade_no = out_trade_no
        self.total_fee = total_fee
        self.notify_url = notify_url
        self.open_id = open_id

    def to_dict(self) -> Dict:
        data = {
            'appid': self.app_id,
            'mchid': self.mch_id,
            'out_trade_no': self.out_trade_no,
            'description': self.description,
            'notify_url': self.notify_url,
            'amount': {
                'total': self.total_fee
            },
            'payer': {
                'openid': self.open_id
            }
        }
        return data

    def to_string(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
