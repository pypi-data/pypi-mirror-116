import os
from typing import Dict

from flask import Flask

from flask_pay_wx.MiniPayBean import MiniPayBean
from flask_pay_wx.v2.mini.PayHelper import PayHelper as PayMiniV2Helper
from flask_pay_wx.v3.mini.PayHelper import PayHelper as PayV3Helper


class PayManager(object):

    def __init__(self):
        self.app = None
        self.app_id = None
        self.app_secret = None

    def init_app(self, app: Flask):
        self.app = app
        self.app_id = app.config.get('APP_ID') # 小程序id
        self.app_secret = app.config.get('APP_SECRET') # 小程序secret
        self.pay_type = app.config.get('APP_PAY_TYPE') # 支付类型v2， v3
        self.mch_id = app.config.get('MCH_ID') # 商户id
        self.serial_no = app.config.get('SERIAL_NO') # 商户API证书serial_no，只针对v3支付
        self.pay_v2_helper = PayMiniV2Helper(self.app, self.app_id, self.mch_id)
        self.pay_v3_helper = PayV3Helper(self.app, self.app_id, self.mch_id, self.serial_no,)

    # 小程序发起支付v2， 返回支付信息
    def pay_order_mini_v2(self, private_key: str, open_id: str, total_fee: str, spbill_create_ip: str, notify_url: str,
                  sign_type: str = 'MD5', trade_type: str = 'JSAPI', product_describe: str = "正源-小店") -> (bool, MiniPayBean):
        result, result_obj = self.pay_v2_helper.handle_pay(private_key, open_id, total_fee, spbill_create_ip, notify_url,
                                                      sign_type, trade_type, product_describe)
        return result, result_obj

    # 小程序支付v2查询订单， 返回订单详情
    def query_order_mini_v2(self, private_key: str, sign_type: str = 'MD5', transaction_id: str = None,
                       out_trade_no: str = None) -> Dict:

        result_dict = self.pay_v2_helper.query_order(private_key, sign_type, transaction_id, out_trade_no)
        return result_dict

    # 小程序发起支付v3， 返回支付信息
    # open_id: open_id, total_fee: 总费用(单位:分), notify_url: 回调地址, product_describe:产品描述, api_client_key_path: 加密私钥路径 商户私钥路径
    def pay_order_mini_v3(self, open_id: str, total_fee: str, notify_url: str, product_describe: str, api_client_key_path: str) -> (bool, MiniPayBean):
        if self.app_id is None or self.mch_id is None or self.serial_no is None:
            self.app.logger.info("pay_order_v3 is none")
            return False, None

        self.app.logger.info("pay_order_v3 path:%s" % api_client_key_path)
        self.pay_v3_helper.api_client_key_path = api_client_key_path
        result, result_obj  = self.pay_v3_helper.handle_pay(open_id, total_fee, notify_url, product_describe)
        return result, result_obj

    # 小程序支付v3查询订单，返回订单详情，支付结果数据，详见(https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_5_5.shtml
    def query_order_mini_v3(self, transaction_id: str = None, out_trade_no: str = None) -> (bool, Dict):
        result, result_obj = self.pay_v3_helper.query_order(transaction_id, out_trade_no)
        return result, result_obj
