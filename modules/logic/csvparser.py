"""
CSV parser for KOKMS.
"""
import csv
import StringIO
import chardet

def parse_iter(fp):
#     reader = csv.reader(__enc_fp(fp), dialect=u"excel", \
#                         delimiter=",", lineterminator="\n", quotechar="\"")

    reader = csv.reader(fp, dialect=u"excel", \
                        delimiter=",", lineterminator="\n", quotechar="\"")
    for line in reader:
        yield line

"""
Wrapper for fp to convert desired target encoding automatically.
"""
def __enc_fp(fp):
    # workaround.
    enc_fp = StringIO.StringIO()
    for line in fp:
        detect = chardet.detect(line)
        if detect['confidence'] < 0.95 : 
            raise IOError('Encoding error, confidence is too low.')
        enc_fp.write(line.decode(detect['encoding']))
        enc_fp.write(u'\n')
    
    # rewind enc_fp and return. 
    return enc_fp