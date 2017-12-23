APath = "/Users/yonlif/PycharmProjects/alphaWork/Uruk/babylonienTexts2/"
TPath = "./data/alphaData5"

all = open(APath+r"/texts.txt", 'r')
outtest = open(TPath+r"/test.txt", 'w')
outtrain = open(TPath+r"/train.txt", 'w')
outvalid = open(TPath+r"/valid.txt", 'w')

i = 0
for line in all:
    if line.startswith("http") == False:
        if (i + 2) % 11 == 0:
            outtest.write(line)
        if (i + 1) % 11 == 0:
            outvalid.write(line)
        else:
            outtrain.write(line)
    else:
        if (i + 2) % 11 == 0:
            outtest.write("<ENDTOKEN> ")
        elif (i + 1) % 11 == 0:
            outvalid.write("<ENDTOKEN> ")
        elif i != 0:
            outtrain.write("<ENDTOKEN> ")
        i += 1

outtrain.write("<ENDTOKEN> ")