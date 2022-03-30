import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    path = []
    dist = 0
    num_visited = 0
    mystack = []
    mydict = {}
    myset = set()
    with open(edgeFile,newline='') as csvfile:
        rows1 = csv.reader(csvfile)
        rows = []
        for row in rows1:
            rows.append(row)
        mystack.append(start)

        while len(mystack)!=0:
            thisnode = mystack.pop()
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
                if int(row[0]) == thisnode and not(int(row[1]) in myset):
                    mystack.append(int(row[1]))
                    mydict[int(row[1])] = (int(row[0]),row[2])         
            myset.add(thisnode)
            #print(thisnode)
        print("Done with DFS.")
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
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
