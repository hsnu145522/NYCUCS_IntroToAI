import csv
from heapq import *
edgeFile = 'edges.csv'


def ucs(start, end):
    #initialize myqueue(a priority_queue implemented by list+heapq functions for UCS),
    #mydict(a dictionary for recording the preceder of nodes),
    #myset(a set to check if a node is visited).
    path = []
    dist = 0
    num_visited = 0
    myqueue = []
    mydict = {}
    myset = set()
    with open(edgeFile,newline='') as csvfile:
        rows1 = csv.reader(csvfile)
        rows = []
        #create a list rows for data in csvfile.
        for row in rows1:
            rows.append(row)
                
        heappush(myqueue,(0,start))               #put the start node in the queue.
        while not(len(myqueue)==0):               #UCS algorithm
            thisdist, thisnode = heappop(myqueue)
            if thisnode in myset:                 #if the node was visited,continue.
                continue
            else:
                myset.add(thisnode)               #mark thisnode as visited.
                if end in myset:                  #if end is accessable, break.
                    break
            
            first = False                         #first is for the first row of csvfile.
            for row in rows:
                if not(first):
                    first = True
                    continue
                if int(row[0]) == thisnode and not(int(row[1]) in myset):
                    #put the nodes that are adjacent to thisnode into the priority_queue.
                    #In order to let heap work properly, store information in tuples.
                    #Store information as (distance from start to int(row[1]), int(row[1])).
                    heappush(myqueue,(float(row[2])+thisdist,int(row[1])))
                    if int(row[1]) in mydict:
                        temp = mydict[int(row[1])]
                        #If there is a way nearier than the former one, update it.
                        #It's ok to not delete the information in the priority queue,
                        #since, nearier ones will be pop out earlier.
                        if temp[2]>float(row[2])+thisdist:
                            mydict[int(row[1])] = (int(row[0]),row[2],float(row[2])+thisdist)
                    else:
                        mydict[int(row[1])] = (int(row[0]),row[2],float(row[2])+thisdist)
    '''
    Last part is to trace back from the end node.
    Record the distance in dist and the path at list path.
    Reverse the list order.
    record the number of visited nodes in num_visited, which is the length of myset.
    '''
    path.append(end)
    nownode = end
    while nownode != start:
        nownode,thisdist = mydict[nownode][0],mydict[nownode][1]
        path.append(nownode)
        dist+=float(thisdist)
    path.reverse()
    num_visited = len(myset)
    return path, dist, num_visited


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
