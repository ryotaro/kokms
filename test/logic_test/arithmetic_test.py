# !coding:utf-8

from nose.tools import with_setup, ok_, eq_
from modules.logic.arithmetic import * 

def test_summation():
    target = []
    target.append({'begintime':u"14:57:47",'endtime':u'18:05:32','mins':185 })
    target.append({'begintime':u"",'endtime':u'18:11:28','mins':135 })
    ret = summation(data=target, price=800)
    eq_(ret['mins'],320)
    eq_(ret['payment'], 4266)
    eq_(ret['subtract'], 0)
    eq_(ret['summation'], 4266)

    ret = summation(data=target, price=800, rate=0.5)
    eq_(ret['summation'], 4266)
    eq_(ret['payment'], 2133)
    eq_(ret['subtract'], 2133)
    eq_(ret['mins'],320)
    