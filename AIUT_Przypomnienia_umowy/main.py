#Pobranie klasy do wobslugi aplikacji, zawiera DataHandler.py
from GUI import GUI

#Potrzebne pliki: main.py, GUI.py, DataHandler.py, Zapis_danych.txt - nazwe mozna zmienic w mainie

#Uruchomienie aplikacji 
if __name__== "__main__":

    app = GUI("data_files/Workers_data.txt")
    