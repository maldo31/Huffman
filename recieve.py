import socket

END = bytearray()
END.append(255)
print(END[0])


def recvall(sock):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # 0 lub koniec danych
            break
    return data


def create_dict(data):
    dict = {}
    i = 0
    while True:
        dict[chr(data[i])] = ''
        j = 1
        while data[i + j] != END[0]:
            dict[chr(data[i])] += str(chr(data[i + j]))
            j += 1

        i += 1 + j
        if data[i] == END[0] and data[i + 1] == END[0]:
            break
    return dict


def extract_start(data):
    i = 0
    while True:
        if data[i] == END[0] and data[i + 1] == END[0] and data[i + 2] == END[0]:
            return i + 3
        i += 1


def bytes_to_bits(data, begin):
    bits = ''
    for i in range(begin, len(data)):
        bits += format(data[i], "08b")
    return bits


def data_to_extract(data, dict):
    begin = extract_start(data)
    print(begin)
    data = bytes_to_bits(data, begin)
    dict = {y: x for x, y in dict.items()}
    text = ''
    temp_code = ''
    for i in range(len(data)):
        temp_code += data[i]
        if temp_code in dict:
            text += dict[temp_code]
            temp_code = ''
    return text


port = 9090

sock = socket.socket()
sock.bind(('', int(port)))
sock.listen()
conn, addr = sock.accept()

print('Połączono:', addr)
rec_data = recvall(conn)
rec_dict = create_dict(rec_data)
extracted = data_to_extract(rec_data, rec_dict)

print("ODEBRANY SLOWNIK\n")
print(rec_dict)
print(extracted)

f = open("odbior_ZAKODOWANY.txt", "wb")
f.write(rec_data)
f.close()
f = open("odbior_ODKODOWANY.txt", "w")
f.write(extracted)
f.close()
