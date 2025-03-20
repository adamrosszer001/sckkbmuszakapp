import tkinter as tk
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyperclip
from datetime import datetime, timedelta
from datetime import time
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from googleapiclient.discovery import build
from google.oauth2 import service_account


hivasok = []
cimke = None
datum2 = None
szazalek = 0
holnap3 = None
ma = datetime(2025, 1, 1)
osszes = 0
bmuszak = False
ido_a = time(0,0,0)
proba_datum = datetime(2025, 1, 1)
names_l = {}
perces = 0
regi = False
hivas_3_regi = []
elfogadva = 0
elutasitva = 0
perces_szamok_l = []
sorok2 = []
b_hivasok = []
adat_window = None
kulombsegek = []

utvonal_loc = "utvonalak.txt"


service_account_path =  "service_account.json"

print("B Műszak APP 1.0.2")

def mentés():
    global hivasok, cimke, osszes

    if cimke is None:
        print("Hiba: Nincs elérhető címke.")
        return
    
    fájlnev = "mentes.txt"
    tartalom = cimke.cget("text")
    
    sorok = tartalom.split("\n")
    if len(sorok) < 5:
        print("Hiba: Nem megfelelő adatstruktúra.")
        return

    datum = sorok[0].split(": ")[1]  
    elutasitva = sorok[2].split(": ")[1]  
    elfogadva = sorok[3].split(": ")[1]  
    szazalek = sorok[4].split(": ")[1]  

    print(f"Mentés adatok: {datum}, {osszes}, {elutasitva, elfogadva, szazalek}")

    uj_sor = f"{datum};{osszes};{elutasitva};{elfogadva};{szazalek}\n"

    

    with open(fájlnev, "r", encoding="utf-8") as fájl:
        sorok = fájl.readlines()

    uj_sorok = []
    beirt = False
    for sor in sorok:
        if datum in sor:
            print("Frissítjük a meglévő bejegyzést.")
            uj_sorok.append(uj_sor)
            beirt = True
        else:
            uj_sorok.append(sor)

    if not beirt:
        print("Új adat hozzáadása.")
        uj_sorok.append(uj_sor)

    with open(fájlnev, "w", encoding="utf-8") as fájl:
        fájl.writelines(uj_sorok)

    print("Mentés sikeres!")


def upload_to_google_docs(file_content):
    SCOPES = ['https://www.googleapis.com/auth/documents']
    SERVICE_ACCOUNT_FILE = 'service_account.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('docs', 'v1', credentials=credentials)

    # Create a new Google Docs document
    document = service.documents().create(body={
        'title': 'B Műszak APP LOG'
    }).execute()
    document_id = "1ja49EPTP9rYqozwwMzdkC-iAWOqn8AB2uJXQzqlUQLg"

    # Prepare the requests to insert the content into the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': file_content
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()

