import pandas as pd
from pandas import DataFrame
COL_TYPE = {'fdt_mean':float,'fdt_std':float}

INPUTS_train = [r'./data/train-time_{0}'.format(i) for i in range(0,3)]
INPUTS_test =[r'./data/test-time_{0}'.format(i) for i in range(0,2)]
OUTPUTS = [r'./data/train-time', r'./data/test-time']

for i in range(0,1):
    k=0
    if(i==0):
        INPUTS=INPUTS_train
    else:
        INPUTS=INPUTS_test
    for f in INPUTS:
        raw=pd.read_csv(f,dtype=COL_TYPE)
        print "csv read success!"
        need=raw[['fdt_mean','fdt_std']]
        if (k!=0):
            need=pd.concat([last_need,need])
        last_need=need
        k=k+1
    need.to_csv(OUTPUTS[i], index=False)
    del need,raw,last_need
