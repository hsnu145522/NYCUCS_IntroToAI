import csv
import queue
edgeFile = 'edges.csv'


def bfs(start, end):
    path = []
    dist = 0
    num_visited = 0
    myqueue = queue.Queue()
    mydict = {}
    myset = set()
    with open(edgeFile,newline='') as csvfile:
        rows1 = csv.reader(csvfile)
        rows = []
        for row in rows1:
            rows.append(row)
        myqueue.put(start)
        
        while not(myqueue.empty()):
            thisnode = myqueue.get()
            if end in mydict:
                myset.add(end)
                break
            if thisnode in myset:
                continue
            else:
                pass
            first = False
            #print(rows)
            for row in rows:
                if not(first):
                    first = True
                    continue
                if int(row[0]) == thisnode and not(int(row[1]) in mydict):
                    myqueue.put(int(row[1]))
                    mydict[int(row[1])] = (int(row[0]),row[2])
                    
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
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
