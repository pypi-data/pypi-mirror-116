import sys


class Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const %s value!" % name)
        if not name.isupper():
            raise self.ConstCaseError("const %s is not all letters are capitalized" % name)
        self.__dict__[name] = value


sys.modules[__name__] = Const()

Const.SIGNTYPE_V2_MD5 = "MD5"
Const.SIGNTYPE_V2_SHA256 = "HMAC-SHA256"
Const.SIGNTYPE_V3_RSA = "RSA"