from __future__ import print_function

import torch
import torch.autograd

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
        r = []
        for a in tmp:
            r.append(float(a))
        data.append([r[0], r[1:]])

print(data)
print(len(data))

def disp(W,b):
    outString = "y = "
    for i in range(0,7):
        outString += (str(W[i]) + " * X" + str(i + 1) + " + ")
    outString += str(b).replace("\n"," ")
    return outString
batch_size = 4
def get_batch(count):

    x = torch.Tensor(batch_size,7)
    y = torch.Tensor(batch_size,1)
    for i in range(0, batch_size):
        y[i] = data[count + i][0]
        x[i] = torch.Tensor(data[count + i][1])
    return Variable(x), Variable(y)

fc = torch.nn.Linear(7, 1)
loss = 0

counter = 0
while True:
    # Get data
    batch_x, batch_y = get_batch(counter)
    counter += batch_size

    # Reset gradients
    fc.zero_grad()

    # Forward pass
    h = fc(batch_x) - batch_y

    for a in h:
        a = a * a

    output = torch.mean(h)
    loss = output

    # Backward pass
    output.backward()

    # Apply gradients
    for param in fc.parameters():
        param.data.add_(-0.01 * param.grad.data)

    # Stop criterion
    if loss < 1e-3 or counter == 320 :
        break

print('Loss: ' + str(loss))
print('==> Learned function: ' + disp(fc.weight.data.view(-1), fc.bias.data))
