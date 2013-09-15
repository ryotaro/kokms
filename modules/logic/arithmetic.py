#!coding:utf-8

def summation(data,price,rate=0.0):
    ret = {}
    ret['mins'] = sum(map(lambda x: x['mins'], data))
    ret['summation'] = int(price * (ret['mins'] / 60.0))
    ret['payment'] = ret['summation'] * (1 - rate)
    ret['subtract'] = ret['summation'] * rate
    return ret

