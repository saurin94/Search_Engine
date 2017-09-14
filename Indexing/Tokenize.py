import re
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer

# Get stopwords from List provided
f = open("stoplist.txt", "r")
stopList = f.read().split("\n")
f.close()

ps = PorterStemmer()


# sn = SnowballStemmer("english")

class Tokenize(object):
    global exclude
    global table
    global ps, stopList

    def tokenizeText(self, data, docId, wordDictWithOffset, positionNew, vocab):
        # Text Preprocessing
        data = re.sub("/('ll|'LL|'re|'RE|'ve|'VE|n't|N'T)/g", " $1 ", data)
        data = re.sub("[^\w\s\.\-\{\}\(\)\[\]]", ' ', data)
        data = re.sub("[\\]\\[\\(\\)\\{\\}<>]", " ", data)
        data = re.sub("(?![.])\\p{Punct}", " ", data)
        data = re.sub("([^\\w.\\d]|(?!\\w)\\.(?!\\w))+", " ", data)
        data = re.sub("'([sSmMdD])", "", data)
        data = data.lower().replace("_", " ")
        text = data
        wordList = []
        textSplit = text.split()
        # Iterate over each word in text
        # for each_word in textSplit:
        #     if each_word not in stopList:
        #         word = ps.stem(each_word)
        #     # wordList.append(each_word)
        #     # vocab.add(each_word)
        for each_word in textSplit:
            if each_word not in stopList:
                word = ps.stem(each_word)
                wordList.append(word)
                vocab.add(word)
        # Make dictionary for each file and then write it to file
        for each_word in wordList:
            dict = {}
            if each_word in wordDictWithOffset:
                if docId in wordDictWithOffset[each_word]:
                    wordDictWithOffset[each_word][docId] += [positionNew]
                else:
                    wordDictWithOffset[each_word][docId] = [positionNew]
            else:
                dict[docId] = [positionNew]
                wordDictWithOffset[each_word] = dict
            positionNew += 1

        return wordDictWithOffset
