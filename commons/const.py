# -*- coding: UTF-8 -*-

__author__ = 'yangtianhang'


class _const(object):
    class ConstError(TypeError): pass
    class ConstCaseError(TypeError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise _const.ConstError, "Cannot change const.%s" % (name,)
        if not name.isupper():
            raise _const.ConstCaseError, 'const name "%s" is not all uppercase' % (name,)

        self.__dict__[name] = value


import sys
sys.modules[__name__] = _const()