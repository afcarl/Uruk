#!/bin/bash
python3 main.py --logDataFile "./logs/log2" --nhid 64 --nlayers 2 --lr 20 --dropout 0.2
python3 main.py --logDataFile "./logs/log3" --nhid 128 --nlayers 2 --lr 20 --dropout 0.2
python3 main.py --logDataFile "./logs/log4" --nhid 256 --nlayers 2 --lr 20 --dropout 0.2
python3 main.py --logDataFile "./logs/log5" --nhid 64 --nlayers 4 --lr 20 --dropout 0.2
python3 main.py --logDataFile "./logs/log6" --nhid 128 --nlayers 4 --lr 20 --dropout 0.2
python3 main.py --logDataFile "./logs/log7" --nhid 128 --nlayers 2 --lr 20 --dropout 0.1
python3 main.py --logDataFile "./logs/log8" --nhid 128 --nlayers 2 --lr 20 --dropout 0.3
python3 main.py --logDataFile "./logs/log9" --nhid 128 --nlayers 2 --lr 10 --dropout 0.2
