import random
import string
import time

class Util(object):
    # byte转字符串
    @staticmethod
    def byte_to_str(content) -> str:
        return str(content, encoding='utf-8')

    # 随机字符串 32位
    @staticmethod
    def get_nonce_str(nums: int = 32) -> str:
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, nums))
        return ran_str.upper()

    # 生成订单编号
    @staticmethod
    def get_out_trade_no() -> str:
        timestamp = int(time.time() * 1000)
        ran_str = Util.get_nonce_str(8)
        return '{0}{1}'.format(timestamp, ran_str)