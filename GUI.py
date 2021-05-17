from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import os

from tkinter import filedialog
import serial
import time

class XmodemGUI:
    def __init__(self):
        self.root = Tk()
        self.stopbit = StringVar()
        self.stopbit.set("1.0")
        self.mode = StringVar()
        self.mode.set("NAK")
        self.root.title("Xmodem 229952|230039")
        self.filename = None
        self.send_mode = IntVar()
        self.com_port = StringVar()
        self.com_port.set("COM2")
        self.parity = StringVar()
        self.parity.set("None")
        self.tytul_label = Label(self.root, text="XMODEM", font=(None, 17, 'bold'), fg='blue')
        self.tytul_label.grid(row=0, column=0, columnspan=6)

        self.tytul_label = Label(self.root, text="USTAWIENIA", font=(None, 14, 'bold'))
        self.tytul_label.grid(row=1, column=0, columnspan=4)

        self.tryb_frame = LabelFrame(self.root, text="Tryb:", padx=40, pady=8)
        self.tryb_frame.grid(row=5, column=0, columnspan=2)
        self.tryb_CRC = Radiobutton(self.tryb_frame, text="CRC", variable=self.mode, value="C")
        self.tryb_Checksum = Radiobutton(self.tryb_frame, text="Checksum", variable=self.mode, value="NAK")
        self.tryb_CRC.grid(row=0, column=0)
        self.tryb_Checksum.grid(row=0, column=1)

        self.stopbit_frame = LabelFrame(self.root, text="Bity stopu:", padx=40, pady=8)
        self.stopbit_frame.grid(row=6, column=0, columnspan=2)
        self.bitone = Radiobutton(self.stopbit_frame, text="1bit", variable=self.stopbit, value="1.0",
                                  command=self.changeStopBit)
        self.bitonehalf = Radiobutton(self.stopbit_frame, text="1.5bit", variable=self.stopbit, value="1.5",
                                      command=self.changeStopBit)
        self.bittwo = Radiobutton(self.stopbit_frame, text="2bit", variable=self.stopbit, value="2.0",
                                  command=self.changeStopBit)
        self.bitone.grid(row=0, column=0)
        self.bitonehalf.grid(row=0, column=1)
        self.bittwo.grid(row=0, column=2)

        self.odczyt_label = Label(self.root, text="Odczyt z pliku:")
        self.odczyt_label.grid(row=2, column=0)
        self.odczyt_button = Button(self.root, text="Wybierz Plik", command=self.loadFile)
        self.zapisz_button = Button(self.root, text="Wybierz Plik", command=self.saveFile)
        self.odczyt_button.grid(row=2, column=1)
        self.zapisz_button.grid(row=4, column=1)

        self.port_label = Label(self.root, text="Port COM:")
        self.port_label.grid(row=3, column=0)
        self.port_menu = OptionMenu(self.root, self.com_port, "COM1", "COM2", "COM3", "COM4", command=self.changePort)
        self.port_menu.grid(row=3, column=1)

        self.zapis_label = Label(self.root, text="Zapis do pliku:")
        self.zapis_label.grid(row=4, column=0)

        self.szerokosc_label = Label(self.root, text="Szerokość pasma")
        self.szerokosc_label.grid(row=7, column=0)

        self.podpis_label = Label(self.root, text="©Daniel Malicki/Maciej Wlodarczyk")
        self.podpis_label.grid(row=12, column=4)

        self.szerokosc_entry = Entry(self.root, width=8)
        self.szerokosc_entry.grid(row=7, column=1)
        self.szerokosc_entry.insert(0, 9600)

        self.logi_text = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.logi_text.grid(row=2, column=4, rowspan=7)
        self.postep_label = Label(self.root, text="Postęp:")
        self.postep_label.grid(row=10, column=4)

        self.wyslij_button = Button(self.root, text="Wyślij", font=(None, 13, 'bold'), width=20, height=3, bg='green',
                                    command=self.wyslijClick)
        self.zatrzymaj_button = Button(self.root, text="Zatrzymaj", font=(None, 13, 'bold'), width=20, height=3,
                                       bg='red',
                                       command=self.zatrzymaj)
        self.odbierz_button = Button(self.root, text="Odbierz", font=(None, 13, 'bold'), width=20, height=3, bg='blue',
                                     command=self.odbierzClick)
        self.odbierz_button.grid(row=2, column=5, rowspan=2)
        self.zatrzymaj_button.grid(row=4, column=5, rowspan=2)

        self.wyslij_button.grid(row=6, column=5, rowspan=2)
        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=500, mode='determinate')
        self.progress.grid(row=11, column=1, columnspan=4, sticky="E")
        self.port_label = Label(self.root, text="Parzystość:")
        self.port_label.grid(row=11, column=0)
        self.port_menu = OptionMenu(self.root, self.parity, "None", "Even", "Odd")
        self.port_menu.grid(row=11, column=1)

        self.mode1k = Checkbutton(self.root, text = "Tryb 1K", font=(None,12),
                                  variable=self.send_mode)
        self.mode1k.grid(row=12, column=0, columnspan=2,sticky="S")

    def dodajprocent(self, value):
        self.progress['value'] = value

    def zatrzymaj(self):
        self.logi_text.delete('1.0', END)
        self.progress['value'] = 0
        self.xmodem.cancel_transmision()

    def wyslijClick(self):
        self.progress['value'] = 0
        if self.filename:
            # ser.baudrate = int(self.szerokosc_entry.get())
            # print(self.send_mode.get())
            # if self.send_mode.get()==0:
            #     self.xmodem.change_send_mode(SOH)
            # else:
            #     self.xmodem.change_send_mode(STX)
            self.odbierz_button.config(state="disabled")
            self.wyslij_button.config(state="disabled")
            self.logi_text.delete(1.0, END)
            self.logi_text.insert(INSERT, "WYSYŁAM ")
            self.root.update()
            self.xmodem.send_data()
            self.wyslij_button.config(state="normal")
            self.odbierz_button.config(state="normal")
        else:
            self.errorFile()

    def printToLogi(self, text):
        self.logi_text.insert(INSERT, text)
        self.logi_text.see("end")

    def odbierzClick(self):
        self.progress['value'] = 0
        if self.filename:
            # ser.baudrate = int(self.szerokosc_entry.get())
            self.odbierz_button.config(state="disabled")
            self.wyslij_button.config(state="disabled")
            self.root.update()
            time.sleep(1)
            # if self.mode.get() == "C":
            #     self.xmodem.recive_data(C, self)
            # else:
            #     self.xmodem.recive_data(NAK, self)
            self.wyslij_button.config(state="normal")
            self.odbierz_button.config(state="normal")
        else:
            self.errorFile()

    def errorFile(self):
        messagebox.showerror("Błąd", "Podaj plik")

    def loadFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes='')
        self.xmodem.setFileName(self.filename)

    def saveFile(self):
        self.filename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik")
        self.xmodem.setFileName(self.filename)

    def bitradio(self):
        print("stopbit" + self.stopbit.get())

    def changePort(self, value):
        # ser.port = self.com_port.get()

    def changeStopBit(self):
        if self.stopbit.get() == "1.0":
            serial.STOPBITS_ONE
        elif self.stopbit.get() == "2.0":
            serial.STOPBITS_TWO
        else:
            serial.STOPBITS_ONE_POINT_FIVE

    def start_gui(self):
        self.root.mainloop()