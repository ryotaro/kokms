"""
CSV parser for KOKMS.
"""
import csv
import StringIO
import chardet
import StringIO
import codecs
def parse_csv_iter(fp):
    import pdb
    pdb.set_trace()
#     reader = csv.reader(__enc_fp(fp), dialect=u"excel", \
#                         delimiter=",", lineterminator="\n", quotechar="\"")
    # Use StringIO to eliminate BOM.
    str_fp = StringIO.StringIO()
    file_string_all = fp.read()
    # Propagate encode and remove BOM if necessary.
    detect = chardet.detect(file_string_all)
    file_string_all = file_string_all.decode(detect['encoding'])
    if detect['encoding'] == "UTF-8":
        # remove BOM
        file_string_all = \
        file_string_all.lstrip(codecs.BOM_UTF8.decode('UTF-8'))
    str_fp.write(file_string_all.encode('UTF-8'))
    str_fp.seek(0)
    reader = csv.reader(str_fp, dialect=u"excel", \
                        delimiter=",", lineterminator="\n", quotechar="\"")
    for line in reader:
        yield map(lambda x: x.decode(detect['encoding']), line)

def parse_iter(fp):
    for line in parse_csv_iter(fp):
        if len(line) <= 0:
            continue
        result_map = dict()
        for i,key in enumerate(('date','time','stat','name','mins')) :
            result_map[key] = line[i]
        yield result_map