def browseFiles():
    global cimke, regi, perces_szamok_l, sorok2, elfogadva, elutasitva, b_hivasok, adat_window
    global datum2, szazalek, holnap3, ma, datum, hnap, osszes, bmuszak, hivasok, names_l, perces, kulombsegek
    file_n = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))

    adat_window = tk.Tk()
    adat_window.title("B Műszak APP || Kiértékelés")
    adat_window.configure(background="#535251")
    frame = tk.Frame(adat_window)
    frame.grid(row=5)
    frame.destroy()
    hivas_3 = []
    
    with open(file_n, "r", encoding="utf-8") as adat:
        file_content = adat.read()
        sorok = file_content.splitlines()
        datum = None
        sorok2 = []
        hivas_3_regi = []
        for sor in sorok:
            adatok = [elem.strip() for elem in sor.split("\t") if elem.strip()]
            if len(adatok) < 4:
                continue
            if len(adatok) > 4:
                sorok.append(adatok[0])
                hivasok.append((adatok[0], adatok[2], adatok[1]))
               
                datum = adatok[3]
                datum = datum.split(" ")
                ido_e = datum[3].split(":")
                regi = True
            else:
                sorok.append(adatok[0])
                hivasok.append((adatok[0], adatok[2], adatok[1]))
                
                datum = adatok[2]
                datum = datum.split(" ")
                ido_e = datum[3].split(":")
                regi = False

            ido_a = time(hour=int(ido_e[0]), minute=int(ido_e[1]), second=int(ido_e[2]))
            if time(18, 30, 0) < ido_a < time(21, 59, 59):
                sorok2.append(adatok[0])
                hivas_3.append(adatok)
                hivas_3_regi.append(adatok[2])
                osszes += 1
                bmuszak = True

    datum2 = datum[0] + datum[1] + datum[2]
    ma_ev = datum[0][:-1]
    ma_ho = datum[1][:-1]
    ma_nap = datum[2][:-1]
    ma = datetime(int(ma_ev), int(ma_ho), int(ma_nap))
    nap2 = datum[2]
    nap3 = nap2[:-1]
    nap_int = int(nap3) + 1
    hnap = str(nap_int)
    holnap3 = datum[1]  + hnap

    adat.close()
    osszhivas = 0
    elutasitva = 0
    elfogadva = 0

    if bmuszak:
        datum_formatum = "%Y. %m. %d. %H:%M:%S"
        if not regi:
            for i in hivas_3:
                elfog = i[2].split(" ")
                elfog_i = elfog[3].split(":")
                elfog = datetime(int(elfog[0][:-1]), int(elfog[1][:-1]), int(elfog[2][:-1]), int(elfog_i[0]), int(elfog_i[1]), int(elfog_i[2]))
                beerkez = i[3].split(" ")
                beerkez_i = beerkez[3].split(":")
                beerkez = datetime(int(beerkez[0][:-1]), int(beerkez[1][:-1]), int(beerkez[2][:-1]), int(beerkez_i[0]), int(beerkez_i[1]), int(beerkez_i[2]))
                kulombseg = elfog - beerkez 
                if i[0] == "Lemondott":
                    if kulombseg < timedelta(minutes=1.5):
                        perces += 1
                        b_hivasok.append("1 perc alatt lemondott")
                    else:
                        elutasitva += 1
                        b_hivasok.append("Lemondott")
                else:
                    elfogadva += 1
                    b_hivasok.append(i[0])
                szazalek = round((elfogadva + perces) / len(sorok2) * 100, 1)
                kulombsegek.append(kulombseg.total_seconds())
        else:
            elfogadva = sum(1 for i in hivas_3_regi if i == "Accepted")
            elutasitva = sum(1 for i in hivas_3_regi if i == "Cancelled")
            elutasitva = elutasitva - len(perces_szamok_l)
            szazalek = round(elfogadva / len(sorok2) * 100, 1)

        for i in sorok2:
            osszhivas += 1

        names_l = {}
        for i in b_hivasok:
            nev = i
            if nev in names_l:
                names_l[nev] += 1
            else:
                names_l[nev] = 1
                
    else:
        szazalek = 0
        elfogadva = 0
        elutasitva = 0
    if regi:
        adat_window.title("B Műszak APP")
        perces_gomb = tk.Button(adat_window, text="1 perces lemondott hozzáadása", command=perces_def)
        perces_gomb.pack(pady=5)
    else:
        adat_window.geometry("500x300")
        
        if regi:
            cimke = tk.Label(adat_window, text=f"Dátum: {datum2} \nÖsszes hívás: {osszhivas}\nLemondott hívások: {elutasitva}\nElfogadott hívások: {elfogadva}\n 1 perces lemondottak: {perces}\nSzázalék: {szazalek}%", fg="white")
        else:
            cimke = tk.Label(adat_window, text=f"Dátum: {datum2} \nÖsszes hívás: {osszhivas}\nLemondott hívások: {elutasitva}\nElfogadott hívások: {elfogadva}\n 1 perces lemondottak: {perces}\nSzázalék: {szazalek}% \nÁtlagosan egy hívás {sum(kulombsegek) / len(kulombsegek) if kulombsegek else 0:.2f} másodpercig volt bent.", fg="white")
        cimke.configure(background="#535251")
        cimke.pack(pady=10)

        kiiras_gomb = tk.Button(adat_window, text="Kiírás", command=masol_vagolapra)
        kiiras_gomb.pack(pady=5)

        mentes_gomb = tk.Button(adat_window, text="Mentés", command=lambda: feltolt_google_sheets(datum2, osszhivas, elutasitva, elfogadva, szazalek, perces))
        mentes_gomb.pack(pady=5)

        button_jelenlet = tk.Button(adat_window, text="Jelenlét", command=open_jelenlet_window)
        button_jelenlet.pack(pady=10)

        adat_window.mainloop()
        print(szazalek, holnap3, ma, ido_a)

    upload_to_google_docs(file_content)


