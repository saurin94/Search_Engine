import re

data = "10. ill u.s.a hello. j.j.s 192.168.0.1. kaise.ho"
data = re.sub("/('ll|'LL|'re|'RE|'ve|'VE|n't|N'T)/g", " ", data)
data = re.sub("[^\w\s\.\-\{\}\(\)\[\]]", ' ', data)
data = re.sub("[\\]\\[\\(\\)\\{\\}<>]", " ", data)
data = re.sub("(?![.])\\p{Punct}", " ", data)
data = re.sub("([^\\w.\\d]|(?!\\w)\\.(?!\\w))+", " ", data)
data = re.sub("'([sSmMdD])", "", data)
data = data.lower().replace("_", " ")
print data
