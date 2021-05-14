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

file = readFromFile("kod.txt")
dictionary=count_occurance(file)
print(file)
print("\n")
print(dictionary)