def perces_def():
    global names_l, hivas_3_regi, elfogadva, elutasitva, perces_szamok_l
    perces_window = tk.Tk()
    root.destroy()
    perces_window.geometry("600x400")
    perces_window.title("B MŰSZAK APP || 1 perces hívás dokumentálása")
    perces_window.configure(background="#535251")
    tk.Label(perces_window, text="Hívás(ok) azonosítója (,-vel elválasztva add meg). Ha nics akkor hagyd üresen!",fg="white", background="#535251").grid(row=0, column=1)
    perces_szamok = tk.Entry(perces_window)
    perces_szamok.grid(row=0, column=2)


    def perces_szamol():
        global sorok2, elutasitva, elfogadva, names_l, hivas_3_regi
        perces_szamok_l = []
        perces_szamok_l = perces_szamok.get()
        perces_szamok_l = perces_szamok_l.split(",")
        perces_window.destroy()

        if "" in perces_szamok_l:
            perces = 0
            elutasitva2 = elutasitva
        else:
            elutasitva2 = elutasitva-len(perces_szamok_l)
            perces = len(perces_szamok_l)
        
        names_l = {}
        for i in sorok2:
            nev = i
            if nev in names_l:
                names_l[nev] += 1
            else:
                names_l[nev] = 1


        adat2_window = tk.Tk()
        adat2_window.geometry("500x300")
        adat2_window.title("B Műszak APP2")

        adat2_window.configure(background="#535251")
        sorok2_db = len(sorok2)
        szazalek = round((elfogadva+perces) / len(sorok2) * 100, 1)

        cimke = tk.Label(adat2_window, text=f"Dátum: {datum2} \nÖsszes hívás: {sorok2_db}\nLemondott hívások: {elutasitva2}\nElfogadott hívások: {elfogadva}\n 1 perces lemondottak: {perces}\nSzázalék: {szazalek}%", fg="white", background="#535251")
        cimke.pack(pady=10)

        kiiras_gomb = tk.Button(adat2_window, text="Kiírás", command=masol_vagolapra)
        kiiras_gomb.pack(pady=5)

        mentes_gomb = tk.Button(adat2_window, text="Mentés", command=lambda: feltolt_google_sheets(datum2, sorok2_db, elutasitva, elfogadva, szazalek, perces))
        mentes_gomb.pack(pady=5)

        button_jelenlet = tk.Button(adat2_window, text="Jelenlét", command=open_jelenlet_window)
        button_jelenlet.pack(pady=10)

        adat2_window.mainloop()
        print(szazalek, holnap3, ma, ido_a, names_l)


    perces_gomb2 = tk.Button(perces_window, text="Mentés", command=perces_szamol)
    perces_gomb2.grid(row=1, column=1)


def feltolt_google_sheets(datum, osszes, elutasitva, elfogadva, szazalek, perces):
    try:
        f = open("service_account.json", 'r')
        f.read()
        filename_service = "service_account.json"
    except:
           filename_service = "service_account.json"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename_service, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("B Műszak Hivatalos Adatbázis")  
    sheet = spreadsheet.worksheet("Mentés")

    osszes_sor = sheet.get_all_values()

    felulirando_sor_index = None
    for i, sor in enumerate(osszes_sor):
        if sor[0] == datum: 
            felulirando_sor_index = i
            break

    if felulirando_sor_index is not None:
        sor_szam = felulirando_sor_index + 1
        sheet.update(values=[[datum, osszes, elutasitva, elfogadva, szazalek]], range_name=f"A{sor_szam}:E{sor_szam}")
    else:
        sheet.append_row([datum, osszes, elutasitva, elfogadva, szazalek, perces])

    

def get_hivasszamok_tartalom():
    global names_l
    filename_service = "service_account.json"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename_service, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("B Műszak Hivatalos Adatbázis")

    hivasszamok_sheet = spreadsheet.worksheet("Tagok")

    nevek = hivasszamok_sheet.col_values(22)[1:]
    hivasszamok = hivasszamok_sheet.col_values(23)[1:] 

    tartalom = ""
    for nev, hivas in zip(nevek, hivasszamok):
        tartalom += f"{nev}: {hivas}\n"

    return tartalom

