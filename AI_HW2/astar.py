import csv
from heapq import *
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    path = []
    dist = 0
    num_visited = 0
    h_distance = {}
    myqueue = []
    mydict = {}
    myset = set()
    with open(heuristicFile, newline='') as csvfile:
        rows1 = csv.reader(csvfile)
        first = False
        for row in rows1:
            if not(first):
                first = True
                continue
            h_distance[int(row[0])] = float(row[1]) #row[i] task[i] for i=1,2,3
    with open(edgeFile,newline='') as csvfile:
        rows1 = csv.reader(csvfile)
        rows = []
        for row in rows1:
            rows.append(row)
        
        heappush(myqueue,(0,start))
        while not(len(myqueue)==0):
            thisdist, thisnode = heappop(myqueue)
            if end in mydict:
                myset.add(end)
                break
            if thisnode in myset:
                continue
            else:
                pass
            first = False
            for row in rows:
                if not(first):
                    first = True
                    continue
                if int(row[0]) == thisnode and not(int(row[1]) in mydict):
                    heappush(myqueue,(float(row[2])+thisdist+h_distance[int(row[1])],int(row[1])))
                    mydict[int(row[1])] = (int(row[0]),row[2])
                if end in mydict:
                    break
                    
            myset.add(thisnode)
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
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
