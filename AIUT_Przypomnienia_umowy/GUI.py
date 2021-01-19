import tkinter as tk
from tkinter import ttk
from datetime import date, datetime

#Pobranie klasy do obslugi danych  z pliku
from DataHandler import DataHandler



class GUI():                                  
    def __init__(self, file):
        self.file = file
        self.DH = DataHandler(self.file)
        self.ErrorText = "Brak bledow"

        self.window = tk.Tk()
        self.window.title("Przypomnienia o koncach umow pracownikow")

        #Szerokosc i wysokosc glownego okna
        w = 850
        h = 370
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        
        # Oblicz srodek 
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)

        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.OrganizeGUI()
        self.window.mainloop()

#                                                                                           #
#---------------Definicje wszystkich metod odpowiedzialnych za okna aplikacji---------------#
#                                                                                           #

    #Glowne okno
    def OrganizeGUI(self):

        #----------------------Przyciski, informacje, pracownicy-----------------------------#

        #Okno z pracownikami, przyciskami edycji i scrollbarem
        containerF_L = ttk.Frame(self.window)
        canvasF_L = tk.Canvas(containerF_L, width=200) 
        scrollbarF_R = ttk.Scrollbar(containerF_L, orient="vertical", 
                                     command=canvasF_L.yview)
        scrollableF_R = ttk.Frame(canvasF_L)


        #Przyciski dodaj pracownika, odswiez, zapisz oraz informacje dodatkowe
        addonF = ttk.Frame(self.window,width=550, height=50, relief=tk.SOLID)
        buttonsF = tk.Frame(containerF_L, borderwidth=2, relief=tk.SOLID)


        #configure wywoluje gdy zmieniamy WorkersArray
        scrollableF_R.bind("<Configure>", lambda e: canvasF_L.configure(
                           scrollregion=canvasF_L.bbox("all")))


        #Rysowanie scrollbara w canvasie
        canvasF_L.create_window((0, 0), window=scrollableF_R, anchor="nw")              
        canvasF_L.configure(yscrollcommand=scrollbarF_R.set)


        #Wyswietlenie wszystkich pracownikow, oraz przyciski do edycji ich danych
        i = 0
        for x in range(len(self.DH.WorkersArray)):
            
            lbNS = tk.Label(scrollableF_R, text=self.DH.WorkersArray[x][0] +
                            " " + self.DH.WorkersArray[x][1]) 
            
            btnEd = tk.Button(scrollableF_R, text="Edytuj", bg="grey", fg="white", 
                            command=lambda i=i: self.EditWindow(i))                     #i=i zapisuje wartosc i do danej lampdy
            
            lbNS.grid(row=i,column=0, sticky=tk.W)
            btnEd.grid(row=i,column=1)
            
            i += 1


        #Przyciski Dodania pracownika | Odswiez | Zapisz
        btnAdd = tk.Button(buttonsF, text="Dodaj pracownika", bg="grey", fg="white", 
                           command=self.AddWorkerWindow)

        btnUp = tk.Button(buttonsF, text="Odswiez", bg="grey", fg="white", 
                          command= lambda: self.Update(windowNumber=1))

        btnSv = tk.Button(buttonsF, text="Zapisz", bg="grey", fg="white", 
                          command= lambda: self.DH.SaveFile(self.file, self.DH.WorkersArray))  

        lbInfo = tk.Label(addonF, 
                          text='Dodatkowe informacje: \n'+
                          'Termin w formie: "YYYY-MM-DD" albo "nok"-nieokreslony \n'+
                          'Zapisz przed wyjsciem z aplikacji', 
                          justify="left")
        
        lbError = tk.Label(addonF, text=self.ErrorText, justify="left", font=("Arial Bold", 10)) 

        #Wyswietl przyciski w buttonsF
        btnAdd.pack(anchor="sw", side="left")
        btnUp.pack(anchor="sw", side="left")
        btnSv.pack(anchor="sw", side="left")  
        lbInfo.pack()
        lbError.pack()

        #Wyswietl przyciski w framie | dodatkowe informacje
        buttonsF.pack(anchor="nw", side="bottom")
        addonF.pack(side="bottom")
        
        #Wyswietl lewe okienko zawierajace pracownikow
        containerF_L.pack(anchor="nw", side="left")
        canvasF_L.pack(side="left", fill="both", expand=True)
        scrollbarF_R.pack(side="right", fill="y")
        

        #----------------------Frame informacji o pozostalych dniach do konca umowy-----------------------------#

        #Okno informacjami o pracownikach, ich umowach, ile dni do konca i scrollbarem
        containerF_R = ttk.Frame(self.window, borderwidth=3, relief=tk.SOLID)
        canvasF_R = tk.Canvas(containerF_R, width=600) 
        scrollbarF_R = ttk.Scrollbar(containerF_R, orient="vertical", command=canvasF_R.yview)
        scrollableF_R = ttk.Frame(canvasF_R)


        #configure wywoluje gdy zmieniamy WorkersArray
        scrollableF_R.bind("<Configure>", lambda e: canvasF_R.configure(
                           scrollregion=canvasF_R.bbox("all")))


        #narysuj scrollbara w canvasie
        canvasF_R.create_window((0, 0), window=scrollableF_R, anchor="nw") 
        canvasF_R.configure(yscrollcommand=scrollbarF_R.set)


        #Wyswietlenie pracownikow | umow | terminow | dni do konca | paski
        i=0
        for ThisWorker in self.DH.WorkersArray:
            
            CopiedWorker = ThisWorker.copy()
            
            while len(CopiedWorker) > 2:
                
                #Jesli umowa jest nie jest na czas nieokreslony oblicz ile dni zostalo i ustal pasek
                if CopiedWorker[3] != 'nok':
                    days = self.DaysLeft(CopiedWorker[3])
                    colorRemainder = self.ColorByDays(days)
                
                #Jesli umowa jest na czas nieokreslony to ustaw recznie ile dni zostalo i ustw pasek
                elif CopiedWorker[3] == 'nok':
                    days = "inf"
                    colorRemainder = "gray95"

                #w kolejnych labelach wyswietl Nazwisko i Imie | Umowa i Termin | Dni | Pasek
                lbNS = tk.Label(scrollableF_R, text=CopiedWorker[0]+"  "+CopiedWorker[1]+"  ", 
                                font=("Arial Bold", 11))
                
                lbCT = tk.Label(scrollableF_R, text=CopiedWorker[2]+"  "+CopiedWorker[3]+"  ", 
                                font=("Arial Bold", 11))
                
                lbD = tk.Label(scrollableF_R, text=str(days)+" dni", font=("Arial Bold", 10),
                                border=1,relief=tk.SOLID)

                lbCl = tk.Label(scrollableF_R, width=50, bg=colorRemainder)
                
                del CopiedWorker[2:4]

                #Wyswietl te labele
                lbNS.grid(row=i, column=0, sticky="w")
                lbCT.grid(row=i, column=1, sticky="w")
                lbD.grid(row=i, column=2, sticky="w")
                lbCl.grid(row=i, column=3, sticky="w")
                
                i += 1


        #Wyswietl prawy frame
        containerF_R.pack(anchor="n",side="left")
        canvasF_R.pack(side="right", fill="both", expand=True)
        scrollbarF_R.pack(side="left", fill="y")
        


    #Uruchamiane z "Edytuj" po wybraniu przekieruj na inne metody
    def EditWindow(self,whichWorker):
        
        #Ustawienie ktory pracownik zostal wybrany do edycji
        self.DH.WorkerNumber = whichWorker  

        self.windowEdit = tk.Tk()

        #Ustalenie czy te okno zostalo juz zamkniete przez inne okno
        self.windowEditDestroyed = 0    

        #Ustaw okno na srodku ekranu
        x,y = self.CenterWindow()
        self.windowEdit.geometry('+%d+%d' % (x, y))


        #Deklaracja przyciskow okna z odniesieniem do kolejnych okien
        btnAC = tk.Button(self.windowEdit, text="Dodaj umowe", bg="grey", fg="white", 
                         command= self.AddContractWindow)

        btnED = tk.Button(self.windowEdit, text="Edytuj dane", bg="grey", fg="white", 
                         command= self.EditDataWindow)
        
        btnRC = tk.Button(self.windowEdit, text="Usun umowe", bg="grey", fg="white", 
                         command= self.RemoveContractWindow)
        
        btnRW = tk.Button(self.windowEdit, text="Usun pracownika", bg="grey", fg="white", 
                         command= self.RemoveWorkerWindow)
        
        
        #Wyswietl przyciski i wypelnij nimi przestrzen okna
        btnAC.grid(row=0,column=0, sticky="nesw")
        btnED.grid(row=0,column=1, sticky="nesw")
        btnRC.grid(row=1,column=0, sticky="nesw")
        btnRW.grid(row=1,column=1, sticky="nesw")


        self.windowEdit.mainloop()
    


    #Dodawanie umowy do wybranego pracownika (z EditWindow)
    def AddContractWindow(self):
        
        #Jesli windowEdit nie zostalo zamkniete -> zamknij
        if self.windowEditDestroyed == 0:
            self.windowEdit.destroy()
            self.windowEditDestroyed = 1


        windowAdd = tk.Tk()
        windowAdd.title("Umowa")

        #Ustaw srodek okna
        x,y = self.CenterWindow()
        windowAdd.geometry('+%d+%d' % (x, y))

        #Deklaracja informacji o pracowniku
        lbW = tk.Label(windowAdd, text="Umowa dla:"+self.DH.WorkersArray[self.DH.WorkerNumber][0]
                      +" "+self.DH.WorkersArray[self.DH.WorkerNumber][1], font=("Arial Bold", 10))
        
        lbW.grid(row=0,column=0, sticky=tk.W,columnspan=3)

        #Deklaracja tekstow do wypisania w oknie
        TextArray = ['Umowa:','Termin:']
        ExamplesArray = ['np.: UoP','np.: 2022-03-30 / nok']

        #Zbior nowej umowy pracownika
        NewContractArray = []

        i = 1
        for x in TextArray:
            
            #Deklaracja: Tekst | pole do wypelnienia | tekst
            lbT = tk.Label(windowAdd, text=x, font=("Arial Bold", 10))

            entryAddData = tk.Entry(windowAdd,width=14)
            NewContractArray.append(entryAddData)

            lbEx = tk.Label(windowAdd, text=ExamplesArray[i-1], font=("Arial Bold", 10))
            
            #Wyswietlenie
            lbT.grid(row=i,column=0, sticky=tk.W)
            entryAddData.grid(row=i,column=1)
            lbEx.grid(row=i,column=2, sticky=tk.W)          
            
            i += 1


        #Deklaracja i wyswietlenie zapisu danych
        btnSetAdd = ttk.Button(windowAdd, text="Zatwierdz dane", 
                              command= lambda: self.DH_SND_Update(mode=1,NewData=NewContractArray))
        
        btnSetAdd.grid(row=i,column=1)        

        windowAdd.mainloop()


    #Edytowanie danych pracownika (z EditWindow)
    def EditDataWindow(self):
        
        #Jesli windowEdit nie zostalo zamkniete -> zamknij
        if self.windowEditDestroyed == 0:
            self.windowEdit.destroy()
            self.windowEditDestroyed = 1

        windowEditData = tk.Tk()
        windowEditData.title("Dane")
        
        #Ustaw srodek okna
        x,y = self.CenterWindow()
        windowEditData.geometry('+%d+%d' % (x, y))       

        #Deklaracja i wyswietlenie informacji o pracowniku
        lbW = tk.Label(windowEditData, text="Dane pracownika:"+
                      self.DH.WorkersArray[self.DH.WorkerNumber][0]+" "+
                      self.DH.WorkersArray[self.DH.WorkerNumber][1], font=("Arial Bold", 10))

        lbW.grid(row=0,column=0,columnspan=2)

        #Deklaracja tekstow do wypisania w oknie
        TextArray = ['Nazwisko:','Imie:']
        
        #Zbior nowych danych pracownika
        NewDataArray = [] 

        #Deklaracja i wyswietlenie: tekst | Nazwisko | tekst | imie
        i = 1
        for x in TextArray:                                                                                         
            lbT = tk.Label(windowEditData, text=x, font=("Arial Bold", 10))

            entryDataN = tk.Entry(windowEditData,width=14)
            entryDataN.insert(tk.END, self.DH.WorkersArray[self.DH.WorkerNumber][i-1])
            
            lbT.grid(row=i,column=0, sticky=tk.W)
            entryDataN.grid(row=i,column=1)

            NewDataArray.append(entryDataN)
  
            i += 1


        ContractNum = 1         #Numer umowy
        LabelText = "Umowa "    #tekst do wyswietlenia

        #Deklaracja i wyswietlanie kolejnych umow pracownika
        x = 2
        while x < len(self.DH.WorkersArray[self.DH.WorkerNumber]):                                                       
            lbT = tk.Label(windowEditData, text= 
                           LabelText + "% s" % ContractNum + ":", font=("Arial Bold", 10))

            entryDataC = tk.Entry(windowEditData,width=14)
            entryDataC.insert(tk.END, self.DH.WorkersArray[self.DH.WorkerNumber][x])
            
            lbT.grid(row= i,column= 0, sticky= tk.W)
            entryDataC.grid(row=i,column=1)

            NewDataArray.append(entryDataC)


            # w zaleznosci od x tekstem jest umowa badz termin
            x += 1
            if x % 2 == 0:
                ContractNum+=1
                LabelText = "Umowa "

            elif x % 2 == 1:
                LabelText = "Termin "

            i += 1


        #Deklaracja i wyswietlenie ustawienia nowych danych
        SetButton = ttk.Button(windowEditData, text="Zatwierdz dane", 
                               command= lambda: self.DH_SND_Update(mode=2, NewData=NewDataArray))
        SetButton.grid(row=i,column=1)        


        windowEditData.mainloop()



    #Usuwanie wybranej umowy pracownika (z EditWindow)
    def RemoveContractWindow(self):
        
        #Jesli windowEdit nie zostalo zamkniete -> zamknij
        if self.windowEditDestroyed == 0:
            self.windowEdit.destroy()
            self.windowEditDestroyed = 1

        self.windowRC = tk.Tk()
        self.windowRC.title("Usun umowe")      
        
        #Ustaw srodek okna
        x,y = self.CenterWindow()
        self.windowRC.geometry('+%d+%d' % (x, y))
        
        lbT = tk.Label(self.windowRC, text="Umowy pracownika:"+
                       self.DH.WorkersArray[self.DH.WorkerNumber][0]+" "+
                       self.DH.WorkersArray[self.DH.WorkerNumber][1], font=("Arial Bold", 10))

        lbT.grid(row=0,column=0,columnspan=2)  

        #Deklaracja i wyswietlenie kolejnych umow do usuniecia
        i=2
        while i < len(self.DH.WorkersArray[self.DH.WorkerNumber]):                                                        
            
            lbC = tk.Label(self.windowRC, text= self.DH.WorkersArray[self.DH.WorkerNumber][i], 
                           font=("Arial Bold", 10))
            
            lbTr = tk.Label(self.windowRC, text= self.DH.WorkersArray[self.DH.WorkerNumber][i+1], 
                            font=("Arial Bold", 10))

            btnR = tk.Button(self.windowRC, text="Usun", bg="grey", fg="white", 
                             command=lambda i=i: self.DH_RD_Update(mode=1,index=i))
            

            lbC.grid(row= i,column= 0, sticky= tk.W)
            lbTr.grid(row= i,column= 1, sticky= tk.W)
            btnR.grid(row=i,column=2)
            
            i = i+2


        self.windowRC.mainloop()


    #Usuwanie wybranego pracownika (z EditWindow)
    def RemoveWorkerWindow(self):
        
        #Jesli windowEdit nie zostalo zamkniete -> zamknij
        if self.windowEditDestroyed == 0:
            self.windowEdit.destroy()
            self.windowEditDestroyed = 1

        self.windowRW = tk.Tk()
        self.windowRW.title("Pracownik")      
        
        #Ustaw srodek okna
        x,y = self.CenterWindow()
        self.windowRW.geometry('+%d+%d' % (x, y))
        
        #Deklaracja i wyswietlenie pracownika i opcji usuniecia
        lbW = tk.Label(self.windowRW, text="Pracownik: " + self.DH.WorkersArray[self.DH.WorkerNumber][0] +
                      " " + self.DH.WorkersArray[self.DH.WorkerNumber][1], font=("Arial Bold", 10)) 

        btnR = tk.Button(self.windowRW, text="Usun", bg="grey", fg="white", 
                        command= lambda:  self.DH_RD_Update(mode=2))
        
        
        lbW.grid(row=0,column=0,columnspan=2) 
        btnR.grid(row=0,column=2)


        self.windowRW.mainloop()


    #dodanie pracownika (z OrganizeGUI)
    def AddWorkerWindow(self):
        
        windowAdd = tk.Tk()
        windowAdd.title("Dodaj pracownika")
        
        #Ustaw srodek ekranu
        x,y = self.CenterWindow()
        windowAdd.geometry('+%d+%d' % ( x, y))
        
        #Tekst do wyswietlenia
        TextArray = ['Nazwisko:','Imie:']
        ExamplesArray = ['np.: Kowalski','np.: Jan']

        #Zapis nowych danych
        NewWorkerArray = []
        
        #Deklaracja i wyswietlenie: Tekst | pole do wypisania
        i = 0
        for x in TextArray:
            lbT = tk.Label(windowAdd, text=x, font=("Arial Bold", 10))

            entryAddData = tk.Entry(windowAdd,width=14)
            NewWorkerArray.append(entryAddData)

            lbEx = tk.Label(windowAdd, text=ExamplesArray[i], font=("Arial Bold", 10))
            
            lbT.grid(row=i,column=0, sticky=tk.W)
            entryAddData.grid(row=i,column=1)
            lbEx.grid(row=i,column=2, sticky=tk.W)     

            i += 1


        #Deklaracja i wyswietlenie przycisku do zapisu nowych danych
        SetAddButton = ttk.Button(windowAdd, text="Zatwierdz dane", 
                                  command=lambda: self.DH_SND_Update(mode=3,NewData=NewWorkerArray))
        SetAddButton.grid(row=i,column=1)

        windowAdd.mainloop()


