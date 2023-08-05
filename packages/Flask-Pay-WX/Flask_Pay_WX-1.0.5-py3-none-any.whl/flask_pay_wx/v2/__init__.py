from typing import Dict

from flask_pay_wx.v2.Tools import Tools


class PayOrder(object):

    def __init__(self, private_key: str, app_id: str = None, mch_id: str = None, nonce_str: str = None, product_body: str = None,
                 out_trade_no: str = None, total_fee: str = None, spbill_create_ip: str = None, notify_url: str = None,
                 trade_type: str = 'JSAPI', open_id: str = None, sign_type: str = 'MD5'):
        self.private_key = private_key
        self.app_id = app_id
        self.mch_id = mch_id
        self.nonce_str = nonce_str
        self.product_body = product_body
        self.out_trade_no = out_trade_no
        self.total_fee = total_fee
        self.spbill_create_ip = spbill_create_ip
        self.notify_url = notify_url
        self.trade_type = trade_type
        self.open_id = open_id
        self.sign_type = sign_type

    def to_dict(self) -> Dict:
        data = {
            'xml': {}
        }
        data['xml']['appid'] = self.app_id
        data['xml']['mch_id'] = self.mch_id
        data['xml']['nonce_str'] = self.nonce_str
        data['xml']['body'] = self.product_body
        data['xml']['out_trade_no'] = self.out_trade_no
        data['xml']['total_fee'] = self.total_fee
        data['xml']['spbill_create_ip'] = self.spbill_create_ip
        data['xml']['notify_url'] = self.notify_url
        data['xml']['trade_type'] = self.trade_type
        if self.trade_type == 'JSAPI':
            data['xml']['openid'] = self.open_id
        sign = self._get_sign()
        data['xml']['sign'] = sign
        return data

    def _get_sign(self) -> str:
        if self.trade_type == 'JSAPI':
            sort_str = '''appid={0}&body={1}&mch_id={2}&nonce_str={3}&notify_url={4}&openid={5}&out_trade_no={6}&
                       &spbill_create_ip={7}&trade_type={8}&total_fee={9}'''.format(self.app_id, self.product_body, self.mch_id,
                        self.nonce_str, self.notify_url, self.open_id, self.out_trade_no, self.spbill_create_ip,
                        self.trade_type, self.total_fee)
        else:
            sort_str = '''appid={0}&body={1}&mch_id={2}&nonce_str={3}&notify_url={4}&out_trade_no={5}&
                        &spbill_create_ip={6}&trade_type={7}&total_fee={8}'''.format(self.app_id, self.product_body, self.mch_id,
                        self.nonce_str, self.notify_url, self.out_trade_no, self.spbill_create_ip, self.trade_type, self.total_fee)

        encryption_str = self._encryption_str(sort_str)
        return encryption_str

    # 加密字符串
    def _encryption_str(self, origin_str: str) -> str:
        string_sign_temp = "{0}&key={1}".format(origin_str, self.private_key)
        if self.sign_type == 'MD5':
            sign = Tools.md5(string_sign_temp)
        else:
            sign = Tools.hmac_sha256(self.private_key, string_sign_temp)
        return sign


class QueryOrder(object):

    def __init__(self, private_key: str, app_id: str = None, mch_id: str = None, nonce_str: str = None, out_trade_no: str = None,
                 transaction_id: str = None, sign_type: str = 'MD5'):
        self.private_key = private_key
        self.app_id = app_id
        self.mch_id = mch_id
        self.nonce_str = nonce_str
        self.out_trade_no = out_trade_no
        self.transaction_id = transaction_id
        self.sign_type = sign_type

    def to_dict(self) -> Dict:
        data = {
            'xml': {}
        }
        data['xml']['appid'] = self.app_id
        data['xml']['mch_id'] = self.mch_id
        data['xml']['nonce_str'] = self.nonce_str
        if self.out_trade_no is not None:
            data['xml']['out_trade_no'] = self.out_trade_no

        if self.transaction_id is not None:
            data['xml']['transaction_id'] = self.transaction_id

        data['xml']['sign_type'] = self.sign_type

        sign = self._get_sign()
        data['xml']['sign'] = sign
        return data

    def _get_sign(self) -> str:
        if self.out_trade_no is not None:
            sort_str = '''appid={0}&mch_id={1}&nonce_str={2}&out_trade_no={3}&sign_type={4}'''\
                        .format(self.app_id, self.mch_id, self.nonce_str, self.out_trade_no, self.sign_type)
        else:
            sort_str = '''appid={0}&mch_id={1}&nonce_str={2}&sign_type={3}&transaction_id={4}'''\
                        .format(self.app_id, self.mch_id, self.nonce_str, self.sign_type, self.transaction_id)

        encryption_str = self._encryption_str(sort_str)
        return encryption_str


    # 加密字符串
    def _encryption_str(self, origin_str: str) -> str:
        string_sign_temp = "{0}&key={1}".format(origin_str, self.private_key)
        if self.sign_type == 'MD5':
            sign = Tools.md5(string_sign_temp)
        else:
            sign = Tools.hmac_sha256(self.private_key, string_sign_temp)
        return sign
