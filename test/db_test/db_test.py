# !coding:utf-8

from nose.tools import with_setup, ok_, eq_
from modules.databases.db import *

TEST_SESSION_NAME = '__test__'

def setup():
    session = open_session(TEST_SESSION_NAME)
    # Drop all
    session.query(KokmsCore).delete()
    # Insert some DB.
    session.add(KokmsCore(u"2013/05/28", u"18:23:12", u"退室", u"◆池田　涼太郎", 205))
    session.add(KokmsCore(u"2013/05/28", u"18:23:12", u"退室", u"◆池田　涼太郎", 205))
    session.add(KokmsCore(u"2013/05/28", u"14:58:02", u"入室", u"◆池田　涼太郎", None))
    session.add(KokmsCore(u"2013/05/24", u"18:05:32", u"退室", u"◆池田　涼太郎", 188))
    session.add(KokmsCore(u"2013/05/24", u"14:57:47", u"入室", u"◆池田　涼太郎", None))
    session.add(KokmsCore(u"2013/05/23", u"18:11:28", u"退室", u"◆池田　涼太郎", 135))
    session.add(KokmsCore(u"2013/05/28", u"14:58:02", u"入室", u"◆池田　涼太郎", None))
    session.add(KokmsCore(u"2013/05/24", u"18:05:32", u"退室", u"◆池田　涼太郎", 188))
    session.add(KokmsCore(u"2013/05/24", u"14:57:47", u"入室", u"◆池田　達郎", None))
    session.add(KokmsCore(u"2013/05/23", u"18:11:28", u"退室", u"◆池田　瑛香", None))
    session.commit() 

@with_setup(setup)
def test_get_names():
    session = open_session(TEST_SESSION_NAME)
    # Expecting list.
    it = iterator_name(session)
    names = [x for x in it]
    ok_(len(names) > 0)
    print names[0].encode('utf-8', 'utf-8')
    ok_(names.count(u'◆池田　涼太郎') == 1)
    ok_(names.count(u'◆池田　達郎') == 1)
    ok_(names.count(u'◆池田　瑛香') == 1)

@with_setup(setup)
def test_min_date():
    session = open_session(TEST_SESSION_NAME)
    # mindate must be the pastest.
    eq_(get_mindate(session) , u"2013/05/23")

@with_setup(setup)
def test_max_date():
    session = open_session(TEST_SESSION_NAME)
    # mindate must be the pastest.
    eq_(get_maxdate(session) , u"2013/05/28")

@with_setup(setup)
def test_existing_dates():
    session = open_session(TEST_SESSION_NAME)
    existing_dates = iterator_existing_dates(session)
    l = [x for x in existing_dates]
    # All dates are correctly extracted
    eq_(l.count(u"2013/05/28"), 1)
    eq_(l.count(u"2013/05/24"), 1)
    eq_(l.count(u"2013/05/23"), 1)
    # Other dates aren't contained nor duplicated.
    eq_(len(l), 3)
    
@with_setup(setup)
def test_filterby_name_date():
    session = open_session(TEST_SESSION_NAME)
    record_iter = iterator_filterby_name_date(\
                     session=session, \
                     name=u"◆池田　涼太郎", \
                     begindate=u"2013/05/23", \
                     enddate=u"2013/05/24")
    date, name = [], []
    for entity in record_iter:
        date.append(entity.date)
        name.append(entity.name) 
    eq_(len(date) , 4)
    eq_(name.count(u"◆池田　涼太郎"), 4)
    eq_(name.count(u"◆池田　達郎"), 0)
    eq_(name.count(u"◆池田　瑛香"), 0)
    eq_(date.count(u"2013/05/28"), 0)
