import tkinter
from tkinter import *
from tkinter import filedialog
import cv2
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from datetime import datetime
import pandas as pd
from tabulate import tabulate
gpath = "00"
#widget(yscrollcommand =scrollbar.set)
#scrollbar.configcommand = widget.yview)
def barcode(flag):
    def inbound(id):
        with open(gpath, "r+") as f:
            now = datetime.now()
            date = now.date()
            date1 = str(date)
            time = now.strftime("%H:%M:%S")
            C_id = id[0:3]
            mfg_id = id[3:7]
            pd_id = id[7:12]
            ID = id[0:12]
            pin = pd_id+"in"
            min = mfg_id+"in"
            din = date1+"in"
            list=f.readlines()
            f.writelines(f'{ID},{C_id}, {mfg_id}, {pd_id}, {date}, {time}, {"Inbound"},{pin},{min},{din}\n')

    def outbound(id):
        with open(gpath, "r+") as f:
            now = datetime.now()
            date = now.date()
            date1 =str(date)
            time = now.strftime("%H:%M:%S")
            C_id = id[0:3]
            mfg_id = id[3:7]
            pd_id = id[7:12]
            ID = id[0:12]
            pin = pd_id + "out"
            min = mfg_id + "out"
            din = date1 + "out"
            list = f.readlines()
            f.writelines(f'{ID},{C_id}, {mfg_id}, {pd_id}, {date}, {time}, {"Outbound"},{pin},{min},{din}\n')

    #print(flag)
    if(flag == "IN"):
        flag = 0
    else:
        flag = 1

    cap1 = cv2.VideoCapture(0)
    cap1.set(3, 720)
    cap1.set(4, 720)

    str1 = "000000000000000"

    time = datetime.now()
    time1 = time.strftime("%S")
    inttime = int(time1)
    while True:
        success, img1 = cap1.read()
        symbols = [ZBarSymbol.EAN13, ZBarSymbol.EAN8]
        code = decode(img1, symbols)
        for code in code:
            T = datetime.now()
            TT = int(T.strftime("%S"))
            T1 = T.strftime("%S")
            if (TT - inttime) % 5 == 0:
                stro = code.data.decode('utf-8')
                rectangle = code.rect
                topx = code.rect.left
                topy = code.rect.top
                w = code.rect.width
                h = code.rect.height
                bottomx = topx + w
                bottomy = topy + h
                strAP = stro + T1
                if (str1!= strAP)&(flag == 0):
                    str1 = strAP
                    img1 = cv2.rectangle(img1, (topx, topy), (bottomx, bottomy), (0, 255, 0), 3)
                    inbound(strAP)
                if (str1!= strAP)&(flag ==1 ):
                    str1 = strAP
                    img1 = cv2.rectangle(img1, (topx, topy), (bottomx, bottomy), (0, 255, 0), 3)
                    outbound(strAP)
        cv2.imshow("SCANNER WINDOW", img1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def Enterdata():
    input = "input00"
    def flag():
        def next():
            flag1 = str(et12.get())
            print(flag1)
            if (flag1 == "IN"):
                #flag1="IN"
                barcode(flag1)
            elif(flag1 == "OUT"):
                #flag1="OUT"
                barcode(flag1)

        subbt11 = Button(subwin, text = "NEXT",font = ("Times New Roman", 12), command =next )
        subbt11.grid(row=3, column=1, columnspan =2)
        subl4 = Label(subwin, text="PRESS 'q' TO EXIT SCANNER WINDOW", bg="orange", fg="green",
                      font=("Times New Roman", 14))
        subl4.grid(row=4, column=1, columnspan=2)
    subwin= tkinter.Tk()
    subwin.config(bg= "orange")
    subwin.title("Transaction Type")
    subl1 = Label(subwin, text = "Specify the Type of Transaction - Inbound / Outbound", font = ("Times New Roman", 15))
    subl1.grid (row= 1,column =1, columnspan =2)
    L1 = Label(subwin, text="Transaction Type - 'IN'/'OUT'", font = ("Times New Roman", 12))
    L1.grid(row=2, column=1)
    et12 = Entry(subwin, width = 15)
    et12.grid(row=2, column=2)
    flag()
    mainloop()
def Getstats():
    with open(gpath) as file:
        list = file.readlines()
    size=len(list)
    label = Label(window, text="ID - Country ID - Mfg ID - Product ID - Date - Time - Type", font=("Times New Roman", 14))
    label.grid(row=6, column=2, columnspan = 3)
    scrollbar=Scrollbar(window)
    scrollbar.grid(row=7, column =4)
    list1 = Listbox(window, width=55,height=25, font=("Times New Roman", 14), yscrollcommand = scrollbar.set)
    i = 1
    while i < size:
        ilist = list[i]
        list1.insert(i, ilist[0:61])
        i = i + 1
    scrollbar.config(command = list1.yview)
    list1.grid(row=7, column=2, columnspan=3)
    data = pd.read_csv(gpath)
    dataframe = pd.DataFrame(data)
    datadf = tabulate(dataframe, headers = "keys", tablefmt="psql")
    datawin = tkinter.Tk()
    datawin.title("Statistics")
    x= data["Type"].value_counts()
    y= x.index
    size = y.size
    sz = 0
    if (size == 2):
        sz=2
        a = str(str(y[0]) + "s = " +  str(x[0]))
        b= str(str(y[1]) + "s = " +  str(x[1]))
        l1= Label(datawin, text ="Total "+a+" |", font = ("Times New Roman", 14) )
        l1.grid(row=1, column =1, columnspan= 1)
        l2 = Label(datawin, text = "Total "+b+" |" , font = ("Times New Roman", 14))
        l2.grid(row =1, column =2, columnspan= 1)
        if(str(y[0]) == "Outbound"):
            #x[0] is outbounds and x[1] is inbound
            instocks = int(x[1])-int(x[0])
        else:
            instocks = int(x[0])-int(x[1])
        l3 = Label(datawin, text = "Instocks = "+ str(instocks) , font = ("Times New Roman", 14))
        l3.grid(row=1, column  =3, columnspan= 1)
    if (size == 1):
        sz=1
        a = str(str(y[0]) + "s = " +  str(x[0]))
        l1 = Label(datawin, text="Total " + a, font=("Times New Roman", 14))
        l1.grid(row =1, column =1, columnspan= 1)
        if (str(y[0]) == "Outbound"):
            # x[0] is outbounds and x[1] is inbound
            instocks = 0
        else:
            instocks = int(x[0])
        l2 = Label(datawin, text="Instocks = " + str(instocks), font=("Times New Roman", 14))
        l2.grid(row= 1, column = 2, columnspan= 1)
    pin = data["Pin"].value_counts()
    min = data["Min"].value_counts()
    din = data["Din"].value_counts()

    l11 = Label(datawin, text = "--**Search by**-- ", font=("Times New Roman", 14))
    l11.grid(row =2, column = 2)
    l12 = Label(datawin, text = "Product ID", font=("Times New Roman", 14))
    l12.grid(row =3, column =1)
    l13 = Label(datawin, text="Mfg ID", font=("Times New Roman", 14))
    l13.grid(row=3, column=2)
    l14 = Label(datawin, text="Date", font=("Times New Roman", 14))
    l14.grid(row=3, column=3)
    l15 = Label(datawin, text = "*_*Pdt ID In/Out bounds", fg="red", font=("Times New Roman", 11))
    l15.grid(row=4, column=1)
    l16 = Label(datawin, text="*_*Mfg ID In/Out bounds", fg="red", font=("Times New Roman", 11))
    l16.grid(row=4, column=2)
    l17= Label(datawin, text="*_*Date In/Out bounds", fg="red", font=("Times New Roman", 11))
    l17.grid(row=4, column=3)
    choices = []
    choices_m=[]
    choices_d =[]
    ipin= 0
    imin =0
    idin =0
    while ipin< pin.size:
        pinindex = pin.index
        pstr=str(pinindex[ipin])
        pinstr1 = "*"+str(ipin)+"*"+pstr[0:5]
        pinstr2 = pstr[5:7]
        if pinstr2 == "in":
            addstringIN = pinstr1+" Inbounds"
            choices.append(addstringIN)
        else:
            addstringOUT = pinstr1 + " Outbounds"
            choices.append(addstringOUT)
        ipin = ipin+1
    default = StringVar(datawin)
    default_m=StringVar(datawin)
    default_d=StringVar(datawin)
    default_m.set("Select")
    default_d.set("Select")
    default.set("Select")
    pp11 = OptionMenu(datawin, default, *choices)
    pp11.grid(row=5, column=1)
    def selectedp():
        selopt = str(default.get())
        index = int(selopt[1])
        finalstr = str("Pdt ID-"+" " +selopt[3:8]+" "+ selopt[8:]+ " = "+ str(pin[index]))
        sellb1 = Label(datawin, text = finalstr, font = ("Times New Roman", 12))
        sellb1.grid(row=7, column =1)
    b11 = Button(datawin, text = "Get Count", command = selectedp, font = ("Times New Roman", 12))
    b11.grid(row=6, column =1)
    ##########################
    while imin< min.size:
        minindex = min.index
        mstr=str(minindex[imin])
        minstr1 = "*"+str(imin)+"*"+mstr[0:4]
        minstr2 = mstr[4:]
        if minstr2 == "in":
            addstringmIN = minstr1+" Inbounds"
            choices_m.append(addstringmIN)
        else:
            addstringmOUT = minstr1 + " Outbounds"
            choices_m.append(addstringmOUT)
        imin = imin+1
    mm11 = OptionMenu(datawin, default_m, *choices_m)
    mm11.grid(row=5, column=2)
    def selectedm():
        selopt = str(default_m.get())
        index = int(selopt[1])
        finalstr = str("Mfg ID-" + " " + selopt[3:7] + " " + selopt[7:] + " = " + str(min[index]))
        sellb1 = Label(datawin, text=finalstr, font=("Times New Roman", 12))
        sellb1.grid(row=7, column=2)

    b12 = Button(datawin, text="Get Count", command=selectedm, font=("Times New Roman", 12))
    b12.grid(row=6, column=2)
    ########################
    while idin< din.size:
        dinindex = din.index
        dstr=str(dinindex[idin])
        dinstr1 = "*"+str(idin)+"*"+dstr[0:10]
        dinstr2 = dstr[10:]
        if dinstr2 == "in":
            addstringdIN = dinstr1+" Inbounds"
            choices_d.append(addstringdIN)
        else:
            addstringdOUT = dinstr1 + " Outbounds"
            choices_d.append(addstringdOUT)
        idin = idin+1

    dd11 = OptionMenu(datawin, default_d, *choices_d)
    dd11.grid(row=5, column=3)
    def selectedp():
        selopt = str(default_d.get())
        index = int(selopt[1])
        finalstr = str("Date -" + " " + selopt[3:10] + " " + selopt[10:] + " = " + str(din[index]))
        sellb1 = Label(datawin, text=finalstr, font=("Times New Roman", 12))
        sellb1.grid(row=7, column=3)
    b13 = Button(datawin, text="Get Count", command=selectedp, font=("Times New Roman", 12))
    b13.grid(row=6, column=3)
def createfile():
    files = [('CSV', '*.csv')]
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files, title = "Select Location")
    path  = file.name
    with open(path, "r+") as f:
        if True:
            global gpath
            gpath = path
            list =f.readlines()
            f.writelines(f'{"ID"}, {"Country ID"}, {"Mfg ID"}, {"Product ID"}, {"Date"}, {"Time"},{"Type"},{"Pin"},{"Min"},{"Din"}\n')
            l2.configure(text = "FILE CREATED SUCCESSFULLY>IMPORT THE FILE",bg = "green",fg = "white",  font = ("Times New Roman", 12))
            #bt2.configure(command = Enterdata, bg = "green")
            #bt3.configure(command = Getstats, bg = "green")
            #bt2["state"]= DISABLED
            #bt3["state"] = DISABLED

