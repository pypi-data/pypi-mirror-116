
import hashlib, hmac
from typing import Dict
import xmltodict


class Tools(object):

    # md5加密
    @staticmethod
    def md5(content: str) -> str:
        sign = hashlib.md5(content.encode('utf8')).hexdigest().upper()
        return sign

    # hmac_sha256加密
    @staticmethod
    def hmac_sha256(private_key: str, content: str) -> str:
        sign = hmac.new(private_key.encode('utf-8'), content.encode('utf-8'), hashlib.sha256).hexdigest().upper()
        return sign

    @staticmethod
    def handle_xml_to_str(content: Dict) -> str:
        return xmltodict.unparse(content)

    @staticmethod
    def handle_xml_str_to_dict(content: str) -> Dict:
        return xmltodict.parse(content)
