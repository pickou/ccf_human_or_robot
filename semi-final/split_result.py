# encoding=utf-8
from __future__ import division
import os

DATA_DIR = '/home/era/Documents/my_workplace/zhou/data/'
TMP_DIR = DATA_DIR + 'tmp/'

if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)


###############################################################################
# split result
###############################################################################
def split_result(offline):
    if offline:  # if offline then we calculte F1 score
        true_label = open(TMP_DIR + 'test-label', 'r')
        #true_label.readline() # ignore header
        TP = 0
        FP = 0
        FN = 0
        TN = 0
    with open('./lightgbm/LightGBM_predict_result.txt', 'r') as result:
        high = open('./high_result.csv', 'w')
        low = open('./low_result.csv', 'w')
        rank = 0
        for line in result:
            p = float(line.strip())
            if offline:
                tmp=true_label.readline().rstrip('\n').strip()
               # print tmp.strip()
                try:
                    label = float(tmp.strip())
                except ValueError,e:
                    print "error",e,"on line",tmp

            if p >0.5:
                high.write(str(rank) + '\n')
                if offline:
                    if label == 1:  TP += 1
                    else:           FP += 1
            else:
                low.write(str(rank) + '\n')
                if offline:
                    if label == 1:  FN += 1
                    else:           TN += 1
            rank += 1

        high.close()
        low.close()
       # print TP
        if offline:
            F1 = (2*TP) / (2*TP + FP + FN)
            print('offline test, F1 score: ' + str(F1))
            print(TN/(TN+FN))
            print(TP/(TP+FP))


if __name__ == '__main__':
    split_result(offline=True)
    #split_result(offline=False)
