"""
CSV parser for KOKMS.
"""
import csv
import StringIO
import chardet

def parse_csv_iter(fp):
#     reader = csv.reader(__enc_fp(fp), dialect=u"excel", \
#                         delimiter=",", lineterminator="\n", quotechar="\"")
    reader = csv.reader(fp, dialect=u"excel", \
                        delimiter=",", lineterminator="\n", quotechar="\"")
    for line in reader:
        yield line

def parse_iter(fp):
    for line in parse_csv_iter(fp):
        if len(line) <= 0:
            continue
        line = map(__decode,line)
        # map
        result_map = dict()
        for i,key in enumerate(('date','time','stat','name','mins')) :
            result_map[key] = line[i]
        yield result_map   

"""
Wrapper for fp to convert desired target encoding automatically.
"""
def __decode(line):
    if len(line) == 0 : return u''
    # workaround.
    detect = chardet.detect(line)
    if detect['confidence'] < 0.55 : 
        raise IOError('Encoding error, confidence is too low.')
    line = line.decode(detect['encoding']) 
    # rewind enc_fp and return. 
    return line