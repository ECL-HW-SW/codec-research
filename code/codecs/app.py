from SVT import svt_codec
from CodecComparator import CodecComparator

qps = [22,27,32,37]

svt = svt_codec()
for qp in qps:
    svt.set_qp(qp)
    svt.encode()
    svt.add_to_csv()

csv_bowing = svt.get_csvs

comp = CodecComparator()
print(comp.bdrate(svt.get_csvs(),svt.get_csvs()))