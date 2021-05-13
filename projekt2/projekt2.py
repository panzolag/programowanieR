#PROJEKT 2
#Krzysztof Solak
#nr. albumu 42755
print('''Wykorzsystana w tym projekcie technika bezuje na stworzeniu słowników zawierających jako kluczę nazwy krajów a jako wartości słowniki zawierające
z koleji jako klucze kolejne daty natomiast jako wartości odpowienie dane z pliku, wczytanie pierwszych słowników może zająć chwilkę jednak następnie operację
na owych słwoniakch są szybsze!''')


import requests
import numpy as np 
import matplotlib.pyplot as plt
import csv

#proszę o dane ze strony podanej w poleceniu
r = requests.get('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
with open('full_data.csv', 'wb') as f:
    f.write(r.content)
#usuwam pierwszy wiersz i tworzę nowy plik \bibitem(1)
with open("full_data.csv",'r') as f:
    with open("fulldata.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

#Tworzę lisytę krajów (w tym świat i kontynenty)
kraje = ['location']
with open("fulldata.csv") as datafile:
    for line in datafile:
        a = line.split(',')
        if kraje[-1] != a[2]:
            kraje.append(a[2])
        else: continue
del kraje[0] #usuwam pozycję location
del kraje[-17] #usuwam Tuvalu... nie wiem dlaczego nie ma go w bazie
#Tworzę słownik którego kluczami są kraje a eartościmi słowniki których z koleji kluczami są dany a wartościmi całkowita liczba przypadków
#{Kraj:{data:Liczba przypadków}}
totalcases = {}
with open("fulldata.csv") as datafile:
        for j in kraje:
            b = {}
            for line in datafile:
                a = line.split(',')
                if a[2] == j:
                    b[a[3]] = a[4]
                    totalcases["%s" %j] = b
                else: break
#{Kraj:{data:Liczba nowcyh przypadków}}
newcases = {}
with open("fulldata.csv") as datafile:
        for j in kraje:
            c = {}
            for line in datafile:
                a = line.split(',')
                if a[2] == j:
                    c[a[3]] = a[5]
                    newcases["%s" %j] = c
                else: break  
#{kraj:{data:liczba zgonów}}
newdeaths = {}
with open("fulldata.csv") as datafile:
        for j in kraje:
            c = {}
            for line in datafile:
                a = line.split(',')
                if a[2] == j:
                    c[a[3]] = a[8]
                    newdeaths["%s" %j] = c
                else: break  
#************************************************************************************************************************************************************************************
# KLASA
class Kraj:

    def __init__(self, name):
        self.name = name 
        self.newcases = newcases[f'{name}'] 
        self.totalcases = totalcases[f'{name}']
        self.newdeaths = newdeaths[f'{name}']
#metoda rysująca wykres wszyskich zakarzeń od czasu 
    def total(self):
        
        x1 = list(self.totalcases.keys())
        x = []
        leng = len(x1)
        for i in range (0,leng):
            x.append(i)
        y1 = list(self.totalcases.values())
        y = []
        for i in y1:
            y.append(float(i))
        plt.scatter(x, y,
        color = "black",
        s = 1)
        plt.xlabel(f'Dni od {x1[0]}')
        plt.ylabel('całkowita liczba przypadków')
        plt.show()
#metoda rysująca wykres nowych zakarzeń na dzień  
    def new(self):
        x1 = list(self.newcases.keys())
        x = []
        leng = len(x1)
        for i in range (0,leng):
            x.append(i)
        y1 = list(self.newcases.values())
        y = []
        for i in y1:
            y.append(float(i))
        plt.scatter(x, y,
        color = "black",
        s = 1)
        plt.xlabel(f'Dni od {x1[0]}')
        plt.ylabel('dzienna liczba przypadków')
        plt.show()
#dodawanie nowch przypadków w krajach
    def __add__(self, other):
        self.x = list(self.newcases.keys()) #lista dat self
        self.y = list(self.newcases.values()) #lista nowych choryvch self
        other.x = list(other.newcases.keys()) # lista dat other 
        other.y = list(other.newcases.values()) #lista nowych chorych other 
        newname = f"{self.name}"+" and "+f"{other.name}" # nazwa nowego kraju (połączonego)
                
        D = max(len(self.x), len(other.x)) #długość listy do sumowania
        z = np.abs(len(self.y)-len(other.y)) #Różnica długości list (czasem nie są równe w pliku)
        if len(self.y) < len(other.y): # jeżeli self.y jest krutsza dopełniam ją zerami do sługości other.y
            for i in range (z):
                self.y.append(0)
        elif len(self.y) > len(other.y): # jak komentarz wyżej 
            for i in range (z):
                other.y.append(0)
        
        suma = [float(other.y[i]) + float(self.y[i]) for i in range(D)] #\Bibitem(2)  Sumuje elemnty każdej z list  
        e = {} # tworzę pusty słownik krótego kluczami będą daty a wartościmi sumy wartości dla  krajów   
        if D == len(self.x):# pakowanie słownika 
            for i in range (D):
                e[self.x[i]] = suma[i]
            newcases[newname] = e
            totalcases[newname] = {} # w zadaniu nie sumuję wszystkich zachorowań ale pro forma niech będą w słowniku jako argumęt
            newdeaths[newname] = {}
        elif D == len(other.x):
            for i in range (D):
                e[other.x[i]] = suma[i]
            newcases[newname] = e
            totalcases[newname] = {} # jak wyżej komentarz
            newdeaths[newname] = {}
        return Kraj(newname)
    __radd__ = __add__ #możliwa jest zamiana kolejnosci
#Wyliczanie średniej  z ostatnich 7 dni 
    def lastaverage(self):
        k = {}
        l1 = list(self.newcases.values())
        try:
            average1 = (float(l1[-1])+float(l1[-2])+float(l1[-3])+float(l1[-4])+float(l1[-5])+float(l1[-6])+float(l1[-7]))/7
        except:
            average1 = "Dane nie zostały zaktualizowne" 
        k['Średnia newcases'] = average1

        l2 = list(self.totalcases.values())
        try:
            average2 = (float(l2[-1])+float(l2[-2])+float(l2[-3])+float(l2[-4])+float(l2[-5])+float(l2[-6])+float(l2[-7]))/7
        except:
            average2 = "Danie nie zostały zaktualizowane"
        k['Średnia totalcases'] = average2
        l3 = list(self.newdeaths.values())
        try:
            average3 = (float(l3[-1])+float(l3[-2])+float(l3[-3])+float(l3[-4])+float(l3[-5])+float(l3[-6])+float(l3[-7]))/7
        except:
            average3 = 'Dane nie zostały zaktualizowane'
        k['Średnia newdeaths'] = average3
        return k

# podanie pola w klasie 
    def operator(self):
        d = str(input('Podaj dajną jaką chcesz sprawdzić (name, newcases, totalcases, newdeaths):'))
        if d == 'name':
            print(self.name)
        elif d == 'newcases':
            print(self.newcases)
        elif d == 'totalcases':
            print(self.totalcases)
        elif d == 'newdeaths':
            print(newdeaths)
        else: print('proszę podać nazwę z nawiastu')
         
    def operator2(self):
        return(newdeaths)
        


tablica = []
o = {}
for j in kraje:
    a = Kraj(j)
    tablica.append(a)
for i in tablica:
    a = i.name
    b = i.lastaverage()
    o[a] = b
print(o)




#Poland = Kraj('Poland')
#Germany = Kraj('Germany')
#PA = Poland + Germany
#Poland.operator()
#Germany.total()
#print(Poland.lastaverage())
#Poland.nowe()
#Bibliografia
#(1) https://stackoverflow.com/questions/23615496/removing-the-first-line-of-csv-file
#(2) http://glach.wikidot.com/p1r-polyclass