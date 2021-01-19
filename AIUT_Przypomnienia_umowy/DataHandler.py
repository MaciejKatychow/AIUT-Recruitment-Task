from datetime import date, datetime

# Modul importowany przez GUI
# Operowanie na danych o pracownikach i ich umowach z pliku "Zapis_danych.txt"
# w formie: [Nazwisko, Imie, Umowa, Termin, Umowa, Termin ...]
# WorkersArray - aktualna lista z wszystkimi pracownikami i ich danymi
# WorkerNumber - wykorzystywany jako indeks WorkersArray do pracy nad danymi wybranego pracownika

class DataHandler:
    def __init__(self, file):
        self.WorkersArray = []
        self.WorkerNumber = 0
        self.WorkersArray = self.OpenFile(file)
        self.WorkersArray.sort()



    #Otworzenie pliku i zczytanie danych
    def OpenFile(self,file):
        with open(file) as f:  
            DataArray = []
            for line in f:                            # czytaj reszte linni i rozdziel na slowa
                DataArray.append(line.split())
        return DataArray



    #Zapis danych do pliku
    def SaveFile(self,filepath,file):
        f = open(filepath, "w")
        for line in file:
            for x in line:
                x = x + ' '
                f.write(x)
            f.write('\n')
        f.close()



    #Ustawienie nowych danych do self.WorkersArray
    #mode=1 -> umowe do pracownika, mode=2 -> wszystkie dane pracownika, mode=3 -> pracownik
    def SetNewData(self,mode,NewData):
        OneData = []
        for x in NewData:
            OneData.append(x.get())
    

        #Dodaj umowe do pracownika
        if mode == 1:
            if OneData[1] != "nok":
                try:
                    datetime.strptime(OneData[1], '%Y-%m-%d')
                except ValueError:
                    return True       
                                                                                            
            self.WorkersArray[self.WorkerNumber].extend(OneData)


        #zmiana wszystkich danych jezeli termin jest poprawny
        elif mode ==2:
            for x in range(3,len(OneData),2):
                
                if OneData[x] != "nok":
                    try:
                        datetime.strptime(OneData[x], '%Y-%m-%d')
                    except ValueError:
                        return True            

            self.WorkersArray[self.WorkerNumber] = OneData

        #dodaj pracownika
        elif mode == 3:
            self.WorkersArray.append(OneData)

        return False
        


    #Usuwanie danych z self.DH.WorkersArray
    def RemoveData(self,mode,index=2):
        
        #Usun umowe pracownika
        if mode == 1:
            del self.WorkersArray[self.WorkerNumber][index:index+2]
        
        #Usun pracownika i jego umowy
        elif mode == 2:
            del self.WorkersArray[self.WorkerNumber]
