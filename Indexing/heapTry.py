import heapq

# t1 = [9, 34, 141, 162, 173, 188, 191, 211, 226, 232, 252, 305, 315, 323, 328]
# t2 = [44, 144, 164, 187, 219, 231, 277]
# t3 = [2, 20, 55, 57, 73, 107, 136, 139, 284, 294, 308, 312, 342]
# t1 = [193, 216]
# t2 = [11, 20, 143]
# t3 = [35, 92, 102]
# h = []
# rangeheap = []
# flag1 = 1
# flag2 = 1
# flag3 = 1
# heapq.heappush(h, t1[0])
# heapq.heappush(h, t2[0])
# heapq.heappush(h, t3[0])
# while (len(t1) >= 1 and len(t2) >= 1 and len(t3) >= 1):
#     if flag1 == 0:
#         heapq.heappush(h, t1[0])
#     if flag2 == 0:
#         heapq.heappush(h, t2[0])
#     if flag3 == 0:
#         heapq.heappush(h, t3[0])
#     largest = heapq.nlargest(1, h)[0]
#     smallest = heapq.nsmallest(1, h)[0]
#     range = largest - smallest
#     heapq.heappush(rangeheap, range)
#     heapq.heappop(h)
#     if smallest in t1:
#         t1.remove(smallest)
#         flag1 = 0
#         flag2 = 1
#         flag3 = 1
#     elif smallest in t2:
#         t2.remove(smallest)
#         flag2 = 0
#         flag3 = 1
#         flag1 = 1
#     elif smallest in t3:
#         t3.remove(smallest)
#         flag3 = 0
#         flag2 = 1
#         flag1 = 1
# print heapq.nsmallest(1, rangeheap)[0]
# if termInDoc == 1:
#     finalDocIdMap[docId] = 2 * C
# elif termInDoc == 2:
#     t1 = termstat[0].positions
#     t2 = termstat[1].positions
#     h = []
#     rangeheap = []
#     flag1 = 1
#     flag2 = 1
#     heapq.heappush(h, t1[0])
#     heapq.heappush(h, t2[0])
#     while (len(t1) >= 1 and len(t2) >= 1):
#         if flag1 == 0:
#             heapq.heappush(h, t1[0])
#         if flag2 == 0:
#             heapq.heappush(h, t2[0])
#         largest = heapq.nlargest(1, h)[0]
#         smallest = heapq.nsmallest(1, h)[0]
#         range = largest - smallest
#         heapq.heappush(rangeheap, range)
#         heapq.heappop(h)
#         if smallest in t1:
#             t1.remove(smallest)
#             flag1 = 0
#             flag2 = 1
#         elif smallest in t2:
#             t2.remove(smallest)
#             flag2 = 0
#             flag1 = 1
#     finalDocIdMap[docId] = heapq.nsmallest(1, rangeheap)[0] + 1 * C
# elif termInDoc == 3:
#     t1 = termstat[0].positions
#     t2 = termstat[1].positions
#     t3 = termstat[2].positions
#     h = []
#     rangeheap = []
#     flag1 = 1
#     flag2 = 1
#     flag3 = 1
#     heapq.heappush(h, t1[0])
#     heapq.heappush(h, t2[0])
#     heapq.heappush(h, t3[0])
#     while (len(t1) >= 1 and len(t2) >= 1 and len(t3) >= 1):
#         if flag1 == 0:
#             heapq.heappush(h, t1[0])
#         if flag2 == 0:
#             heapq.heappush(h, t2[0])
#         if flag3 == 0:
#             heapq.heappush(h, t3[0])
#         largest = heapq.nlargest(1, h)[0]
#         smallest = heapq.nsmallest(1, h)[0]
#         range = largest - smallest
#         heapq.heappush(rangeheap, range)
#         heapq.heappop(h)
#         if smallest in t1:
#             t1.remove(smallest)
#             flag1 = 0
#             flag2 = 1
#             flag3 = 1
#         elif smallest in t2:
#             t2.remove(smallest)
#             flag2 = 0
#             flag3 = 1
#             flag1 = 1
#         elif smallest in t3:
#             t3.remove(smallest)
#             flag3 = 0
#             flag2 = 1
#             flag1 = 1
#     finalDocIdMap[docId] = heapq.nsmallest(1, rangeheap)[0]

# f = {1: [212], 2: [9, 82, 150, 183, 189], 3: [8, 222]}
# f = {1: [335], 2: [334, 343], 3: [20, 316]}
# f = {1: [14, 22, 64, 89, 145, 149, 160, 232, 408, 636], 2: [13, 88, 93, 189, 206, 304, 388, 402, 450, 453, 524, 532, 535]}
# f = {1: [0,5,10,15] , 2:[1,3,6,14], 3:[4,8,15,21]}
# f = {1: [53, 130]}
f = {1: [121], 2: [43, 82]}
# f = {1: [121]}
a = 0
array = []
flags = []
for key,value in f.iteritems():
    array.append(value)
    a+=len(value)
    flags.append(1)
print a
h = []
rangeheap = []
for termArray in array:
    heapq.heappush(h,termArray[0])
while a>0:
    for flag in flags:
        if flag == 0:
            index = flags.index(flag)
            heapq.heappush(h,array[index][0])
    largest = heapq.nlargest(1, h)[0]
    smallest = heapq.nsmallest(1, h)[0]
    range = largest - smallest
    heapq.heappush(rangeheap, range)
    heapq.heappop(h)
    indexFlag = 0
    indexGet = 0
    for termArray in array:
        if smallest in termArray:
            termArray.remove(smallest)
            termArray.append(smallest)
            indexGet = indexFlag
        indexFlag+=1
    i = 0
    while i != len(flags):
        if i == indexGet:
            flags[i] = 0
        else:
            flags[i] = 1
        i+=1
    a-=1
print heapq.nsmallest(1, rangeheap)[0]




