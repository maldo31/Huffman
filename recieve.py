import socket

END = bytearray()
END.append(255)
print(END[0])


def recvall(sock):  # Odbiór danych
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:  # odbieramy dane, pakiety 4KiB
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # 0 lub koniec danych
            break
    return data


def create_dict(data):  # Odczytuje otrzymany słownik
    dict = {}
    i = 0
    while True:
        dict[chr(data[i])] = ''
        j = 1
        while data[i + j] != END[0]:  # Dopóki nie znajdzie FF, uznaje bajty za 'kod' slowa
            dict[chr(data[i])] += str(chr(data[i + j]))
            j += 1

        i += 1 + j
        if data[i] == END[0] and data[i + 1] == END[0]:  # Gdy znajdzie 3x FF, kończy słownik
            break
    return dict


def extract_start(data):  # Poszukuje pącztka segmentu danych
    i = 0
    while True:
        if data[i] == END[0] and data[i + 1] == END[0] and data[i + 2] == END[0]:
            return i + 3
        i += 1


def bytes_to_bits(data, begin):  # Zamienia bajty na znakowy odpowiednik w bitach
    bits = ''
    for i in range(begin, len(data)):
        bits += format(data[i], "08b")
    return bits


def data_to_extract(data, dict):  # Otrzymane dane na podstawie slownika odczytuje do tekstu
    begin = extract_start(data)  # Szukamy początku tekstu
    print(begin)
    data = bytes_to_bits(data, begin)
    dict = {y: x for x, y in dict.items()}  # Zamiana kluczy z wartością w słowniku
    text = ''
    temp_code = ''
    for i in range(len(data)):  # Dla kazdego bitu
        temp_code += data[i]
        if temp_code in dict:  # Szukamy czy utworzona tymczasowo zmienna nie zawiera się
            # w słowniku
            text += dict[temp_code]
            temp_code = ''
    return text


def recieve_data(codedpath, decodedpath, ip, port):
    port = int(port)                        #Segment odpowiedzialny za utworzenie połaczenia przy użyciu gniazda
    sock = socket.socket()
    sock.bind((ip, int(port)))
    sock.listen()
    conn, addr = sock.accept()
    print('Połączono:', addr)
    rec_data = recvall(conn)                            #Odbierz dane
    rec_dict = create_dict(rec_data)                    #Utwórz słownik z danych
    extracted = data_to_extract(rec_data, rec_dict)     #Na podstawie słownika, odkoduj tekst

    print("ODEBRANY SLOWNIK\n")
    print(rec_dict)
    print(extracted)

    f = open(codedpath, "wb")                           #Zapis otrzymanych danych
    f.write(rec_data)
    f.close()
    f = open(decodedpath, "w")
    f.write(extracted)
    f.close()
    return 0
