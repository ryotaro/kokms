#!coding:utf-8

def summation(data,price,rate=0.0):
    ret = {}
    ret[u'mins'] = sum(map(lambda x: x[u'mins'], data))
    ret[u'summation'] = int(price * (ret[u'mins'] / 60.0))
    ret[u'payment'] = ret[u'summation'] * (1 - rate)
    ret[u'subtract'] = ret[u'summation'] * rate
    return ret

