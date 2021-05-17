import socket

END = bytearray()
END.append(255)
print("dupa")
print(END[0])
import time
def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def create_dict(data):
    dict={}
    i=0
    print(len(data))
    while True:
        dict[chr(data[i])]=0
        int=0
        j=1
        while data[i+j] !=END[0]:
            print(END)
            #print(i+j)
            #print(data[i+j])
            int+=(data[i+j])
            j+=1

        i+=1+j
        if data[i]==END[0] and data[i+1]==END[0]:
            break
    return dict





port=9090

sock = socket.socket()
sock.bind(('',int(port)))
sock.listen()
conn, addr = sock.accept()

print('Połączono:', addr)
rec_data=recvall(conn)
rec_dict=create_dict(rec_data)
print("ODEBRANY SLOWNIK\n")
print(rec_dict)

f = open("odbior.txt", "wb")
f.write(rec_data)
f.close()


