import sys
import time
from typing import Dict

import requests
from flask import Flask

from flask_pay_wx import Const
from flask_pay_wx.MiniPayBean import MiniPayBean
from flask_pay_wx.utils.Util import Util
from flask_pay_wx.v3 import PayOrder
from flask_pay_wx.v3.Tools import Tools


class PayHelper(object):

    def __init__(self, app: Flask, app_id: str, mch_id: str, serial_no: str, api_client_key_path: str = None):
        self.app = app
        self.app_id = app_id
        self.mch_id = mch_id
        self.serial_no = serial_no
        self.api_client_key_path = api_client_key_path #商户私钥
        self.BASE_URL = "https://api.mch.weixin.qq.com"

    # 处理支付
    def handle_pay(self, open_id: str, total_fee: str, notify_url: str, product_describe: str) -> (bool, MiniPayBean):
        result = True
        result_obj = None
        mini_pay_bean = MiniPayBean()

        try:
            nonce_str = Util.get_nonce_str()
            out_trade_no = Util.get_out_trade_no()
            pay_order = PayOrder(app_id=self.app_id, mch_id=self.mch_id,
                                 description=product_describe,
                                 out_trade_no=out_trade_no, total_fee=total_fee,
                                 notify_url=notify_url,open_id=open_id)
            sub_url = "/v3/pay/transactions/jsapi"
            url = "{0}{1}".format(self.BASE_URL, sub_url)
            cur_time_stamp = str(int(time.time()))
            content = pay_order.to_string()
            sign_str = Tools.handle_sign(self.mch_id, self.serial_no, self.api_client_key_path, "POST", sub_url,
                                         cur_time_stamp, nonce_str, content)
            self.app.logger.info("v3 handle_pay sign_str:%s", sign_str)
            self.app.logger.info("v3 handle_pay content:%s", content)
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': sign_str
            }
            response = requests.post(url=url, data=content.encode('utf-8'), headers=headers, timeout=10)
            result = self._handle_pay_order_response(response, nonce_str, mini_pay_bean)
            if result:
                mini_pay_bean.sign_type = Const.SIGNTYPE_V3_RSA
                mini_pay_bean.sign_data(api_client_key_path=self.api_client_key_path)
            mini_pay_bean.out_trade_no = out_trade_no
            result_obj = mini_pay_bean
        except requests.Timeout as exception:
            result = False
            mini_pay_bean.err_msg = '超时了'
            result_obj = mini_pay_bean
            self.app.logger.error('v3 (%s.%s) request timeout exception: %s', self.__class__.__name__,
                                  sys._getframe().f_code.co_name,
                                  str(exception))
        except Exception as exception:
            result = False
            mini_pay_bean.err_msg = '请求异常'
            result_obj = mini_pay_bean
            self.app.logger.error('v3 (%s.%s) other exception: %s', self.__class__.__name__,
                                  sys._getframe().f_code.co_name,
                                  str(exception))
        finally:
            self.app.logger.info("_handle_pay_v3 result:%s, result_msg:%s", result, result_obj.to_string())
            return result, result_obj

    def _handle_pay_order_response(self, response, nonce_str: str, mini_pay_bean: MiniPayBean) -> bool:
        result = True
        status_code = response.status_code
        self.app.logger.info("_handle_pay_order_response code:%s", status_code)
        content = response.content
        result_dict = self._handle_order_response_result(content)
        self.app.logger.info("_handle_pay_order_response content:%s", result_dict)
        if status_code == 200 or status_code == 204:
            time_stamp = str(int(time.time()))
            mini_pay_bean.app_id = self.app_id
            mini_pay_bean.time_stamp = time_stamp
            mini_pay_bean.nonce_str = nonce_str
            mini_pay_bean.package = result_dict['prepay_id']
        elif status_code == 401:
            result = False
            mini_pay_bean.err_msg = "请求失败"
        return result

    # 处理请求结果
    def _handle_order_response_result(self, content) -> Dict:
        result_str = Util.byte_to_str(content)
        result_dict = Tools.str_to_json(result_str)
        return result_dict

    # 查询订单
    def query_order(self, transaction_id: str = None, out_trade_no: str = None) -> (bool, Dict):
        result = False
        result_obj = {}
        if transaction_id is not None:
            sub_url = '{0}{1}'.format('/v3/pay/transactions/id/', transaction_id)
            url = "{0}{1}{2}".format(self.BASE_URL, sub_url, transaction_id)
            content = {
                "mchid": self.mch_id
            }
            sign_str, headers = self._query_order_sign('GET', sub_url)
            response = requests.get(url=url, params=content, headers=headers, timeout=10)
            result, result_obj = self._handle_query_order_response(response)

            return result, result_obj

        if out_trade_no is not None:
            sub_url = '{0}{1}'.format('/v3/pay/transactions/out-trade-no/', out_trade_no)
            url = "{0}{1}{2}".format(self.BASE_URL, sub_url, out_trade_no)
            content = {
                "mchid": self.mch_id
            }
            sign_str, headers = self._query_order_sign('GET', sub_url)
            response = requests.get(url=url, params=content, headers=headers, timeout=10)
            result, result_obj = self._handle_query_order_response(response)
            return result, result_obj

        return result, result_obj

    # 查询订单签名
    def _query_order_sign(self, request_type: str, request_url: str) -> (str, Dict):
        nonce_str = Util.get_nonce_str()
        cur_time_stamp = str(int(time.time()))
        sign_url = "{0}?mchid={1}".format(request_url, self.mch_id)
        sign_str = Tools.handle_sign(self.mch_id, self.serial_no, self.api_client_key_path, request_type, sign_url,
                                     cur_time_stamp, nonce_str)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': sign_str
        }
        return sign_str, headers

    # 处理查询订单响应
    def _handle_query_order_response(self, response) -> (bool, Dict):
        query_result_obj = {}
        status_code = response.status_code
        content = response.content
        response_dict = self._handle_order_response_result(content)
        self.app.logger.info("_handle_query_order_response content:%s", response_dict)
        if status_code == 200 or status_code == 204:
            result = True
            query_result_obj = response_dict
        else:
            result = False

        return result, query_result_obj


if __name__ == '__main__':
    # helper = PayHelper(None, "1", "2", "3")
    # result = helper._handle_sign("GET", "/puch", "1655550999", "sdfdsfgree445t5t")
    # print(result)
    request_type = 'GET'
    request_url = '/v3/certificates'
    time_stamp = '1554208460'
    nonce_str = '593BEC0C930BF1AFEB40B4A08C8FB242'
    sort_str = "{0}\n{1}\n{2}\n{3}\n".format(request_type, request_url, time_stamp, nonce_str)
    sort_str = "{0}\n".format(sort_str)
    auth_str = Tools.handle_sign("1","2","../../ach.key", request_type, request_url, time_stamp, nonce_str)

    # auth_str = Tools.sign_sha256(sort_str, "../../ach.key")
    print(auth_str)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': auth_str
    }
    response = requests.get(url="https://api.mch.weixin.qq.com/v3/certificates", headers=headers, timeout=10)
    head_dict = response.headers
    status_code = response.json
    print(status_code)
    print(head_dict['Request-ID'])