#                                                                           #
#---------------Definicje pozostalych metod potrzebnych w GUI---------------#
#                                                                           #

    #Wywolanie RemoveData z DataHandler i pozniejszy update okien, 
    #mode=1 -> usun umowe, mode=2 -> usun pracownika 
    def DH_RD_Update(self,mode,index=2):
        
        self.DH.RemoveData(mode,index)
        
        if mode == 1:
            self.Update(windowNumber=2)

        if mode == 2:
            self.Update(windowNumber=3)


    #Wywolanie SetNewData z DataHandler oraz odswiezenie okien
    #mode=1 -> dodaj umowe, mode=2 -> zmiana danych pracownika, mode=3 -> dodaj pracownika 
    def DH_SND_Update(self,mode,NewData):

        #Sprawdzenie czy termin ma dobra forme, jezeli tak to zapisze dane
        DateCheck = self.DH.SetNewData(mode=mode,NewData=NewData)
        
        #Jezeli jest blad wypisz go na glownym oknie
        if DateCheck:
            self.ErrorText = 'Error: Bledny zapis "Termin"!'
        
        else:
            self.ErrorText = 'Brak bledow'
        
        self.Update(windowNumber=1)



    #Wyliczenie srodka monitoru z malym przesunieciem (troche oszustwo)
    def CenterWindow(self):
        
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()

        # obliczenie srodka i przesuniecie
        x = (ws/2) - 100
        y = (hs/2) - 100
        return x, y        

        

    #Ponowne uruchomienie okien po wyczyszczeniu starych widgetow
    def Update(self,windowNumber):

        #Posortuj nowe dane po nazwiskach
        self.DH.WorkersArray.sort()

        #Odswiez OrganizeGUI
        if windowNumber == 1:

            #Zwraca liste wszystkich widgetow z window
            WidgetsList = self.window.winfo_children()          
            
            for item in WidgetsList :
                
                if item.winfo_children() :
                    WidgetsList.extend(item.winfo_children())   
            
            for item in WidgetsList:
                item.pack_forget()

            self.OrganizeGUI()


        #Odswiez RemoveContractWindow & OrganizeGUI
        elif windowNumber == 2:
            self.Update(windowNumber=1)
            self.windowRC.destroy()
            self.RemoveContractWindow()
            

        #Odswiez RemoveWorker & OrganizeGUI
        elif windowNumber == 3:
            self.Update(windowNumber=1)
            self.windowRW.destroy()
            

        else:
            return



    #Obliczenie ile dni zostalo do konca umowy
    def DaysLeft(self,Termin):
        
        dateTermin = datetime.strptime(Termin, '%Y-%m-%d').date()   
        today = date.today()

        delta = dateTermin - today
        return delta.days



    #Wybranie koloru paska na podstawie dni do konca umowy
    def ColorByDays(self,days):      
       
        if days <= 1:
            bg = "black"
        elif days <= 7:
            bg = "red"
        elif days <= 30:
            bg = "yellow"  
        elif days <= 90:
            bg = "green"  
        elif days > 90:
            bg = "light grey"                                       
        return bg