def get_hivasszamok_tartalom2():
    global names_l
    filename_service = "service_account.json"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename_service, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("B Műszak Hivatalos Adatbázis")

    hivasszamok_sheet = spreadsheet.worksheet("Tagok")

    nevek = hivasszamok_sheet.col_values(1)[1:]
    hivasszamok = hivasszamok_sheet.col_values(2)[1:] 

    tartalom = ""
    for nev, hivas in zip(nevek, hivasszamok):
        tartalom += f"{nev}: {hivas}\n"

    return tartalom

def masol_vagolapra():
    global names_l
    pyperclip.copy(kiiras(holnap3, szazalek, ma, holnap3))    
    print("Szöveg másolva a vágólapra!")


def kiiras(holnap, szazalek, ma, holnap3):
    global names_l, perces
    if float(szazalek) > 89:
        eredmeny = "Szép munka! :clap:"
    if float(szazalek) == 100:
        eredmeny = "Tökéletes nap! Gratulálok :tada:"
    else:
        eredmeny = ""

    names_l_str = ""
    for key, value in names_l.items():
        if key == "Lemondott" or key == "1 perc alatt lemondott":
            continue
        else:
            names_l_str += f"{key}: {value}\n"

    holnap3 = holnap3.split(".")
    if int(holnap3[1]) < 10:
        holnap3[1] = "0" + holnap3[1]
    holnap3 = ".".join(holnap3) 

    if elutasitva >= 4:
        lemond_jel = ":exclamation:"
    elif elutasitva >= 8:
        lemond_jel = ":bangbang:" 
    elif elutasitva <= 3:
        lemond_jel = ":clap:"

    if regi:
        if ma.weekday() == 4:
            kiiras_szoveg = f"**Kedves B műszak!**\n\n**Mai műszak:** ({ma.strftime('%Y-%m-%d')})\n\n{names_l_str} \n Lemondott hívások: {elutasitva} {lemond_jel} \n 1 percen belül lemondott hívások: {perces} \n\n**Mutatom a heti zárást:**\n\n{get_hivasszamok_tartalom2()}\n\nA mai műszak eredményessége: {szazalek}% \n {eredmeny}\n\nKérlek jelezzétek a holnapi ({holnap3}) nappal kapcsolatban! \n :nem: - Nem leszek \n :igen: - Leszek \n\n :sckkkarika: B Műszak Vezetőség :sckkkarika:"
        elif ma.weekday() == 3:
            kiiras_szoveg = f"**Kedves B műszak!**\n\n**Mai műszak:** ({ma.strftime('%Y-%m-%d')})\n\n{names_l_str} \n Lemondott hívások: {elutasitva} {lemond_jel} \n 1 percen belül lemondott hívások: {perces}\n\n**Összesen a héten:** \n**(Leintések nélkül)**\n\n{get_hivasszamok_tartalom()}\n\nHolnap elérkezik a heti zárás. Megkérünk mindenkit hogy holnap azaz ({holnap3}) 22:00ig adjátok le valamelyik műszakvezetőnek a kasszazárásotokat. \n\n A mai műszak eredményessége: {szazalek}% \n {eredmeny}\n\n Kérlek jelezzétek a holnapi ({holnap}) nappal kapcsolatban! \n :nem: - Nem leszek \n :igen: - Leszek \n\n :sckkkarika: B Műszak Vezetőség :sckkkarika:"
        else:
            kiiras_szoveg = f"**Kedves B műszak!**\n\n**Mai műszak:** ({ma.strftime('%Y-%m-%d')})\n\n{names_l_str} \n Lemondott hívások: {elutasitva} {lemond_jel} \n 1 percen belül lemondott hívások: {perces}\n\n**Összesen a héten:** \n**(Leintések nélkül)**\n\n{get_hivasszamok_tartalom()}\n \nA mai műszak eredményessége: {szazalek}% \n {eredmeny}\n\nKérlek jelezzétek a holnapi ({holnap3}) nappal kapcsolatban! \n :nem: - Nem leszek \n :igen: - Leszek \n\n :sckkkarika: B Műszak Vezetőség :sckkkarika:"

    else:
        if ma.weekday() == 4:
            kiiras_szoveg = f"**Kedves B műszak!**\n\n**Mai műszak:** ({ma.strftime('%Y-%m-%d')})\n\n{names_l_str} \n Lemondott hívások: {elutasitva} {lemond_jel} \n 1 percen belül lemondott hívások: {perces} \n\n**Mutatom a heti zárást:**\n\n{get_hivasszamok_tartalom2()}\n\nA mai műszak eredményessége: {szazalek}% \n {eredmeny} \nÁtlagosan egy hívás {sum(kulombsegek) / len(kulombsegek) if kulombsegek else 0:.2f} másodpercig volt bent.\n\nKérlek jelezzétek a holnapi ({holnap3}) nappal kapcsolatban! \n :nem: - Nem leszek \n :igen: - Leszek \n\n :sckkkarika: B Műszak Vezetőség :sckkkarika:"
        elif ma.weekday() == 3:
            kiiras_szoveg = f"**Kedves B műszak!**\n\n**Mai műszak:** ({ma.strftime('%Y-%m-%d')})\n\n{names_l_str} \n Lemondott hívások: {elutasitva} {lemond_jel} \n 1 percen belül lemondott hívások: {perces}\n\n**Összesen a héten:** \n**(Leintések nélkül)**\n\n{get_hivasszamok_tartalom()}\n\nHolnap elérkezik a heti zárás. Megkérünk mindenkit hogy holnap azaz ({holnap3}) 22:00ig adjátok le valamelyik műszakvezetőnek a kasszazárásotokat. \n\n A mai műszak eredményessége: {szazalek}% \n {eredmeny} \nÁtlagosan egy hívás {sum(kulombsegek) / len(kulombsegek) if kulombsegek else 0:.2f} másodpercig volt bent. \n\n Kérlek jelezzétek a holnapi ({holnap}) nappal kapcsolatban! \n :nem: - Nem leszek \n :igen: - Leszek \n\n :sckkkarika: B Műszak Vezetőség :sckkkarika:"
        else:
            kiiras_szoveg = f"**Kedves B műszak!**\n\n**Mai műszak:** ({ma.strftime('%Y-%m-%d')})\n\n{names_l_str} \n Lemondott hívások: {elutasitva} {lemond_jel} \n 1 percen belül lemondott hívások: {perces}\n\n**Összesen a héten:** \n**(Leintések nélkül)**\n\n{get_hivasszamok_tartalom()}\n \nA mai műszak eredményessége: {szazalek}% \n {eredmeny} \nÁtlagosan egy hívás {sum(kulombsegek) / len(kulombsegek) if kulombsegek else 0:.2f} másodpercig volt bent. \n\nKérlek jelezzétek a holnapi ({holnap3}) nappal kapcsolatban! \n :nem: - Nem leszek \n :igen: - Leszek \n\n :sckkkarika: B Műszak Vezetőség :sckkkarika:"
    print(szazalek, holnap3, ma)
    return kiiras_szoveg


