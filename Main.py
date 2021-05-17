import socket


def readFromFile(path):                     #Odczyt pliku do kodowania
    f = open(path, "r")
    read = f.read()
    return read

 #Zapis zakodowanego pliku
def write_to_file(path, text):
    file = open(path, "w")
    file.write(text)
    file.close()

#Liczymy wystąpienia znaku
def count_occurance(text):
    dict = {}
    for char in text:
        if char in dict:
            dict[char] += 1
        else:
            dict[char] = 1
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)   #Zwracamy posortowane malejąco wystąpienia znaku
    return dict                                                     #wraz z ich liczbą


                                                                    # Klasa odpowiedzialna za drzewo binarne
class NodeTree(object):                                             #Wymagane do stworzenia kodu huffmana

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


                                                        # Funkcja używająca drzewa do implementacji kodowania huffmana
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()                                           #Dodaje "bit" przy przejsciu przez liść drzewa
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


def create_huffman_dict(freq_dict):                        #Tworzymy strukture słownika kodowego
    nodes = freq_dict
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]                                  #Tworzymy liście drzewa
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])            #Na podstawie drzewa dostajemy słownik kodowy
    return huffmanCode


def print_Table(freq, huffmanCode):                         #Drukowanie słownika w przyjaznej formie
    print(' Char | Huffman code ')
    print('----------------------')
    for (char, frequency) in freq:
        print(' %-4r |%12s' % (char, huffmanCode[char]))


def encode_text(text, huffmanCode):                         #Koduje tekst do ciągu 0 i 1, na podstawie słownika
    codedmessage = ''
    for char in text:
        codedmessage += huffmanCode[char]
    return codedmessage


def convert_text_to_bytes(coded):                            #Zamiana ciągu 0 i 1 do bajtów
    if len(coded) % 8 == 0:
        splited = [coded[8 * i:8 * (i + 1)] for i in range(int(len(coded) / 8))]
    else:
        splited = [coded[8 * i:8 * (i + 1)] for i in range(int(len(coded) / 8) + 1)]
    splited = [int(i, 2) for i in splited]
    splited = bytearray(splited)
    return splited


def prepare_dict(dict):                                     #Przygotowuje słownik do wysłania, zamienia go na bajty
    to_send = bytearray()
    for key in dict:
        to_send.append(ord(key))
        i = 0
        for char in dict[key]:
            i += 1
            # print(i)
            to_send.append(ord(char))

        to_send.append(255)                                 #Pomiędzy znaki wstawia FF
    to_send.append(255)                                     #Na końcu słownika wstawia 3xFF
    to_send.append(255)
    return to_send


def final_message(dict, text):                              #Zwraca słownik + dane, zakodowane, w formie bajtowej
    final = dict + text
    return final


def send_data(data, ip='localhost', port=10000):            #Wysyła dane poprzez gniazdo
    sock = socket.socket()
    sock.connect((ip, int(port)))
    print("Połączono z:" + str(ip) + str(port))
    sock.send(data)


def send(readpath, savepath, ip, socket):                   #Główna funkcja której używa GUI
    file = readFromFile(readpath)
    dictionary = count_occurance(file)                      #Na podstawie pliku liczymy wystąpienia
    kodowanie = create_huffman_dict(dictionary)             #Tworzymy słownik
    print(kodowanie)
    coded_dict = prepare_dict(kodowanie)                    #Przygotowujemy słownik do przesyłu
    # print(prepare_dict(kodowanie))
    print_Table(dictionary, kodowanie)
    coded = encode_text(file, kodowanie)                    #Kodujemy tekst otrzymanym słownikiem
    #
    text_zakodowany = convert_text_to_bytes(coded)          #Zamieniamy kod, na bajty
    final = final_message(coded_dict, text_zakodowany)      #Laczymy zakodowany slownik z zakodowanym tekstem
    # print(convert_text_to_bytes(coded))
    # write_to_file(savepath,coded)
    send_data(final, ip, int(socket))                       #Wysylamy
    f = open(savepath, "wb")
    f.write(final)
    f.close()
    return 0
