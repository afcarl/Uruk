from __future__ import print_function

import torch.autograd
import torch.optim as optim

from torch.autograd import Variable

import re
import urllib.request

f = urllib.request.urlopen("http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
page = (f.read()).decode("utf-8")

data = []
counter = 0

page = re.sub('\s\s+',' ',page)
page = page.split('\n')
del page[-1]
for el in page:
    tmp = el.split(' ')
    if (tmp[3] != '?'):
        tmp[7] = tmp[7][0]
        tmp = tmp[:8]
        tmp[4] = tmp[4][:4]
        for a in range(0,8):
            tmp[a] = float(tmp[a])
        data.append(tmp)
data = torch.Tensor(data)

print("Data:")
print(data)
print(len(data))

divData = torch.Tensor(8)
meanData = torch.Tensor(8)
for a in range(0,8):
    num = torch.mean(data[:,a])
    data[:,a] -= num
    meanData[a] = num
    num = torch.std(data[:,a])
    data[:,a] /= num
    divData[a] = num

print(data)

def disp(W,b):
    outString = "y = "
    for i in range(0,7):
        outString += (str(W[i]) + " * X" + str(i + 1) + " + ")
    outString += str(b).replace("\n"," ")
    return outString

batch_size = 4
def get_batch(count):
    x = data[count:count+batch_size, 1:]
    y = data[count:count+batch_size, 0]
    return Variable(x), Variable(y)

fc = torch.nn.Linear(7, 1)

print("Weights:")
print(fc.weight)

numberOfBatches = 80
epoc = 0
numberOfEpocs = 5
counter = 0
optimizer = optim.Adam(fc.parameters(), lr=0.001)
while True:
    # Get data
    batch_x, batch_y = get_batch(counter)
    counter += batch_size

    # Reset gradients
    optimizer.zero_grad()

    # Forward pass
    loss = torch.mean((fc(batch_x) - batch_y).pow(2))

    # Backward pass
    loss.backward()

    # Apply gradients
    optimizer.step()

    # Stop criterion
    if counter == numberOfBatches*batch_size:
        counter = 0
        epoc += 1
        print("Loss in epoc " + str(numberOfEpocs) + ": " +str(loss))
        if epoc == numberOfEpocs:
            break

a = loss[0]
print(loss[0][0])
print('Loss: ' + str(loss[0]) + " After " + str(numberOfBatches) + " batches")
print('==> Learned function: ' + disp(fc.weight.data.view(-1), fc.bias.data.view(-1)))
'''
help = []
for a in range(0,7):
    help.append(fc.weight.data.view(-1)[a] * divData[a] + meanData[a])
print('==> Actual function ' + disp(help, fc.bias.data))
'''
