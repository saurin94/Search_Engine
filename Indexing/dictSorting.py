d = {u'54': [88], u'32': [48], u'20': [37], u'25': [9], u'70': [71, 198]}
s = sorted(d.items(),key=lambda x: (len(x[1])),reverse=True)
print s
newdict = {}
string2 = ""
df= 0
cf = 0
tf = 0
for i in s:
    tf = len(i[1])
    df += 1
    cf += len(i[1])
    string2+=str(i[0])+":"+str(i[1]).replace("]","").replace("[","").replace(" ","")+"-"+str(tf)+";"
string1=str(df)+","+str(cf)+"="
print string1+string2
