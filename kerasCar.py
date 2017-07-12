import urllib
import re
import numpy
import math

link = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
f = urllib.urlopen(link)

list = []
counter = 0
page = f.read()
page = re.sub('\s\s+',' ',page)
page = page.split('\n')
page.remove('')
for el in page:
    tmp = el.split(' ')
    if (tmp[3] != '?'):
        tmp[7] = tmp[7][0]
        tmp = tmp[:8]
        tmp[4] = tmp[4][:4]
        list.append([tmp[0],tmp[1:]])

step_size = input("Please enter a step size")
Weights = []
Weights = numpy.random.randn(7) / math.sqrt(7)
