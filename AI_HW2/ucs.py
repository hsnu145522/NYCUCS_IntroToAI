import csv
from heapq import *
edgeFile = 'edges.csv'


def ucs(start, end):
    path = []
    dist = 0
    num_visited = 0
    myqueue = []
    mydict = {}
    myset = set()
    with open(edgeFile,newline='') as csvfile:
        rows1 = csv.reader(csvfile)
        rows = []
        for row in rows1:
            rows.append(row)
                
        heappush(myqueue,(0,start))
        while not(len(myqueue)==0):
            thisdist, thisnode = heappop(myqueue)

            if thisnode in myset:
                continue
            else:
                myset.add(thisnode)
                if end in myset:
                    #print("ends.")
                    break
            
            first = False

            for row in rows:
                if not(first):
                    first = True
                    continue
                if int(row[0]) == thisnode and not(int(row[1]) in myset):
                    heappush(myqueue,(float(row[2])+thisdist,int(row[1])))
                    if int(row[1]) in mydict:
                        temp = mydict[int(row[1])]
                        if temp[2]>float(row[2])+thisdist:
                            mydict[int(row[1])] = (int(row[0]),row[2],float(row[2])+thisdist)
                    else:
                        mydict[int(row[1])] = (int(row[0]),row[2],float(row[2])+thisdist)
                    
            
            #print(thisnode," ,done.")
    path.append(end)
    nownode = end
    while nownode != start:
        nownode,thisdist = mydict[nownode][0],mydict[nownode][1]
        path.append(nownode)
        dist+=float(thisdist)
    path1 = []
    for i in path:
        path1.insert(0,i)
    num_visited = len(myset)
    return path1, dist, num_visited


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