def openfile():
    file = filedialog.askopenfile(title = "Extract Data")
    path = file.name
    with open(path) as f:
        if True:
            global gpath
            gpath = path
            l2.configure(text = "FILE ACCESED SUCCESSFULLY",bg = "green",fg = "white",  font = ("Times New Roman", 12))
            bt2.configure(command = Enterdata, fg = "green")
            bt3.configure(command = Getstats,fg = "green")
            bt2["state"]= ACTIVE
            bt3["state"] = ACTIVE

window= tkinter.Tk()
window.title("Tool")
w = window.winfo_screenwidth()
h= window.winfo_screenheight()
window.geometry('%dx%d'%(w,h))
window.config(bg="orange")
l1 = Label(window, text = "TO BEGIN LOAD THE FILE FIRST",bg = "orange" , fg = "red", font = ("Times New Roman", 12))
l1. grid(row = 1,column = 3)
cl1 = Label(window, text = "  INVENTORY ",bg= "green" , fg = "white", font = ("Times New Roman", 35))
cl1.grid(row= 0, column = 2)
cl2 = Label(window, text = " MANAGEMENT ", bg= "green" , fg = "white", font = ("Times New Roman", 35))
cl2.grid(row= 0, column = 3)
cl3 = Label(window, text = "TOOL        ", bg= "green" , fg = "white",font = ("Times New Roman", 35))
cl3.grid(row= 0, column = 4)
cl4 = Label(window, text = "                      ***",bg= "green" , fg = "green", font = ("Times New Roman", 35))
cl4.grid(row= 0, column = 5)
cl5 = Label(window, text = "***                 ",bg= "green" , fg = "green", font = ("Times New Roman", 35))
cl5.grid(row= 0, column = 1)
bt1 = Button(window, text = "Import File",bg= "orange", font = ("Times New Roman", 13), command = openfile )
bt1.grid(row = 1, column =2)
bt1 = Button(window, text = "Create New File",bg= "orange",font = ("Times New Roman", 13), command = createfile)
bt1.grid(row = 1, column =4)
l2 = Label(window, text = "*csv file only*",fg = "red", bg= "orange", font = ("Times New Roman", 12))
l2.grid(row= 2, column = 3)
bt2 = Button(window, text = "Enter the Data",bg= "orange", fg= "black", font = ("Times New Roman", 11))
bt2.grid(row=4, column =3)
bt2["state"] = DISABLED
bt3 = Button(window, text = "Get Statistics",bg= "orange", fg= "black", font = ("Times New Roman", 11))
bt3.grid(row = 5, column =3)
bt3["state"]= DISABLED
mainloop()
