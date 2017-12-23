###############################################################################
# Language Modeling
#
# This file complete broken sentences using the language model
#
###############################################################################

import argparse
from copy import deepcopy
import sys

import torch
from torch.autograd import Variable

import data

parser = argparse.ArgumentParser(description='PyTorch Language Model')

# Model parameters
parser.add_argument('--data', type=str, default='./data/penn',
                    help='location of the data corpus')
parser.add_argument('--checkpoint', type=str, default='./models/model_penn.pt',
                    help='model checkpoint to use')
parser.add_argument('--seed', type=int, default=1111,
                    help='random seed')
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--temperature', type=float, default=1.0,
                    help='temperature - higher will increase diversity')
args = parser.parse_args()

# Set the random seed manually for reproducibility
torch.manual_seed(args.seed)
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")
    else:
        torch.cuda.manual_seed(args.seed)

if args.temperature < 1e-3:
    parser.error("--temperature has to be greater or equal 1e-3")

# Opening the model to generate from
with open(args.checkpoint, 'rb') as f:
    model = torch.load(f)
model.eval()

if args.cuda:
    model.cuda()
else:
    model.cpu()

# Loading the data
corpus = data.Corpus(args.data)
ntokens = len(corpus.dictionary)
hidden = model.init_hidden(1)
word_input = Variable(torch.rand(1, 1).mul(ntokens).long(), volatile=True)
if args.cuda:
    word_input.data = word_input.data.cuda()

# Getting the beginning of the line to complete.
lineStart = input("Please enter the start of the line you want to complete:\n")
lineStart = lineStart.split()

# Adding all the words to the model.
for word in lineStart:
    try:
        word_input.data.fill_(corpus.dictionary.word2idx[word])
    except:
        print("Error at adding the word \"" + word + "\" to the model since its not in the dictionery")
        break

# Getting the number of word to complete
numOfWordsToComplete = int(input("Please enter the number of words you want to complete:\n"))

# Getting the end of the line to complete
lineEnd = input("Please enter the end of the line you want to complete:\n")
lineEnd = lineEnd.split()

# Current top 100 sentences to complete
top_100_sentences = []

# Getting the top 100 matches to the first word
# Getting the current output and hidden layers
output, hidden = model(word_input, hidden)
# Getting all the weights for all the words
word_weights = output.squeeze().data.div(args.temperature).exp().cpu()
# Getting the sorted vector of indexes of the top 100 words weights
word_indexes = torch.multinomial(word_weights, 100)

# Adding to the array objects that looks like: ([word index], word weight, the model after adding that word)
for idx in word_indexes:
    # Copping the model into temp
    temp = deepcopy(word_input)
    #  Adding to the copied model the next word predicted
    temp.data.fill_(idx)
    # Adding the object to the array
    top_100_sentences.append(([idx], word_weights[idx], temp))


# Helper function in order to sort the top sentences array by best weight
def get_key(item):
    return item[1]

# Completing the number of words we need to - 1 since we've already completed one word
for word_number in range(numOfWordsToComplete - 1):
    # Array of top 10000 sentences that was created
    top_10000_sentences = []
    # For each sentence we have we create 100 sentences then add them to the top 10000 array
    for sentence in top_100_sentences:
        output, hidden = model(sentence[2], hidden)
        word_weights = output.squeeze().data.div(args.temperature).exp().cpu()
        word_indexes = torch.multinomial(word_weights, 100)
        for idx in word_indexes:
            temp = deepcopy(sentence[2])
            temp.data.fill_(idx)
            top_10000_sentences.append((sentence[0] + [idx], word_weights[idx] + sentence[1], temp))
    # After we have 10000 sentences we put in the top 100 the best 100 of them
    top_100_sentences = sorted(top_10000_sentences, key=get_key, reverse=True)[0:100]

# For each word in the end add the weight that we should have got to the sentence and update the model
for word in lineEnd:
    # Makes sure the word really exist in dictionary and get its index
    try:
        curr_word_idx = corpus.dictionary.word2idx[word]
    except KeyError as e:
        print(e)
        print("Error at adding the word \"" + word + "\" to the model since its not in the dictionary")
        break
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    # For each sentence add the weight that the correct word got and update its model
    for num, sentence in enumerate(top_100_sentences):
        output, hidden = model(sentence[2], hidden)
        word_weights = output.squeeze().data.div(args.temperature).exp().cpu()
        temp = deepcopy(sentence[2])
        temp.data.fill_(curr_word_idx)
        top_100_sentences[num] = (sentence[0], sentence[1] + word_weights[curr_word_idx], temp)

print("\nThe top 10 possibilities for the sentence are: \n")

# Printing top 10
for el_num, el in enumerate(sorted(top_100_sentences, key=get_key, reverse=True)[0:10]):
    # Print number
    print(str(el_num + 1) + ") ", end="")
    # Printing the beginning of the line
    for word in lineStart:
        print(word, end=" ")
    # Printing the predictions
    for idx in el[0]:
        print(corpus.dictionary.idx2word[idx], end=" ")
    # Printing the end of the line
    for word in lineEnd:
        print(word, end=" ")
    # Printing the indexes of the words and the total weight
    print(",", el[0], ",", el[1])
