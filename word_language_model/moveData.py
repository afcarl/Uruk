APath = "/Users/yonlif/Desktop/alphaTmp"
TPath = "./data/alphaData"

all = open(APath+r"/textsAfterTokenizatiom.txt", 'r')
outtest = open(TPath+r"/test.txt", 'w')
outtrain = open(TPath+r"/train.txt", 'w')
outvalid = open(TPath+r"/valid.txt", 'w')

i = 0
for line in all:
    if line.startswith("http") == False:
        if i < 170:
            outtest.write(line)
        if 170 <= i <= 340:
            outvalid.write(line)
        if i > 340:
            outtrain.write(line)
    else:
        if i < 170 and i != 0:
            outtest.write("<ENDTOKEN> ")
        if 170 <= i <= 340:
            outvalid.write("<ENDTOKEN> ")
        if i > 340:
            outtrain.write("<ENDTOKEN> ")
        i += 1

outtrain.write("<ENDTOKEN> ")