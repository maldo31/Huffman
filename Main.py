class node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''


def printNodes(node, val=''):
    # huffman code for current node
    newVal = val + str(node.huff)
    # if node is not an edge node
    # then traverse inside it
    if (node.left):
        printNodes(node.left, newVal)
    if (node.right):
        printNodes(node.right, newVal)
    if (not node.left and not node.right):
        print(f"{node.symbol} -> {newVal}")

def readFromFile(path):
    f = open(path,"r")
    read=f.read()
    return read
def count_occurance(text):
    dict = {}
    for char in text:
        if char in dict:
            dict[char]+=1
        else:
            dict[char]=1
    return dict

def sortDict(to_sort):
    sorted_dict = {}
    sorted_keys = sorted(to_sort, key=to_sort.get,reverse=True)  # [1, 3, 2]
    for w in sorted_keys:
        sorted_dict[w]=to_sort[w]
    return sorted_dict




file = readFromFile("kod.txt")
dictionary=count_occurance(file)
sorted=sortDict(dictionary)
counted=sum(sorted.values())
print(file)
print("\n")
print(dictionary)
print(sorted)
print(counted)

