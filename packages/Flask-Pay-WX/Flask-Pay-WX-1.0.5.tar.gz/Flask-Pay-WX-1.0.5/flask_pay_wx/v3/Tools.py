import json
from typing import Dict

from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64

from flask_pay_wx.utils.Util import Util
from flask_pay_wx.v3 import SignData


class Tools(object):

    # SHA256 with RSA 签名
    # 可以是公钥，也可以是私钥
    @staticmethod
    def sign_sha256_with_rsa(content: str, key_path: str) -> str:

        with open(key_path) as f:
            apiclient_key = f.read()
            data = content.encode("utf-8")  # 将字符串转换成bytes对象

            rsa_key = RSA.importKey(apiclient_key)
            sign = PKCS1_v1_5.new(rsa_key)

            sha_data = SHA256.new(data)  # 签名算法使用SHA256，需根据业务要求进行调整
            sign_data = sign.sign(sha_data)  # 签名

            result = base64.b64encode(sign_data)  # 将签名后的内容，转换为base64编码
            result = result.decode("utf-8")
            return result

    # 字符串转json
    @staticmethod
    def str_to_json(content):
        return json.loads(content)

    # 处理签名(生成签名) 查看https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_0.shtml
    # 通过商户私钥生成签名
    # mch_id: 商户号
    # serial_no: 商户API证书serial_no，用于声明所使用的证书（管理员账号登录微信商户管理后台，在API安全里面点击查看证书可以获取。）
    # api_client_key_path: 私钥 商户私钥
    # request_type: HTTP请求的方法（GET,POST,PUT）等
    # request_url: 签名的URL。如果请求中有查询参数，URL末尾应附加有'?'和对应的查询字符串。
    # time_stamp: 起请求时的系统当前时间戳
    # nonce_str: 生成一个请求随机串
    # body: 请求报文主体 1.GET时报文主体为空。2.POST或PUT时，请使用真实发送的JSON报文
    @staticmethod
    def handle_sign(mch_id: str, serial_no: str, api_client_key_path: str, request_type: str, request_url: str,
                    time_stamp: str, nonce_str: str, body: str = None) -> str:
        sort_str = "{0}\n{1}\n{2}\n{3}\n".format(request_type, request_url, time_stamp, nonce_str)
        if body is None:
            sort_str = "{0}\n".format(sort_str)
        else:
            sort_str = "{0}{1}\n\n".format(sort_str, body)

        auth_str = Tools.sign_sha256_with_rsa(sort_str, api_client_key_path)
        sign_data = SignData(mchid=mch_id, serial_no=serial_no, time_stamp=time_stamp, nonce_str=nonce_str,
                             signature=auth_str)
        sign_data_str = sign_data.to_string()
        return sign_data_str

    # 验证签名，验证是否是微信发的 通过微信支付平台公钥验证签名(https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_1.shtml)
    # 通过微信支付平台公钥生成签名，验证与发来的签名是否一致
    # time_stamp: 应答时间戳
    # nonce_str: 应答随机串
    # response_body: 应答主体
    # real_signature: 应答签名
    # wx_public_key_path: 微信支付平台公钥路径
    @staticmethod
    def verify_sign(time_stamp: str, nonce_str: str, response_body: str, real_signature: str, wx_public_key_path: str) -> bool:
        result = False
        sort_str = "{0}\n{1}\n{2}\n".format(time_stamp, nonce_str, response_body)
        sign_str = Tools.sign_sha256_with_rsa(sort_str, wx_public_key_path)
        if sign_str == real_signature:
            result = True
        return result

    # 解密支付结果数据，详见(https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_5_5.shtml)
    # 通过商户公钥加密，用商户私钥解密
    # api_v3_key: 公钥
    # nonce: 加密使用的随机串初始化向量
    # ciphertext：Base64编码后的密文
    # associated_data：附加数据包（可能为空）
    @staticmethod
    def decrypt_data(api_v3_key: str, nonce: str, ciphertext: str, associated_data: str) -> Dict:
        key_bytes = str.encode(api_v3_key)
        nonce_bytes = str.encode(nonce)
        ad_bytes = str.encode(associated_data)
        data = base64.b64decode(ciphertext)

        aesgcm = AESGCM(key_bytes)
        result_bytes = aesgcm.decrypt(nonce_bytes, data, ad_bytes)
        return Tools.str_to_json(Util.byte_to_str(result_bytes))