def fetch_names_from_google_sheets():
    filename_service = "service_account.json"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename_service, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("B Műszak Hivatalos Adatbázis")
    hivasszamok_sheet = spreadsheet.worksheet("Tagok")
    nevek = hivasszamok_sheet.col_values(1)[1:]
    return nevek


def open_jelenlet_window():
    create_jelenlet_window()

def save_attendance():
    global attendance_vars
    attendance_data = []
    for name, var in attendance_vars.items():
        attendance_data.append((name, var.get()))
    upload_attendance_to_google_sheets(attendance_data)

def upload_attendance_to_google_sheets(attendance_data):
    global datum, filename_service
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        f = open("service_account.json", 'r')
        f.read()
        filename_service = "service_account.json"
    except:
        filename_service =  "service_account.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename_service, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("B Műszak Hivatalos Adatbázis")
    attendance_sheet = spreadsheet.worksheet("Jelenlét")

    clipboard_content = ""  

    for name, status in attendance_data:
        if status == "Jelen":
            status_symbol = "x"
        elif status == "Jelzett":
            status_symbol = "-"
        elif status == "Nem jelzett":
            status_symbol = "--"
        elif status == "Inaktivitás":
            status_symbol = "i"
        elif status == "Ünnepnap":
            status_symbol = "ü"
        elif status == "Mentorálás":
            status_symbol = "m"
        elif status == "Nem tag":
            status_symbol = "k"            
        else:
            status_symbol = status

        clipboard_content += f"{status_symbol}\n"

    pyperclip.copy(clipboard_content)
    print("Adatok másolva a vágólapra!")

    clipboard_content = ""

    for name, status in attendance_data:
        if status == "Jelen":
            status_symbol = "x"
        elif status == "Jelzett":
            status_symbol = "-"
        elif status == "Nem jelzett":
            status_symbol = "--"
        elif status == "Inaktivitás":
            status_symbol = "i"
        elif status == "Ünnepnap":
            status_symbol = "ü"
        elif status == "Mentorálás":
            status_symbol = "m"
        elif status == "Nem tag":
            status_symbol = "k"            
        else:
            status_symbol = status

        clipboard_content += f"{status_symbol}\n"
        canvas = tk.Canvas(jelenlet_window)
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )


