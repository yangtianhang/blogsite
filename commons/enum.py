# -*- coding: UTF-8 -*-

__author__ = 'yangtianhang'


class Enumeration(object):
    class EnumError(TypeError):
        pass

    def __init__(self, name, enum_list, values_are_unique=True):
        self.__doc__ = name
        self.lookup = dict()
        self.reverselookup = dict()
        value = 0
        for x in enum_list:
            if type(x) is tuple:
                try:
                    x, value = x
                except ValueError:
                    raise Enumeration.EnumError("tuple doesn't have 2 items: %r" % (x,))
                if type(x) is not str:
                    raise Enumeration.EnumError("enum name is not a string: %r" % (x,))
                if type(value) is not int:
                    raise Enumeration.EnumError("enum value is not a integer: %r" % (value,))
                if x and value in self.lookup:
                    raise Enumeration.EnumError("enum name is not unique: %r" % (x,))
                if values_are_unique and value in self.reverselookup:
                    raise Enumeration.EnumError("enum value %r not unique for %r" % (value, x))

            self.lookup[x] = value
            self.reverselookup[value] = x
            value += 1

    def __getattr__(self, name):
        try:
            return self.lookup[name]
        except KeyError:
            raise AttributeError(name)

    def whatis(self, value):
        return self.reverselookup[value]