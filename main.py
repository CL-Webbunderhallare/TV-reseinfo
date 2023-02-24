import requests
import tkinter as tk
from tkinter import ttk
import time

#Skrivet av Nima. Pallar inte dokumentera kontakta mig bara. Jag lär ju ha gått klart CL när du väl ser det här :(

class Resa:
    def __init__(self, typ, avgang, linje=None, installd=False, slutstation = None, riktning = None):
        self.typ = typ
        self.avgang = avgang
        self.installd = installd
        if typ == "buss" or typ == "bana":
            self.slutstation = slutstation
            self.linje = linje
        else:
            #för tunnelbanan
            self.riktning = riktning


#big dic(tionary)

def tunnelbana(tunnelbanaLista):
    #returnerar första tåget norrut och första söderut
    flag1 = False
    flag2 = False
    flag3 = False
    norrTåg = "Mörby tåget avgår om:\n"
    fruangen = "Fruängen tåget avgår om:\n"
    liljeholmen = "Liljeholmen tåget avgår om:\n"
    for index, åk in enumerate(tunnelbanaLista):
        if index == 10:
            break #nej nej nu har vi gått för långt
        if åk["JourneyDirection"] == 1:
            flag1 = True
            if åk["Deviations"] == None:
                avgang = åk["DisplayTime"]
                norrTåg += (str(avgang)+"\n")
            else:
                norrTåg += "Inställd\n"
        elif åk["JourneyDirection"] == 2 and åk["Destination"] == "Fruängen":
            if åk["Deviations"] == None:
                avgang = åk["DisplayTime"]
                fruangen += (str(avgang)+"\n")
            else:
                fruangen += "Inställd\n"
        elif åk["JourneyDirection"] == 2 and åk["Destination"] == "Liljeholmen":
            flag3 = True
            if åk["Deviations"] == None:
                avgang = åk["DisplayTime"]
                liljeholmen += (str(avgang)+"\n")
            else:
                liljeholmen += "Inställd\n"
    return norrTåg, fruangen, liljeholmen

def buss(bussLista):
    #just nu tar vi bara första bussen
    bussen = "Bussarna som avgår:\n"
    i = 0
    for buss in bussLista:
        buss1 = bussLista[0]
        linje = buss["LineNumber"]
        slutstation = buss["Destination"]
        if buss["Deviations"] == None:
            avgang = buss["DisplayTime"]
            bussen += "Linje: "+str(linje)+" "+str(slutstation)+" Avgår: "+str(avgang)+"\n"
        else:
            bussen += "Buss inställd"
        i+=1
        if i > 3:
            break
    return bussen

def bana(banaLista):
    banan = "Nästa Roslagsbana som avgår:\n"
    i = 0
    for bana in banaLista:
        linje = bana["LineNumber"]
        slutstation = bana["Destination"]
        if bana["Deviations"] == None:
            avgang = bana["DisplayTime"]
            banan += "Linje: " + str(linje) + " " + str(slutstation) + " Avgår: " + str(avgang) + "\n"
        else:
            banan += "Tåg inställd"
        i += 1
        if i > 3:
            break
    banan+="*reseinfo designat av Nima*"
    return banan

def main():
    root = tk.Tk()
    root.geometry('1920x150+0+0')
    root.overrideredirect(1)
    root.configure(bg="#2f2e2e")
    text1 = tk.StringVar()
    text2 = tk.StringVar()
    text3 = tk.StringVar()
    text4 = tk.StringVar()
    text5 = tk.StringVar()
    #text6 = tk.StringVar()
    text1.set("Mörby tåget: \n")
    text2.set("Fruängen tåget:")
    text3.set("Liljeholmen tåget:")
    text4.set("Nästa Buss")
    text5.set("Nästa Roslagsbana:")
    #text6.set("Reseplaneraren\ndesignad av Nima")
    label1 = ttk.Label(
        root,
        textvariable=text1,
        font=("Helvetica", 18),
        image=tk.PhotoImage(file="/home/thecave/Dokument/resdata/T.png"),
        foreground="white",
        background="#2f2e2e"
    )
    label2 = ttk.Label(
        root,
        textvariable=text2,
        font=("Helvetica", 18),
        foreground="white",
        background="#2f2e2e"
    )
    label3 = ttk.Label(
        root,
        textvariable=text3,
        font=("Helvetica", 18),
        foreground="white",
        background="#2f2e2e"
    )
    label4 = ttk.Label(
        root,
        textvariable=text4,
        font=("Helvetica", 18),
        foreground="white",
        background="#2f2e2e"
    )
    label5 = ttk.Label(
        root,
        textvariable=text5,
        font=("Helvetica", 18),
        foreground="white",
        background="#2f2e2e"
    )

    label1.pack(expand=True, side='left', fill=tk.X)
    label2.pack(expand=True, ipadx=0, pady=0, side='left', fill=tk.X)
    label3.pack(expand=True, ipadx=0, pady=0, side='left', fill=tk.X)
    label4.pack(expand=True, ipadx=0, pady=0, side='left', fill=tk.X)
    label5.pack(expand=True, ipadx=0, pady=0, side='left', fill=tk.X)

    root.update()


    #print(norrTåg.avgang)
    #print(sydTåg.avgang)
    #print(bussen.avgang)
    #print(banan.avgang)
    while True:

        response = requests.get(
            "https://api.sl.se/api2/realtimedeparturesV4.json?key=d1139d99989d425996223d4cf03e32c8&siteid=9204&timewindow=30")
        content = response.json()
        tunnelbanaLista = content["ResponseData"]["Metros"]
        bussLista = content["ResponseData"]["Buses"]
        banaLista = content["ResponseData"]["Trams"]
        norrTåg, fruangen, liljeholmen = tunnelbana(tunnelbanaLista)
        bussen = buss(bussLista)
        banan = bana(banaLista)
        #rita(norrTåg, sydTåg, bussen, banan)
        try:
            try:
                text1.set(norrTåg)
            except:
                text1.set("Kunde inte hitta mörby tåget")
            try:
                text2.set(fruangen)
            except:
                text2.set("Kunde inte hitta ett Fruängen tåg")
            try:
                text3.set(liljeholmen)
            except:
                text3.set("Kunde inte hitta ett Liljeholmen tåg")
            try:
                text4.set(bussen)
            except:
                text4.set("Kunde inte hitta bussinfo")
            try:
                text5.set(banan)
            except:
                text5.set("Kunde inte hitta Roslagsbanainfo")
        except:
            text1.set("Error, refreshar om 10 sekunder")
            text2.set("Error, refreshar om 10 sekunder")
            text3.set("Error, refreshar om 10 sekunder")
            text4.set("Error, refreshar om 10 sekunder")
            text5.set("Error, refreshar om 10 sekunder")


        root.update()
        time.sleep(10)
        print("weeee")
        # rita grejer nedan
    root.mainloop()

main()
