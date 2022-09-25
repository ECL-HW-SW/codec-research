from EVC import EVC
from CodecComparator import CodecComparator
from SVT import svt_codec
from MetricsCalculator import MetricsCalculator
qps = [22,27,32,37]

svt = svt_codec()
evc = EVC()
metrics = MetricsCalculator()
for qp in qps:
    svt.set_qp(qp)
    #svt.encode()
    #print('SVT ENCODED')
    #svt.add_to_csv()
    #print('SVT added csv')
    #svt.decode()
    evc.set_qp(qp)
    #evc.encode()
    #evc.decode()
    #print('EVC ENCODED')
    #a = evc.parse()
    #print('EVC PARSED')
    #evc.add_to_csv(a)
    #print('EVC ADDED TO CSVS')

comp = CodecComparator()
print("SVT-EVC BDRATE:", comp.bdrate(svt.get_csvs(), evc.get_csvs()))