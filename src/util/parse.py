# coding:utf-8

import ConfigParser
import collections
import string

__author__ = 'ren'


def parse_ini(ini_file):
    ini = ConfigParser.SafeConfigParser()
    ini.read(ini_file)

    item_set = collections.OrderedDict()
    for section in ini.sections():
        items = {}

        for option in ini.options(section):
            value = ini.get(section, option)
            if string.isinteger(value):
                value = int(value)
            elif string.isfloat(value):
                value = float(value)
            elif string.islist(value):
                value = string.tolist(value)
            elif string.istuple(value):
                value = string.totuple(value)

            items.setdefault(option, value)

        item_set.setdefault(section, items)

    return item_set

