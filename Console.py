import copy 
class Console(object):
    def __init__(self,Graph):
        self.__graph=Graph
        
    def printMenu(self):
        print ("Possible commands:")
        print ("0.number vertices")
        print ("1.print vertices")
        print ("2.isEdge <origin> <destination>")
        print ("3.degree <vertex>")
        print ("4.outbound <vertex>")
        print ("5.inbound <vertex>")
        print ("6.get cost <origin><destination>")
        print ("7.set cost <origin><destination><newCost>")
        print ("8.addVertex <vertex>")
        print ("9.remVertex <vertex>")
        print ("10.addEdge <origin><destination><cost>")
        print ("11.remEdge <origin><destination>")
        print ("12.copy graph")
        print ("13.NEW FEATURE: getPath<vertexA><vertexB>")
        print ("14.EVEN NEWER FEATURE:lowestWalk<vertexA><vertexB>")
        print ("15.NEWER THAN EVER BEFORE FEATURES:")
        print ("\t15.1.is DAG")
        print ("\t15.2.highestWalk<vertexA><vertexB>")
        print ("help")
        print ("exit\n")  
        
    def run(self):
        print("Welcome to best directed graph ever!")
        x=True
        while x:
            cmd = input("Please input file name:")
            try:
                self.__graph.readFile(cmd)
                x=False
            except UnboundLocalError:
                print("incorrect file name!")
        #UNCOMMENT THE LINE BELOW FOR FLOYD-WARSHALL, disabled for complexity reasons.
        #self.__graph.fwAlg()
        self.__graph.topSort()
        self.printMenu()
        commands={"print":self.__uiPrintVertices, "isEdge":self.__uiIsEdge, "degree":self.__uiDegree, "outbound":self.__uiOutBound, "inbound":self.__uiInBound, "get":self.__uiGetCost, "set":self.__uiSetCost, "addVertex":self.__uiAddVertex, "remVertex":self.__uiRemoveVertex, "addEdge":self.__uiAddEdge, "remEdge":self.__uiRemoveEdge, "copy":self.__uiGraphCopy, "number":self.__uiNumberVertices, "getPath":self.__uiGetPath, "lowestWalk":self.__uiLowestWalk, "is":self.__uiIsDAG, "highestWalk":self.__uiHighestWalk}
        while True:
            cmd = input(">>")
            params = cmd.split()
            if cmd == "exit":
                return
            elif cmd == "help":
                self.printMenu()
            elif params[0] in commands:
                try:
                    commands[params[0]](params[1:])
                except ValueError:
                    print("invalid numeric value given!")
                except IndexError:
                    print("invalid command!")
            else:
                print("invalid command!")
    
    def __uiPrintVertices(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return
        
        for i in self.__graph.parseVertices():
            print(i)
            
    def __uiNumberVertices(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return
        
        x=self.__graph.getVerticesNum()
        print(x)
    
    def __uiIsEdge(self,params):
        if len(params)!=2:
            print("invalid no of params!")
            return
        
        origin=params[0]
        destination=params[1]
        if self.__graph.isEdge(origin,destination):
            print(str(origin) + ":" + str(destination) + " is an edge")
        else:
            print(str(origin) + ":" + str(destination) + " is NOT an edge")
            
    def __uiDegree(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return 
        
        vertex=params[0]
        in_deg,out_deg=self.__graph.vertexDegree(vertex)
        if in_deg==-1:
            print("Vertex does not exist!")
        else:
            print("The in degree of vertex " + str(vertex) + " is:" + str(in_deg) + " and the out degree is:" + str(out_deg))
    
    def __uiOutBound(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return 
        
        vertex=params[0]
        result = self.__graph.outboundEdges(vertex)
        if result == 0:
            print("No outbound edges!")
        else:
            for result in self.__graph.outboundEdges(vertex):
                print (result)      
    
    def __uiInBound(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return 
        
        vertex=params[0]
        result = self.__graph.inboundEdges(vertex)
        if result == False:
            print("No inbound edges!")
        else:
            for result in self.__graph.inboundEdges(vertex):
                print (result)     
                  
    def __uiGetCost(self,params):
        if len(params)!=3:
            print("invalid no of params!")
            return
        
        origin=params[1]
        destination=params[2]
        result=self.__graph.getCost(origin,destination)
        if result == False:
            print("Edge does not exist!")
        else:
            print("Cost is: " + str(result))
            
    def __uiSetCost(self,params):
        if len(params)!=4:
            print("invalid no of params!")
            return
        
        origin=params[1]
        destination=params[2]
        cost=params[3]
        result=self.__graph.setCost(origin,destination,cost)
        if result == False:
            print("Edge does not exist, so we cannot set the cost!")
        else:
            print("New cost set!")
            
    def __uiAddVertex(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return
        vertex=params[0]
        result=self.__graph.addVertex(vertex)
        if result:
            print("Vertex added!")
        else:
            print("Vertex already exists!")
    
    def __uiRemoveVertex(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return
        vertex=params[0]
        result=self.__graph.removeVertex(vertex)
        if result:
            print("Vertex removed!")
        else:
            print("Vertex does not exist!")
            
    def __uiAddEdge(self,params):
        if len(params)!=3:
            print("invalid no of params!")
            return
        origin=params[0]
        destination=params[1]
        cost=params[2]
        
        result=self.__graph.addEdge(origin,destination,cost)
        if result == -1:
            print("One of the vertices does not exist!")
        elif result == -2:
            print("Edge already exists!")  
        elif result == 0:
            print("Edge added!")     
    
    def __uiRemoveEdge(self,params):
        if len(params)!=2:
            print("invalid no of params!")
            return
        origin=params[0]
        destination=params[1]
        
        result=self.__graph.removeEdge(origin,destination)
        if result == -1:
            print("One of the vertices does not exist!")
        elif result == -2:
            print("Edge does not exist!")  
        elif result == 0:
            print("Edge removed!")
    
    def __uiGraphCopy(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return
        graphCopy = copy.deepcopy(self.__graph)
        print(graphCopy)
    def __uiGetPath(self,params):
        if len(params)!=2:
            print("invalid no of params!")
            return
        vertexA=params[0]
        vertexB=params[1]
        listOfPath=[]
        listOfPath=self.__graph.lowestLengthPath(vertexA,vertexB)
        result=len(listOfPath)
        result-=1
        if result == -1:
            print("No path for the given vertices")
        else:
            print("The minimum length path in reverse BFS is: " + str(result) + " with the path:" +str(listOfPath))
    
    def __uiLowestWalk(self,params):
        if len(params)!=2:
            print("invalid no of params!")
            return
        vertexA=params[0]
        vertexB=params[1]
        
        result=self.__graph.lowestCostWalk(vertexA,vertexB)
        if result == 999:
            print("There is no path!")
        elif result == 0:
            print("The path between the same vertices is 0!")
        else:
            print("The path between " + vertexA + " and " + vertexB + " is " +str(result) )
            
    def __uiIsDAG(self,params):
        if len(params)!=1:
            print("invalid no of params!")
            return
        
        l=self.__graph.topSort()
        if len(l)==0:
            print("The given graph is NOT a DAG")
        else:
            print("The given graph IS a DAG")
                    
    def __uiHighestWalk(self,params):        
        if len(params)!=2:
            print("invalid no of params!")
            return
        vertexA=params[0]
        vertexB=params[1]
        l,cost=self.__graph.highestCostWalk(vertexA,vertexB)
        if cost==-9999:
            print("The given graph is NOT a DAG")
        elif cost==-999:
            print("no path")
        else:
            print("The highest cost between "+vertexA+" and "+vertexB+" is "+ str(cost)+" and the path is:")
            for i in l:
                print(i, end=" ")    
            print("")
            
            
            
            
            
            
            
            
            
                