from termcolor import colored
from queue import PriorityQueue

hash_stats = []
dict_stats = []

class State :

    def __init__(self, cells, parent = None, weight = 0) :
        self.cells = cells
        self.countOfNextStats = 0
        self.parent = parent
        self.weight = weight

    def nextState(self) :
        stats = []
        for i,row in enumerate(self.cells) :
            for j,col in enumerate(row) :
                if(col[0] == -1) :
                    listOfCanMoves = self.canMove(i,j)
                    if(listOfCanMoves != []) :
                        stats.extend(listOfCanMoves)
        return stats
                    

    def canMove(self, i, j) :
        list = []
        # left
        l = j - 1
        if(l > -1) :
            if(self.cells[i][l][1] == 2) :
                el = self.move(i,l,i,j,1)
                list.append(el)
                self.countOfNextStats += 1
                # if(self.cells[i][l][0] == 0) :
                #     print(colored(f"{self.countOfNextStats} - Move The Main Car To Right.", 'red'))
                # else :
                #     print(f"{self.countOfNextStats} - Move The Car Number {self.cells[i][l][0]} To Right.")

        # right
        r = j + 1
        if(r < 7) :
            if(self.cells[i][r][1] == 2) :
                el = self.move(i,r,i,j,2)
                list.append(el)
                self.countOfNextStats += 1
                # if(self.cells[i][r][0] == 0) :
                #     print(colored(f"{self.countOfNextStats} - Move The Main Car To Left.", 'red'))
                # else :
                #     print(f"{self.countOfNextStats} - Move The Car Number {self.cells[i][r][0]} To Left.")

        # top
        t = i - 1
        if(t > -1) :
            if(self.cells[t][j][1] == 1) :
                el = self.move(t,j,i,j,3)
                list.append(el)
                self.countOfNextStats += 1
                # print(f"{self.countOfNextStats} - Move The Car Number {self.cells[t][j][0]} To Bottom.")

        # Bottom
        d = i + 1
        if(d < 5) :
            if(self.cells[d][j][1] == 1) :
                el = self.move(d,j,i,j,4)
                list.append(el)
                self.countOfNextStats += 1
                # print(f"{self.countOfNextStats} - Move The Car Number {self.cells[d][j][0]} To Top.")
    
        return list

    def move(self, xFrom, yFrom, xTo, yTo, dir) :
        newArr = self.copy()
        # left
        if(dir == 1) :
            if(newArr[xFrom][yFrom][0] == 0) :
                newArr[xTo][yTo] =  newArr[xFrom][yFrom]
                newArr[xFrom][yFrom - 2] = [-1,-1]
            else :
                newArr[xTo][yTo] =  newArr[xFrom][yFrom]
                newArr[xFrom][yFrom - 1] = [-1,-1]

        # right
        elif(dir == 2) :
            if(newArr[xFrom][yFrom][0] == 0) :
                newArr[xTo][yTo] =  newArr[xFrom][yFrom]
                newArr[xFrom][yFrom + 2] = [-1,-1]
            else :
                newArr[xTo][yTo] =  newArr[xFrom][yFrom]
                newArr[xFrom][yFrom + 1] = [-1,-1]

        # top
        elif(dir == 3) :
            newArr[xTo][yTo] =  newArr[xFrom][yFrom]
            newArr[xFrom - 1][yFrom] = [-1,-1]
        
        # bottom
        elif(dir == 4) :
            newArr[xTo][yTo] =  newArr[xFrom][yFrom]
            newArr[xFrom + 1][yFrom] = [-1,-1]

        
        return State(newArr, self, self.weight + 1)

    def generate_key(self) :
        list = []
        for row in self.cells :
            for col in row :
                list.append(str(col[0]))

        return "".join(list)


    def copy(self) :
        listall = []
        for row in self.cells :
            list = []
            for col in row :
                list.append(col.copy())
            listall.append(list)

        return listall

    def displayState(self) :
        # print(chr(27) + "[2J")
        print("\n")
        print(colored("*" * 50, "blue"))
        # print("\n")
        for index,row in enumerate(self.cells) :
            for j,col in enumerate(row) :
                if(col[0] == 0) :
                    print(colored(col[0], 'red'), end="")
                elif(col[0] == -1) :
                    print(colored(col[0], 'yellow'), end="")
                else:
                    print(col[0], end="")
                if(j == 6 and index != 2) :
                    print(colored(" |", "blue"), end="")
                if(index != 2 or j != 6) :
                    print("\t", end="")
            if(index == 2) :
                print(colored(" Exit", "cyan"), end="")
            print("\n")
        # print("\n")
        print(colored("*" * 50, "blue"))
        print("\n")

    def isGoal(self) :
        if(self.cells[2][6][0] == 0) :
            return True
        return False


