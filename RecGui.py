from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import recieve as recieve

from tkinter import filedialog
import serial
import time

class SendGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("HUFFMAN 229952|230039")
        self.socket = StringVar()
        self.socket.set("10000")
        self.ip = StringVar()
        self.ip.set("127.0.0.1")
        self.codedfilename = None
        self.decodedfilename = None
        self.send_mode = IntVar()
        self.com_port = StringVar()
        self.com_port.set("COM2")
        self.parity = StringVar()
        self.parity.set("None")
        self.tytul_label = Label(self.root, text="HUFFMAN ODBIÓR", font=(None, 17, 'bold'), fg='blue')
        self.tytul_label.grid(row=0, column=0, columnspan=4)

        # self.tytul_label = Label(self.root, text="USTAWIENIA", font=(None, 14, 'bold'))
        # self.tytul_label.grid(row=1, column=0, columnspan=2)



        self.odczyt_label = Label(self.root, text="Zapis zakodowanego do:")
        self.odczyt_label.grid(row=2, column=0)
        self.odczyt_button = Button(self.root, text="Wybierz Plik", command=self.savecoded)
        self.odczyt_button.grid(row=2, column=1)



        self.zapis_label = Label(self.root, text="Zapis odkodowanego:")
        self.zapis_label.grid(row=3, column=0)
        self.zapisz_button = Button(self.root, text="Wybierz Plik", command=self.savedecoded)
        self.zapisz_button.grid(row=3, column=1)

        self.podpis_label = Label(self.root, text="©Daniel Malicki/Maciej Wlodarczyk")
        self.podpis_label.grid(row=12, column=1)

        self.szerokosc_label = Label(self.root, text="Port")
        self.szerokosc_label.grid(row=5, column=0)

        self.szerokosc_entry = Entry(self.root,textvariable=self.socket, width=8)
        self.szerokosc_entry.grid(row=5, column=1)

        self.adres_label = Label(self.root, text="Adres IP")
        self.adres_label.grid(row=4, column=0)

        self.adres_entry = Entry(self.root,textvariable=self.ip, width=20)
        self.adres_entry.grid(row=4, column=1)


        self.wyslij_button = Button(self.root, text="Odbierz", font=(None, 13, 'bold'), width=20, height=3, bg='green',
                                    command=self.odbierzClick)

        # self.odbierz_button = Button(self.root, text="Odbierz", font=(None, 13, 'bold'), width=20, height=3, bg='blue',
        #                              command=self.odbierzClick)
        # self.odbierz_button.grid(row=2, column=5, rowspan=2)
        # self.zatrzymaj_button.grid(row=4, column=5, rowspan=2)

        self.wyslij_button.grid(row=6, column=0, rowspan=2,columnspan=2)




    def odbierzClick(self):
        if self.decodedfilename and self.codedfilename:
           recieve.recieve_data(self.codedfilename,self.decodedfilename,self.ip.get(),self.socket.get())
        else:
            self.errorFile()


    # def odbierzClick(self):
    #     self.progress['value'] = 0
    #     if self.filename:
    #         # ser.baudrate = int(self.szerokosc_entry.get())
    #         self.odbierz_button.config(state="disabled")
    #         self.wyslij_button.config(state="disabled")
    #         self.root.update()
    #         time.sleep(1)
    #         # if self.mode.get() == "C":
    #         #     self.xmodem.recive_data(C, self)
    #         # else:
    #         #     self.xmodem.recive_data(NAK, self)
    #         self.wyslij_button.config(state="normal")
    #         self.odbierz_button.config(state="normal")
    #     else:
    #         self.errorFile()

    def errorFile(self):
        messagebox.showerror("Błąd", "Podaj plik")

    def savecoded(self):
        self.codedfilename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik")

    def savedecoded(self):
        self.decodedfilename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik")



    def start_gui(self):
        self.root.mainloop()

app = SendGUI()
app.start_gui()