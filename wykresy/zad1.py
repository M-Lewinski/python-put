#!/usr/bin/env python
# -*- coding utf-8 -*-
import matplotlib.pyplot as plt

# Funkcja dopisuje w odpowiednim miejscu krotki numer pokolenia
def generation(column,cell,krotka):
    krotka[2] = float(cell)

# Funkcja dopisuje w odpowiednim miejscu krotki liczbę rozegranych gier
def effort(column,cell,krotka):
    krotka[0] = float(cell)

# Funkcja dopisuje w odpowiednim miejscu krotki wynik algorytmu ewolucyjnego
def run(column,cell,krotka):
    krotka[1].append(float(cell))

# Funckja sprawdza opis danej kolumny i napodstawie opisuje modyfikuje krotkę w odpowiedni sposób
def checkCell(column,cell,krotka):
    switcher = {
        "generation": generation, # Jeżeli w kolumnie "generation"
        "effort": effort, # Jeżeli w kolumnie "effort"
    }
    function = switcher.get(column,run) # Jeżeli nie ma pasuje do żadnej kolumny to przypiszę funkcję run
    function(column,cell,krotka) # Wykonanie przypisanej funkcji

# Wczytywanie pliku do odpowiedniego formatu
def readFile(fileName):
    readFile = open(fileName,"r") # otwarcie pliku
    lines = readFile.readlines(); # zczytanie linijek
    readFile.close(); # zamknięcie pliku
    plotArray = [[]]*3 #tablica, w której: element [0] - liczba rozegranych gier
    for i in range(len(plotArray)):      # element [1] - tablica wyników
        plotArray[i] = []                # element [2] - numer pokoleń
    for i in range(len(lines)):
        if i == 0:  # Odczytanie opisów kolumn
            columns = lines[i]
            columns = columns.split(",") # dzielenie linii. Separator - ","
        else:
            cells = lines[i].split(',') # dzielenie linii. Separator - ","
            krotka = [0,[],0] # nowa krotka
            for j in range(len(cells)):
                checkCell(columns[j],cells[j],krotka); # sprawdzenie komórki i wykonanie odpowiednich funkcji
            for i in range(len(krotka)):
                plotArray[i].append(krotka[i]) # dodanie nowej krotki
    return plotArray # utworzona tablica postaci : [liczby rozegranych gier,tablice wyników,pokolenia]

# Funkcja wczytująca wiele plików
def readAllFiles(fileList):
    plotList = []
    for i in range(len(fileList)):
        plotList.append(readFile(fileList[i][0])) # wczytanie pliku
        plotList[-1].append(fileList[i]) # Dodanie do tablicy dodatkowych informacji potrzebnych do narysowania funkcji
    return plotList

# Funkcji rysująca wykresy
def drawPlots(plotList):
    axis1 = plt.subplot(121) # Rysowanie wykresu liniowego z lewej strony
    axis1.set_xlabel("Rozegranych gier (x1000)") # label osi x
    axis1.set_ylabel("Odsetek wygranych gier [%]") # label osi y
    axis2 = axis1.twiny() # utworznie dodatkowej osi X
    axis2.set_xlabel("Pokolenie") # label nowej osi X
    axis3 = plt.subplot(122) #Rysowanie wykresu pudełkowego z prawej strony
    maxGeneration = [] # Sprawdzenie maksymalnej liczby pokoleń
    for newPlot in plotList: # Wczytanie funkcji do wykresu
        xData = [float(x/1000) for x in newPlot[0]] # zmiana notacji liczby gier
        yData = [(sum(x)/len(x))*100 for x in newPlot[1]] # obliczanie średniej wyników
        axis1.plot(xData,yData,color = newPlot[3][1],marker=newPlot[3][2],markevery=25,label=newPlot[3][3]) # Rysowanie funkcji
        maxGeneration = max(maxGeneration,newPlot[2]) # Sprawdzanie maksymalnej liczby pokoleń
    axis1.legend(loc=4) # Utworzenie legendy w lewym dolnym rogu
    part = int(len(maxGeneration)/5) # podział nowej osi X na 5 części
    maxGeneration.append(maxGeneration[-1]+1)
    axis2.set_xticks(maxGeneration[::part]) # Dodanie danych do nowej osi X
    axis1.set_xlim(0,500) # Ustawienie limitu liczby gier
    axis2.set_xlim(0,200) # Ustawienie limity pokoleń
    kropki = dict(marker='o', markerfacecolor='blue')
    axis3.boxplot([[x*100 for x in newPlot[1][-1]] for newPlot in plotList],labels=[newPlot[3][3] for newPlot in plotList],notch=True,showmeans=True,meanprops=kropki) # Rysowanie funkcji
    axis3.yaxis.tick_right() # Ustawienie osi Y po prawej stronie wykresu
    axis3.set_ylim(60,100) # Ustawienie limitu osi Y
    axis3.set_xticklabels(axis3.get_xticklabels(),rotation=20) # Rotacja labeli osi X o 20 stopni
    axis1.grid(True) # Dodanie siatki do wykresu
    axis3.grid(True) # Dodanie siatki do wykresu
    plt.savefig('wykresy.pdf') # Zapisanie wyresów do pliku
    plt.show() # Pokazanie wykresów
    plt.close() # Zamknięcie plotu

# Główna funkcja programu
def main():
    # lista nazw plików oraz informacji do poprawnego rysowania funkcji (nazwa, kolor, marker, label)
    fileList = [["rsel.csv","b","o","1-Evol-RS"],["cel-rs.csv","g","v","1-Coev-RS"],["2cel-rs.csv","r","D","2-Coev-RS"],["cel.csv","k","s","1-Coev"],["2cel.csv",'m',"d","2-Coev"]]
    try: # Sprawdzenie, czy znaleziono pliki
        newPlotList = readAllFiles(fileList)
    except FileNotFoundError:
        print("ERROR::COULDN'T FIND FILES::ERROR")
    drawPlots(newPlotList) # Rysowanie wykresów


if __name__ == '__main__':
    main()
