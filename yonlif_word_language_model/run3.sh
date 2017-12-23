#!/bin/bash
python3 main.py --logDataFile "./logs/log10.1" --nhid 300 --nlayers 2 --lr 20 --dropout 0.2 --save "./models/model10.pt"
python3 main.py --logDataFile "./logs/log11.1" --nhid 400 --nlayers 2 --lr 20 --dropout 0.2 --save "./models/model11.pt"
python3 main.py --logDataFile "./logs/log12.1" --nhid 500 --nlayers 2 --lr 20 --dropout 0.2 --save "./models/model12.pt"