def create_jelenlet_window():
    global jelenlet_window, attendance_vars, ido_a, datum
    jelenlet_window = tk.Tk()
    jelenlet_window.geometry("800x400")
    jelenlet_window.title("B Műszak APP || Jelenlét")

    canvas = tk.Canvas(jelenlet_window)
    scrollbar = tk.Scrollbar(jelenlet_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    nevek = fetch_names_from_google_sheets()
    attendance_vars = {}
    for nev in nevek:
        frame = tk.Frame(scrollable_frame)
        frame.pack(fill='x', pady=5)

        label = tk.Label(frame, text=nev, width=30, anchor='w')
        label.pack(side='left')

        options = ["Jelen", "Jelzett", "Nem jelzett", "Mentorálás", "Ünnepnap", "Inaktivitás", "Nem tag"]
        var = tk.StringVar(frame)
        var.set("Nem jelzett")
        for i in hivasok:
            ido_a = i[1]
            ido_a = ido_a.split(" ")
            ido_e = ido_a[3].split(":")
            ido_t = time(int(ido_e[0]), int(ido_e[1]), int(ido_e[2]))

            if nev == i[0] and time(18, 29, 0) < ido_t < time(22, 0, 0):
                var.set("Jelen")
        dropdown = tk.OptionMenu(frame, var, *options)
        dropdown.pack(side='right')

        attendance_vars[nev] = var

    save_button = tk.Button(jelenlet_window, text="Mentés", command=save_attendance)
    save_button.pack(pady=10)

def probavizsgawindow():
    global proba_utvonal, proba_datum, utvonal_loc

    probawindow = tk.Tk()
    probawindow.geometry("700x500")
    tk.Label(probawindow, text="Útvonal: ").grid(row=2, column=1)

    tk.Label(probawindow, text="Vizsgázó neve:").grid(row=0, column=1)
    tk.Label(probawindow, text="Dátum:").grid(row=1, column=1)
    proba_nev = tk.Entry(probawindow)
    proba_datum = tk.Entry(probawindow)
    proba_nev.grid(row=0, column=2)
    proba_datum.grid(row=1, column=2)

    def set_today_date():   
        today_date = datetime.today().strftime('%Y-%m-%d')
        proba_datum.delete(0, tk.END)
        proba_datum.insert(0, today_date)
        


    tk.Button(probawindow, text="MA", command=set_today_date).grid(row=1, column=3)
    proba_utvonal_label = tk.Label(probawindow, text="Útvonal: ").grid(row=2, column=1)
    proba_utvonal = ttk.Combobox(probawindow, values=["A", "B", "C", "D", "E", "F"])
    proba_utvonal.grid(row=2, column=2)

    def utvonal_t():
        global proba_datum, proba_utvonal, utvonal_loc

        proba_datum_value = proba_datum.get()
        proba_utvonal_value = proba_utvonal.get()
        proba_datum_value = str(proba_datum_value)


        with open(utvonal_loc, "r", encoding="utf8") as utvonalak_forras:
            utvonal_8 = []
            utvonal_16 = []
            utvonal_24 = []
            utvonal_31 = []
            utvonalak = []

            j = 0
            for i in utvonalak_forras:
                if i == "1-8" or i == "9-16" or i == "17-24" or i == "25-31":
                    j = j
                else:
                    if 0 <= j < 6:
                        utvonal_8.append(i)
                    elif 5 < j < 12:
                        utvonal_16.append(i)
                    elif 11 < j < 19:
                        utvonal_24.append(i)
                    elif 17 < j:
                        utvonal_31.append(i)

                utvonalak.append(i)
                j += 1

        p_utvonal_n = None
        for sor in utvonalak:
            p_datum2 = proba_datum_value[-2:]
            p_datum2 = int(p_datum2)
            if p_datum2 < 9:
                for i in range(len(utvonal_8)):
                    if utvonal_8[i][0] == proba_utvonal_value:
                        p_utvonal_n = utvonal_8[i]
            elif 8 < p_datum2 < 17:
                for i in range(len(utvonal_16)):
                    if utvonal_16[i][0] == proba_utvonal_value:
                        p_utvonal_n = utvonal_16[i]
            elif 16 < p_datum2 < 25:
                for i in range(len(utvonal_24)):
                    if utvonal_24[i][0] == proba_utvonal_value:
                        p_utvonal_n = utvonal_24[i]
            elif 24 < p_datum2 < 31:
                for i in range(len(utvonal_31)):
                    if utvonal_31[i][0] == proba_utvonal_value:
                        p_utvonal_n = utvonal_31[i]

            if p_utvonal_n:
                p_utvonal_n = p_utvonal_n.split(";")
                tk.Label(probawindow, text=f"Elméleti lap 1: (pont)").grid(row=4, column=1)
                lap_1_entry = tk.Entry(probawindow)
                lap_1_entry.grid(row=4, column=2)

                tk.Label(probawindow, text=f"Elméleti lap 2: (pont)").grid(row=5, column=1)
                lap_2_entry = tk.Entry(probawindow)
                lap_2_entry.grid(row=5, column=2)

                tk.Label(probawindow, text=f"Az első uticél: {p_utvonal_n[1]}").grid(row=6, column=1)
                tk.Label(probawindow, text=f"KM: ").grid(row=7, column=1)
                km_1 = tk.Entry(probawindow)
                km_1.grid(row=7, column=2)

                tk.Label(probawindow, text=f"A második uticél: {p_utvonal_n[4]}").grid(row=8, column=1)
                tk.Label(probawindow, text=f"KM: ").grid(row=9, column=1)
                km_2 = tk.Entry(probawindow)
                km_2.grid(row=9, column=2)

                tk.Label(probawindow, text=f"KRESZ hibapontok:").grid(row=10, column=1)
                kresz_hiba = tk.Entry(probawindow)
                kresz_hiba.grid(row=10, column=2)

                def vizsgaertekeles():
                    print(p_utvonal_n)
                    km_1_e = km_1.get()
                    km_2_e = km_2.get()
                    kresz_hiba_e = kresz_hiba.get()
                    kresz_hiba_e = int(kresz_hiba_e)
                    km_1_ideal = p_utvonal_n[2][:-2]
                    km_1_max = p_utvonal_n[3][:-3]
                    km_2_ideal = p_utvonal_n[5][:-2]
                    km_2_max = p_utvonal_n[6][:-3]
                    lap_1 = lap_1_entry.get()
                    lap_2 = lap_2_entry.get()

                    print(km_1_ideal, km_1_max)

                    if float(km_1_e) > float(km_1_max):
                        eredmeny_1 = 0
                    if float(km_1_ideal) < float(km_1_e) < float(km_1_max) and (float(km_1_ideal) / 100) * 1.15 > float(km_1_e):
                        eredmeny_1 = 10
                    if (float(km_1_ideal) / 100) * 1.15 <= float(km_1_e):
                        eredmeny_1 = 5
                    if float(km_1_e) == float(km_1_ideal):
                        eredmeny_1 = 10
                    if float(km_1_e) < float(km_1_ideal) - 0.3:
                        eredmeny_1 = 0

                    if float(km_2_e) > float(km_2_max):
                        eredmeny_2 = 0
                    if float(km_2_ideal) < float(km_2_e) < float(km_2_max) and (float(km_2_ideal) / 100) * 1.15 > float(km_2_e):
                        eredmeny_2 = 10
                    if (float(km_2_ideal) / 100) * 1.15 <= float(km_2_e):
                        eredmeny_2 = 5
                    if float(km_2_e) == float(km_2_ideal):
                        eredmeny_2 = 10
                    if float(km_2_e) < float(km_2_ideal) - 0.3:
                        eredmeny_2 = 0

                    osszpont = int(lap_1) + int(lap_2) + (eredmeny_1 + eredmeny_2) - kresz_hiba_e
                    maxpont = 9 + 9 + 10 + 10
                    minpont_atmento = maxpont * 0.64
                    atment = ""
                    if osszpont < minpont_atmento:
                        atment = "Sikertelen"
                    elif osszpont < 35:
                        atment = "Megfelelt"
                    elif osszpont >= 35:
                        atment = "Jól Megfelelt"

                    kiertekeles = f"Az elmélet során {int(lap_1) + int(lap_2)} pontot szerzett. \n Az első helyszínen {eredmeny_1} pontot szerzett. \n A második helszínen {eredmeny_2} pontot szerzett. \n KRESZ hibák miatt {kresz_hiba_e} pontot vesztett. \n Így a vizsga {osszpont} pont lett ami: {atment}!"
                    tk.Label(probawindow, text=kiertekeles).grid(row=12)
                    tk.Label(probawindow, text=kiertekeles).grid(row=12)
                    vizsga_ertekeles = tk.Label(probawindow, text=kiertekeles).grid(row=12)

                    filename_service = "service_account.json"
                    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                    creds = ServiceAccountCredentials.from_json_keyfile_name(filename_service, scope)
                    client = gspread.authorize(creds)
                    spreadsheet = client.open("B Műszak Hivatalos Adatbázis")
                    attendance_sheet = spreadsheet.worksheet("PróbavizsgaEredmények")
                    if attendance_sheet.col_count < 6:
                        attendance_sheet.add_cols(6 - attendance_sheet.col_count)

                    if attendance_sheet.row_count < 1:
                        attendance_sheet.add_rows(1 - attendance_sheet.row_count)

                    vizsgazo_nev = proba_nev.get()
                    vizsga_datum = proba_datum.get()
                    utvonal = proba_utvonal.get()
                    ures = ""
                    new_row = [vizsgazo_nev, utvonal, vizsga_datum, eredmeny_1, eredmeny_2, kresz_hiba_e, ures, lap_1, lap_2, osszpont, atment]
                    attendance_sheet.append_row(new_row)
                    print("Vizsga eredmények feltöltve a doksiba!")

                vizsga_end = tk.Button(probawindow, text="Vizsga kiértékelése", command=vizsgaertekeles)
                vizsga_end.grid(row=11, column=1)

    proba_gomb = tk.Button(probawindow, text="OK", command=utvonal_t)
    proba_gomb.grid(row=3, column=2)



root = Tk()
root.title("B MŰSZAK APP || Főoldal")

root.configure(background="#535251")
root.geometry("600x600")

img = PhotoImage(file='app.png')
root.wm_iconphoto(True, img)

min_w = 50 
max_w = 200 
cur_width = min_w 

setting_img_path = "muszak.png"
ring_img_path = "vizsga.png"
setting_img = ImageTk.PhotoImage(Image.open(setting_img_path).resize((40,40),Image.LANCZOS))
ring_img = ImageTk.PhotoImage(Image.open(ring_img_path).resize((40,40),Image.LANCZOS))

def expand():
    global cur_width, expanded
    cur_width += 10 
    rep = root.after(5,expand) 
    frame.config(width=cur_width) 
    if cur_width >= max_w: 
        expanded = True 
        root.after_cancel(rep) 
        fill()

def contract():
    global cur_width, expanded
    cur_width -= 10 
    rep = root.after(5,contract) 
    frame.config(width=cur_width) 
    if cur_width <= min_w: 
        expanded = False 
        root.after_cancel(rep) 
        fill()

def fill():
    if expanded:  
        set_b.config(text='Műszakértékelés', image=setting_img, compound='left', font=(0, 14), anchor='w')
        ring_b.config(text='Próbavizsga', image=ring_img, compound='left', font=(0, 14), anchor='w')
    else:
        set_b.config(text='', image=setting_img, compound='left', font=(0, 21), anchor='center')
        ring_b.config(text='', image=ring_img, compound='left', font=(0, 21), anchor='center')

frame = Frame(root, bg='orange', width=min_w, height=root.winfo_height())
frame.grid(row=0, column=0, rowspan=2, sticky="ns")

frame.bind('<Enter>', lambda _: expand())
frame.bind('<Leave>',lambda _: contract())

root.update() 
frame = Frame(root,bg='orange',width=min_w,height=root.winfo_height())
frame.grid(row=1,column=0, sticky="ns") 

set_b = Button(frame, image=setting_img, bg='orange',relief='flat', command=browseFiles)
ring_b = Button(frame, image=ring_img, bg='orange',relief='flat', command=probavizsgawindow)

set_b.grid(row=1,column=0,pady=50)
ring_b.grid(row=2,column=0)
frame.bind('<Enter>',lambda _: expand())
frame.bind('<Leave>',lambda _: contract())
frame.bind('<Enter>',lambda e: expand())
frame.bind('<Leave>',lambda e: contract())

frame.grid_propagate(False)

root.mainloop()
