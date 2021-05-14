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