class Logic :

    @staticmethod
    def CMD(state) :
        while state.isGoal() != True :
            state.displayState()
            stats = state.nextState()
            inp = input(colored("\nWhat's The Movement Would You Want: ", 'green'))
            while inp.isnumeric() != True or int(inp) < 1 or int(inp) > len(stats) :
                inp = input(colored("\nWhat's The Movement Would You Want: ", 'green'))
            state = stats[int(inp) - 1]

    @staticmethod
    def BFS(state) :
        queue = []
        queue.append(state)
        while queue != []:
            element = queue.pop(0)
            
            if (element.isGoal()) :
                return element

            hash = Logic.generate_key(element)
            if(Logic.searchInDictStats(hash) != -1) :
                continue

            dict_stats.append([hash, 1])
            stats = element.nextState()
            queue.extend(stats)
        return None

    @staticmethod
    def DFS(state) :
        stack = []
        stack.append(state)
        while stack != []:
            element = stack.pop()

            if (element.isGoal()) :
                return element
                
            hash = Logic.generate_key(element)
            if(Logic.searchInDictStats(hash) != -1) :
                continue

            dict_stats.append([hash, 1])
            stats = element.nextState()
            stack.extend(stats)
        return None

    @staticmethod
    def Dijkstra(state) :
        index = 0
        pqueue = PriorityQueue()
        pqueue.put((0, -1, state))
        while pqueue != []:
            element = pqueue.get()[2]

            if (element.isGoal()) :
                return element

            hash = Logic.generate_key(element)
            indexOfState = Logic.searchInDictStats(hash)
            if(indexOfState != -1 and dict_stats[indexOfState][1] <= element.weight):
                continue
            elif (indexOfState != -1 and dict_stats[indexOfState][1] > element.weight) :
                dict_stats[indexOfState] = [hash, element.weight]
            else :
                dict_stats.append([hash, element.weight])

            stats = element.nextState()
            for el in stats:
                pqueue.put((el.weight, index, el))
                index += 1 
        return None

    @staticmethod
    def AStar(state) :
        index = 0
        pqueue = PriorityQueue()
        pqueue.put((0, -1, state))
        while pqueue != []:
            fromQ = pqueue.get()
            cost = fromQ[0]
            element = fromQ[2]

            if (element.isGoal()) :
                return element

            hash = Logic.generate_key(element)
            indexOfState = Logic.searchInDictStats(hash)
            if(indexOfState != -1 and dict_stats[indexOfState][1] <= cost) :
                continue
            elif (indexOfState != -1 and dict_stats[indexOfState][1] > cost) :
                dict_stats[indexOfState] = [hash, cost]
            else :
                dict_stats.append([hash, cost])

            stats = element.nextState()
            for el in stats:
                pqueue.put((el.weight + Logic.Horistic(el), index, el))
                index += 1 
        return None

    @staticmethod
    def Horistic(state):
        cost = 0
        yes = False
        for i in range(7):
            if state.cells[2][i][0] == 0 :
                yes = True
            if yes and state.cells[2][i][0] != 0 :
                cost += 1
            if yes and state.cells[2][i][0] != -1 and state.cells[2][i][0] != 0 :
                cost += 0.9
        return cost

    @staticmethod
    def searchInDictStats(hash):
        for (index,row) in enumerate(dict_stats) :
            if hash == row[0]:
                return index
        return -1

    @staticmethod
    def displayPath (state):
        if(state is None):
            return
        Logic.displayPath(state.parent)
        state.displayState()

    @staticmethod
    def generate_key(state) :
        list = []
        for row in state.cells :
            for col in row :
                list.append(str(col[0]))

        return "".join(list)

    @staticmethod
    def endOfTheGame():
        print("\n\t\t\t\t\t", end="")
        print(colored("# "*22, 'cyan'))
        print(colored("\n\t\t\t\t\t#\tC o n g r a t u l a t i o n       #", 'cyan'))
        print("\n\t\t\t\t\t", end="")
        print(colored("# "*22, 'cyan'))
        print(f"\n\t\t\t\t\t  The Number Of Generation Nodes: {len(dict_stats)}")




#################################### Main #############################################

 
init =  State([[[1,1], [-1, -1], [8,2], [8,2], [-1 ,-1], [9,2], [9,2]],
            [[1,1], [-1,-1], [10,2], [10,2], [-1,-1], [-1,-1], [7,1]],
            [[0,2], [0,2], [0,2], [3,1], [-1,-1], [5,1], [7,1]],
            [[2,1], [11,2], [11,2], [3,1], [-1,-1], [5,1], [6,1]],
            [[2,1], [-1,-1], [4,2], [4,2], [12,2], [12,2], [6,1]]])


# Start Game
# Logic.CMD(init)
# Logic.displayPath(Logic.DFS(init))
# Logic.displayPath(Logic.BFS(init))
Logic.displayPath(Logic.Dijkstra(init))
# Logic.displayPath(Logic.AStar(init))


# End Game
Logic.endOfTheGame()
input("")
