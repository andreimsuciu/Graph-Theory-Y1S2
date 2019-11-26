import queue

class Graph(object):
    def __init__(self):
        self.__in={}
        self.__out={}
        self.__cost={}
        self.__noVertices=0
        self.__noEdges=0
        #matrix for floyd-warshall
        self.__dist=[[],[]]
        #we need to have a list with all vertices for our topsort algorithm
        self.__vertices=[]
        
    def readFile(self,fileName):
        #fileName="graph.txt"
        try:
            f = open(fileName, "r")
            line = f.readline().strip()
            attrs = line.split(" ")
            self.__noVertices=int(attrs[0])
            self.__noEdges=int(attrs[1])
            line = f.readline().strip()
            while line != "":
                attrs = line.split(" ")
                origin=attrs[0]
                destination=attrs[1]
                cost=attrs[2]
                #putting all in the self.__out dict
                if origin not in self.__out:
                    self.__out[origin]=[]
                self.__out[origin].append(destination)
                #putting all in the self.__in dict
                if destination not in self.__in:
                    self.__in[destination]=[]
                self.__in[destination].append(origin)
                #putting all in the self.__cost dict
                edgeTuple=(origin,destination)
                if edgeTuple not in self.__cost:
                    self.__cost[edgeTuple]=0
                self.__cost[edgeTuple]=cost
                
                #putting all vertices in self.__vertices for the topsort algorithm
                if origin not in self.__vertices:
                    self.__vertices.append(origin)
                if destination not in self.__vertices:
                    self.__vertices.append(destination)
                
                line = f.readline().strip()
                
        except IOError as e:
            raise e
        finally:
            f.close()
            
    def getVerticesNum(self):
        return self.__noVertices
    
    def parseVertices(self):
        for y in self.__out:
            yield y
            
    def isEdge(self,origin,destination):
        if origin in self.__out:
            if destination in self.__out[origin]:
                return True
            else:
                return False
        else:
            return False
    
    def vertexDegree(self,vertex):
        in_deg=0
        out_deg=0
        if vertex in self.__in:
            in_deg=len(self.__in[vertex])
        if vertex in self.__out:
            out_deg=len(self.__out[vertex])
        if vertex not in self.__in and vertex not in self.__out:
            in_deg=-1
        return in_deg,out_deg
        
    def outboundEdges(self,vertex):
        if len(self.__out[vertex])==0:
            return 0
        else:
            for target in self.__out[vertex]:
                yield target
    
    def inboundEdges(self,vertex):
        if len(self.__in[vertex])==0:
            return False
        else:
            for target in self.__in[vertex]:
                yield target        
    
    def getCost(self,origin,destination):
        edgeTuple=(origin,destination)
        if edgeTuple in self.__cost:
            return self.__cost[edgeTuple]
        else:
            return False
    
    def setCost(self,origin,destination,newCost):
        edgeTuple=(origin,destination)
        if edgeTuple in self.__cost:
            self.__cost[edgeTuple]=newCost
            return True
        else:
            return False
        
    def addVertex(self,vertex):
        if vertex in self.__in or vertex in self.__out:
            return False
        self.__in[vertex]=[]
        self.__out[vertex]=[]
        self.__noVertices+=1
        return True
    
    def removeVertex(self,vertex):
        if vertex not in self.__in and vertex not in self.__out:
            return False
        for destination in self.__out[vertex]:
            self.__in[destination].remove(vertex)
            del self.__cost[(vertex,destination)]
        for origin in self.__in[vertex]:
            self.__out[origin].remove(vertex)
            del self.__cost[(origin,vertex)]    
        del self.__in[vertex]            
        del self.__out[vertex]
        self.__noVertices-=1
        return True
    
    def addEdge(self,origin,destination,cost):
        if origin not in self.__in or destination not in self.__out:
            return -1
        edgeTuple=(origin,destination)
        if edgeTuple in self.__cost:
            return -2
        self.__out[origin].append(destination)
        self.__in[destination].append(origin)
        self.__cost[edgeTuple]=cost
        self.__noEdges+=1
        return 0
    
    def removeEdge(self,origin,destination):
        if origin not in self.__in or destination not in self.__out:
            return -1
        edgeTuple=(origin,destination)
        if edgeTuple in self.__cost:
            del self.__cost[edgeTuple]
            self.__out[origin].remove(destination)
            self.__in[destination].remove(origin)
            self.__noEdges-=1
            return 0
        else:
            return -2
    
    def lowestLengthPath(self,vertexA, vertexB):
        '''
        Function that finds a lowest length path between two vertices, 
        by using a backward breadth-first search from the ending vertex
        in: graph, vertexA, vertexB -vertex
        out: listOfPath - list
        '''
        distance={}
        prev={}
        listOfPath=[]
        queueOfParents= queue.Queue(maxsize=self.__noVertices)
        visited=[vertexB]
        queueOfParents.put(vertexB)
        distance[vertexB]=0
        while not queueOfParents.empty():
            vertex=queueOfParents.get()
            try:   
                for neighbor in self.__in[vertex]:
                    if neighbor not in visited:
                        prev[neighbor]=vertex
                        distance[neighbor]=distance[vertex] +1
                        if neighbor == vertexA:
                            listOfPath.append(neighbor)
                            dist=distance[neighbor]
                            preVertex=prev[neighbor]
                            dist -=1
                            while dist!=0:
                                dist-=1
                                listOfPath.append(preVertex)
                                preVertex=prev[preVertex]
                            listOfPath.append(vertexB)
                            return listOfPath
                        queueOfParents.put(neighbor)
                        visited.append(neighbor)
            except KeyError:
                continue
        return listOfPath   
    
    def fwAlg(self):
        self.__dist = [ [ 0 for i in range(self.__noVertices) ] for j in range(self.__noVertices) ]
        for i in range(self.__noVertices):
            for j in range(self.__noVertices):
                if i == j:
                    self.__dist[i][j]=0
                else:
                    self.__dist[i][j]=999
        for vertex in self.__out:
            for neighbour in self.__out[vertex]:
                edgeTuple=(vertex,neighbour)
                vertex_int=int(vertex)
                neighbour_int=int(neighbour)
                self.__dist[vertex_int][neighbour_int]=int(self.__cost[edgeTuple])
        for k in range(self.__noVertices):
            for i in range(self.__noVertices):
                for j in range(self.__noVertices):
                    if self.__dist[i][j]>self.__dist[i][k] + self.__dist[k][j]:
                        self.__dist[i][j]=self.__dist[i][k] + self.__dist[k][j]
        #
    def lowestCostWalk(self,vertexA,vertexB):
        vertexA_int=int(vertexA)
        vertexB_int=int(vertexB)
        return self.__dist[vertexA_int][vertexB_int]
    
    def topSort(self):
        '''
        For this topological sort, I will use the predecessor counting algorithm
        Input:    G : directed graph
        Output:   sortedList : a list of vertices in topological sorting order, or empty list if G has cycles
        '''
        sortedList=[]
        q=queue.Queue(maxsize=self.__noVertices)
        count={}
        
        for vertex in self.__vertices:
            
            if vertex not in self.__in:
                count[vertex] = 0
                q.put(vertex)
            else:
                i=0
                for target in self.__in[vertex]:
                    i+=1
                count[vertex]=i 
        
        while not q.empty():
            vertex=q.get()
            sortedList.append(vertex)
            try:
                for auxVertex in self.__out[vertex]:
                    count[auxVertex]-=1
                    if count[auxVertex]==0:
                        q.put(auxVertex)
            except KeyError:
                continue
        if len(sortedList) < self.__noVertices:
            sortedList=[]
            
        return sortedList
    
    def highestCostWalk(self,origin,destination):
        '''
        finding the highest cost walk in a DAG
        returns path-list of the path between origin and destination, 
                cost-int, cost of walk
        '''
        topSortList=self.topSort()
        print(topSortList)
        if len(topSortList)==0:
            return [],-9999
        #here we keep the cost to each vertex from our given origin
        cost=[]
        #here we keep each parent vertex for the current vertex
        prev=[] 
        for i in range(len(topSortList)):
            cost.append(-999)
            prev.append(-1)
        cost[int(origin)]=0
        for vertex in topSortList:
            try:
                for neighbour in self.__out[vertex]:
                    edgeTuple=(vertex,neighbour)
                    if cost[int(neighbour)]<cost[int(vertex)]+int(self.__cost[edgeTuple]):
                        cost[int(neighbour)]=cost[int(vertex)]+int(self.__cost[edgeTuple])
                        prev[int(neighbour)]=int(vertex)
            except KeyError:
                continue
        
        #here we build the path
        path=[]
        currentVertex=int(destination)
        path.append(currentVertex)
        while(prev[currentVertex]!=int(origin)):
            path.append(prev[currentVertex])
            currentVertex=prev[currentVertex]
        path.append(int(origin))
        path.reverse()
        return path,cost[int(destination)]  