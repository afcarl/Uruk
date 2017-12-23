import argparse
from os import walk
from pathlib import Path
import operator


parser = argparse.ArgumentParser(description='PyTorch PennTreeBank RNN/LSTM Language Model')
parser.add_argument('--dataLocation', type=str, default='/Users/yonlif/PycharmProjects/alphaWork/Uruk/babylonienTexts/textsOut',
                    help='location of the data to analyze')
parser.add_argument('--logFile', type=str, default='/Users/yonlif/PycharmProjects/alphaWork/Uruk/babylonienTexts/log.txt',
                    help='location of the log file')
parser.add_argument('--ignore', type=str, default='',
                    help='words to ignore')
parser.add_argument('--ignoreStartingWith', type=str, default='http',
                    help='words to ignore that starts with')
args = parser.parse_args()

targateFiles = []
try:
    for (dirpath, dirnames, filenames) in walk(args.dataLocation):
       targateFiles.extend(filenames)
       break
except Exception as e:
    print("Error trying to read the files from " + args.dataLocation)
    print("--- Error: \n" + e)
    print("Exiting")
    exit(1)

print(targateFiles)

my_file = Path(args.logFile)
if my_file.is_file():
    userInput = input(str(args.logFile) + " already exist, are you sure you want to replace it? y or n \n")
    if not (userInput == "yes" or userInput == 'y'):
        print("Exiting")
        exit(0)

# A word object for help
class Word(object):
    def __init__(self):
        self.number = 0
        self.numberOfAppear = 0
        self.dict = {}
        self.numberAfter = 0

    def create(self,number,dict):
        self.number = number
        self.numberOfAppear = 1
        self.dict = dict

    def appear(self):
        self.numberOfAppear += 1

# A dictionary object for help
class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        #self.idx2word = []

    def predict(self,word):
        return max((self.word2idx[word].dict).iteritems(), key=operator.itemgetter(1))[0]

    def add_word(self, word):

        if word not in self.word2idx:
            new = Word()
            new.create(len(self.word2idx) + 1,{})
            #self.idx2word.append(new)
            self.word2idx[word] = new
        else:
            self.word2idx[word].numberOfAppear += 1
            #self.idx2word[self.findIdxByWord(word)].numberOfAppear += 1
        return self.word2idx[word]

    def add_next(self, worda, wordb):
        if wordb not in (self.word2idx[worda]).dict:
            (self.word2idx[worda]).dict[wordb] = 1
        else:
            (self.word2idx[worda]).dict[wordb] += 1

    def findIdxByWord(self, word):
        return self.word2idx[word].number - 1

    def __len__(self):
        return len(self.word2idx)

globalDictionery = Dictionary()
totalNumberOfWords = 0

def dictoneryFile(file):
    counter = 0
    tFile = open(args.dataLocation + '/' + file, 'r')

    for line in tFile:
        for word in line.split():
            if word.startswith(args.ignoreStartingWith):
                continue
            globalDictionery.add_word(word)
            counter += 1
    tFile.close()
    return counter

if len(targateFiles) > 1:
    userInput = input("Multiple files founded. Continue? y or n.\n")
    if not (userInput == "yes" or userInput == 'y'):
        print("Exiting")
        exit(0)

print("Finding all the words and put in first dictionary")
for file in targateFiles:
    print("Reading from file: " + file)
    totalNumberOfWords += dictoneryFile(file)

print("Finding all the words and put in upgraded dictionary")
for file in targateFiles:
    print("Reading from file: " + file)
    tFile = open(args.dataLocation + '/' + file, 'r')
    for line in tFile:
        line = line.split()
        for i, k in zip(line,line[1:]):
            globalDictionery.add_next(i, k)
    tFile.close()

def prettyPrint(dict,file):
    for el in dict:
        file.write("** " + el + ": " + str(dict[el].number) + " " + str(dict[el].numberOfAppear) + "\n")
        for sub in dict[el].dict:
            file.write("--- " + sub + ": " + str(dict[el].dict[sub]) + "\n")

print("Printing summarized data to " + str(args.logFile))
logFile = open(args.logFile, 'w')
logFile.write("Dictionary length: " + str(len(globalDictionery.word2idx)) + "\n")
logFile.write("Total number of words: " + str(totalNumberOfWords) + "\n")
prettyPrint(globalDictionery.word2idx,logFile)
logFile.close()

print("Analyze done")
