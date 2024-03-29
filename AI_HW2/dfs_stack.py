import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    #initialize mystack(a stack implemented by list for DFS), mydict(a dictionary for recording the preceder of nodes),
    #myset(a set to check if a node is visited)
    path = []
    dist = 0
    num_visited = 0
    mystack = []
    mydict = {}
    myset = set()
    with open(edgeFile,newline='') as csvfile:
        rows1 = csv.reader(csvfile)
        rows = []
        #create a list rows for data in csvfile.
        for row in rows1:
            rows.append(row)
            
        mystack.append(start)         #put the start node in the stack.
        while len(mystack)!=0:        #DFS algorithm
            thisnode = mystack.pop()
            if end in mydict:         #if end is accessable, break.
                myset.add(end)
                break
            if thisnode in myset:     #if the node was visited,continue.
                continue
            else:
                myset.add(thisnode)   #mark thisnode as visited.
            
            first = False             #first is for the first row of csvfile.
            for row in rows:
                if not(first):
                    first = True
                    continue
                #put the nodes that are adjacent to thisnode into the stack.
                if int(row[0]) == thisnode and not(int(row[1]) in myset):
                    mystack.append(int(row[1]))
                    mydict[int(row[1])] = (int(row[0]),row[2])         
            
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
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
