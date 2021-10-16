import sys
import queue

class Node:
    word = ""
    Children = {}
    parent = None
    def __init__ (self, word):
        self.word = word
        self.Children = {}

    def GetChildren(self):
        return self.Children

    def AddChild(self, key, word):
        if (key in self.Children):
                newNode = Node(word);
                self.Children = {key: newNode};
                newNode.parent = self;
        else:
            newNode = Node(word);
            self.Children = {key: newNode};
            newNode.parent = self;

class BKTree(object):
    _Root = None
    

    def  Add(self, word):
        if self._Root is None:
            self._Root = Node(word);
            self._Root.parent = self._Root;
            return;
        curNode = self._Root;
        while (curNode is not None):
            nodeWord = curNode.word;
            distance = self.LevenshteinDistance(word, nodeWord);
            parent = curNode;
            if (distance in curNode.GetChildren()):
                curNode = curNode.GetChildren().get(distance)
            else:
                curNode = None
            if curNode is None:
                parent.AddChild(distance, word)

    def Search(self, startingWord, finalWord, r):     
        searchResults = []
        toCheck = queue.Queue()
        toCheck.put(self._Root)
        while (toCheck.qsize() > 0):
            node = toCheck.get()
            nodeWord = node.word
            distance = self.LevenshteinDistance(finalWord, nodeWord)
            if distance <= r:
                searchResults.append(nodeWord)                     
            l = distance - r
            h = distance + r
            for  child in node.GetChildren():
                if (l <= child): 
                    if (child <= h):
                        toCheck.put(node.GetChildren()[child])
        return searchResults;

    def LevenshteinDistance(self, first, second):
        if (len(first) == 0): 
            return len(second)
        if (len(second) == 0):
            return len(first)
        lenFirst = len(first)
        lenSecond = len(second)

        d = {}
        for i in range(lenFirst+1):
            d[i,0] = i
        for i in range(lenSecond+1):
            d[0,i] = i;
        for j in range(1,lenSecond+1):
            for i in range(1,lenFirst+1):
                if first[i-1] == second[j-1]:
                    d[i,j] = d[i-1,j-1]
                else:
                    d[i,j] = min(d[i-1,j] + 1, d[i,j-1]+1, d[i-1,j-1]+1)

        return d[lenFirst, lenSecond]

def MyOpenFile(path, text): # Function that opens a file at location "path" and returns the text specified. If locating the file fails, user is asked to try again 

    try: # if file at location "path" opened sucessfully 
        with open(path, "r") as graphFile:			
            # take all the lines from the file and save them to the "text" var
            text = graphFile.readlines()
            graphFile.close()
            return text   
    except FileNotFoundError: # if file at location "path" fails to open
        print("file could not be opened")
        print("Write the full path of the file that contains the graph")
        path = input("") #save new path inserted from user
        return MyOpenFile(path, text) # try again to open file	

path = ""
startingWord =  ""
finalWord =  ""
text = []
if (len(sys.argv) > 2):
    path = sys.argv[1]
    startingWord =  sys.argv[2]
    finalWord =  sys.argv[3]
else:
    print("Write the full path of the file that contains the words")
    path = input("")
    print("you typed: "+ path)
    print("Write the starting word")
    startingWord = input("")
    print("Write the final word")
    finalWord = input("")

print("Opened file succesfully")
text =  MyOpenFile(path, text)

tree = BKTree()
for word in text:
    tree.Add(word)
results = tree.Search(startingWord, finalWord, 1)
print("\n" + "\n" + "-------RESULTS-------" + "\n" + "\n")
closestWord = ""
for word in results:
    print(word)

           
     