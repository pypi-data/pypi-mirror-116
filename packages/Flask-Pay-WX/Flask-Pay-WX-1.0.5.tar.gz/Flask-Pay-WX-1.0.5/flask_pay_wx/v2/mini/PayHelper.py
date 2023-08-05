import sys
import time
from typing import Dict

import requests
from flask import Flask

from flask_pay_wx.MiniPayBean import MiniPayBean
from flask_pay_wx.utils.Util import Util
from flask_pay_wx.v2 import Tools, PayOrder, QueryOrder


class PayHelper(object):

    def __init__(self, app: Flask, app_id: str, mch_id: str):
        self.app = app
        self.app_id = app_id
        self.mch_id = mch_id

    # private_key:私钥,
    # open_id:用户open_id, 交易类型是JSAPI, openid必传
    # total_fee:金额(单位:分),
    # spbill_create_ip:设备ip地址,
    # notify_url:通知地址,
    # trade_type:交易类型, 小程序是JSAPI
    # product_describe: 商品描述(公司名-产品名)
    def handle_pay(self, private_key: str, open_id: str, total_fee: str, spbill_create_ip: str, notify_url: str,
                       sign_type: str, trade_type: str, product_describe: str) -> (bool, MiniPayBean):
        result = True
        result_obj = None
        mini_pay_bean = MiniPayBean()
        try:
            nonce_str = Util.get_nonce_str()
            out_trade_no = Util.get_out_trade_no()
            pay_order = PayOrder(private_key=private_key, app_id=self.app_id, mch_id=self.mch_id,
                                   nonce_str=nonce_str, product_body=product_describe,
                                   out_trade_no=out_trade_no, total_fee=total_fee,
                                   spbill_create_ip=spbill_create_ip,
                                   notify_url=notify_url, trade_type=trade_type, open_id=open_id,
                                   sign_type=sign_type)
            url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
            content = Tools.handle_xml_to_str(pay_order.to_dict())
            headers = {'Content-Type': 'application/xml'}
            response = requests.post(url=url, data=content.encode('utf-8'), headers=headers, timeout=20)
            result = self._handle_pay_order_response(response, nonce_str, mini_pay_bean)
            if result:
                mini_pay_bean.sign_type = sign_type
                mini_pay_bean.sign_data(private_key=private_key)
            mini_pay_bean.out_trade_no = out_trade_no
            result_obj = mini_pay_bean
        except requests.Timeout as exception:
            result = False
            mini_pay_bean.err_msg = '超时了'
            result_obj = mini_pay_bean
            self.app.logger.error('(%s.%s) request timeout exception: %s', self.__class__.__name__,
                                  sys._getframe().f_code.co_name,
                                  str(exception))
        except Exception as exception:
            result = False
            mini_pay_bean.err_msg = '请求异常'
            result_obj = mini_pay_bean
            self.app.logger.error('(%s.%s) request timeout exception: %s', self.__class__.__name__,
                                  sys._getframe().f_code.co_name,
                                  str(exception))
        finally:
            self.app.logger.info("_handle_pay_v2 result:%s, result_msg:%s", result, result_obj)
            return result, result_obj

    # 处理v2请求响应
    def _handle_pay_order_response(self, response, nonce_str: str, mini_pay_bean: MiniPayBean) -> bool:
        status_code = response.status_code
        response_dict = self._handle_pay_response_result(response.content)
        return_code = response_dict['return_code']
        if status_code == 200 or status_code == 204:
            if return_code == 'SUCCESS':
                result_code = response_dict['result_code']
                if result_code == 'SUCCESS':
                    result = True
                    package = 'prepay_id='.format(response_dict['prepay_id'])
                    time_stamp = str(int(time.time()))
                    mini_pay_bean.app_id = self.app_id
                    mini_pay_bean.time_stamp = time_stamp
                    mini_pay_bean.nonce_str = nonce_str
                    mini_pay_bean.package = package
                else:
                    result = False
                    mini_pay_bean.err_msg = response_dict['err_code']
            else:
                result = False
                mini_pay_bean.err_msg = response_dict['return_msg']
        else:
            result = False
            mini_pay_bean.err_msg = "请求失败"

        return result

    # 处理请求结果
    def _handle_pay_response_result(self, content) -> Dict:
        result_str = Util.byte_to_str(content)
        result_dict = Tools.handle_xml_str_to_dict(result_str)
        return result_dict['xml']

    # 查询订单
    def query_order(self, private_key: str, sign_type: str = 'MD5', transaction_id: str = None,
                       out_trade_no: str = None) -> (bool, Dict):
        result = True
        result_dict = {}
        try:
            nonce_str = Util.get_nonce_str()
            url = 'https://api.mch.weixin.qq.com/pay/orderquery'
            query_order = QueryOrder(private_key=private_key, app_id=self.app_id, mch_id=self.mch_id,
                                     nonce_str=nonce_str,
                                     sign_type=sign_type, transaction_id=transaction_id, out_trade_no=out_trade_no)
            content = Tools.handle_xml_to_str(query_order.to_dict())
            headers = {'Content-Type': 'application/xml'}
            response = requests.post(url=url, data=content.encode('utf-8'), headers=headers, timeout=10)
            result = True
            status_code = response.status_code
            if status_code == 200 or status_code == 204:
                result = True
                result_dict = self._handle_pay_response_result(response.content)
            else:
                result = False
        except requests.Timeout as exception:
            result = False
            self.app.logger.error('(%s.%s) request timeout exception: %s', self.__class__.__name__,
                                  sys._getframe().f_code.co_name,
                                  str(exception))
        except Exception as exception:
            result = False
            self.app.logger.error('(%s.%s) request timeout exception: %s', self.__class__.__name__,
                                  sys._getframe().f_code.co_name,
                                  str(exception))
        return result, result_dict