import socket

def readFromFile(path):
    f = open(path,"r")
    read=f.read()
    return read
def write_to_file(path,text):
    file = open(path,"w")
    file.write(text)
    file.close()
def count_occurance(text):
    dict = {}
    for char in text:
        if char in dict:
            dict[char]+=1
        else:
            dict[char]=1
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return dict


# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# Main function implementing huffman coding
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

def create_huffman_dict(freq_dict):
    nodes = freq_dict
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])
    return huffmanCode

def print_Table(freq,huffmanCode):
    print(' Char | Huffman code ')
    print('----------------------')
    for (char, frequency) in freq:
        print(' %-4r |%12s' % (char, huffmanCode[char]))
def encode_text(text,huffmanCode):
    codedmessage=''
    for char in text:
        # print(char)
        codedmessage+=huffmanCode[char]
    return codedmessage

def convert_text_to_bytes(coded):
    if len(coded) % 8 ==0:
        splited = [coded[8 * i:8 * (i + 1)] for i in range(int(len(coded) / 8) )]
    else:
        splited = [coded[8 * i:8 * (i + 1)] for i in range(int(len(coded) / 8)+1)]
    splited = [int(i, 2) for i in splited]
    splited = bytearray(splited)
    return splited

def prepare_dict(dict):
    to_send=bytearray()
    for key in dict:
        to_send.append(ord(key))
        i=0
        for char in dict[key]:
            i+=1
            print(i)
            to_send.append(ord(char))

        to_send.append(255)
    to_send.append(255)
    to_send.append(255)
    return to_send

def final_message(dict,text):
    final =dict+text
    return final

def send_data(data,ip='localhost',port=9090):
    sock=socket.socket()
    sock.connect((ip,int(port)))
    print("Połączono z:"+str(ip)+str(port))
    sock.send(data)

file = readFromFile("hamlet.txt")
dictionary=count_occurance(file)
kodowanie=create_huffman_dict(dictionary)
print(kodowanie)
print("\n\n\nSŁOWNIK W BITACH=\n")
coded_dict=prepare_dict(kodowanie)

print(prepare_dict(kodowanie))
print_Table(dictionary,kodowanie)
coded=encode_text(file,kodowanie)

text_zakodowany=convert_text_to_bytes(coded)

final=final_message(coded_dict,text_zakodowany)
print(convert_text_to_bytes(coded))
write_to_file("zakodwane.txt",coded)

send_data(final)
f = open("sample.txt", "wb")
f.write(final)
f.close()
# counted=sum(dictionary.values())
# print(file)
# print("\n")
# print(dictionary)
# print(sorted)
# print(counted)

