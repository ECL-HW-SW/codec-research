from EVC import EVC
from CodecComparator import CodecComparator
import os


qps = [22,27,32,37]

evc = EVC()
for qp in qps:
    evc.set_qp(qp)
    evc.encode()
    a = evc.parse()
    evc.add_to_csv(a)

comp = CodecComparator()
print(comp.bdrate(evc.get_csvs(),evc.get_csvs()))