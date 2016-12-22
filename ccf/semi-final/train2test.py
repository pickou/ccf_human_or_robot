test=open('./data/test-final','w')
label=open('./data/tmp/test-label','w')
with open('./data/train-final','r') as f:
    while True:
        lines=f.readlines(1000)
        if not lines:
            break
        for line in lines:
            line=line.split(',')
            tmp=line[0]+'\n'
            label.write(tmp)
            line=line[1:]
            line=','.join(line)
            test.write(line)
test.close()
label.close()
