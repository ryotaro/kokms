#!coding: utf-8
from nose import *
from nose.tools import *
from modules.logic.csvparser import parse_iter 
import csv

"""
Test simple data is successfully read.
"""
def test_basic_usage():
    dat_iter = parse_iter(open("./test/testdata_minimal.txt","r"))
    # Will be like following :
    # "2013/05/31","18:19:45","退室","◆池田　涼太郎","202",""
    # "2013/05/31","14:57:15","入室","◆池田　涼太郎","",""
    # "2013/05/30","18:14:13","退室","◆池田　涼太郎","137",""
    # "2013/05/30","15:57:27","入室","◆池田　涼太郎","",""

    line = dat_iter.next()
    eq_(line[0],"2013/05/31")
    eq_(line[1],"18:19:45")
    eq_(line[2],"退室")
    eq_(line[3],"◆池田　涼太郎")
    eq_(line[4],"202")
    ok_(line[5] == "")
    line = dat_iter.next()
    eq_(line[0],"2013/05/31")
    eq_(line[1],"14:57:15")
    eq_(line[2],"入室")
    eq_(line[3],"◆池田　涼太郎")
    ok_(line[4] == "")
    ok_(line[5] == "")
    