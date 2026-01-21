# Egyszerű konzolos Dáma (Checkers) - 2 játékos
# Szabályok (egyszerű, de játszható):
# - 8x8 tábla
# - Fekete (b) felül indul és lefelé lép, Fehér (w) alul indul és felfelé lép
# - Átlósan 1-et lépsz, ütésnél 2-t ugrasz és a köztes bábu lekerül
# - Ütés kötelező, és többszörös ütés is van (ha lehetséges folytatni kell)
# - Király (B/W): elérve a túloldalt, visszafelé is léphet/üthet
import os 

tabla_meret = 8

BG_SZURKE = "\033[47m"
BG_FEKETE = "\033[40m"
FG_CIANK = "\033[96m"
FG_SARGA = "\033[93m"
RESET = "\033[0m"
EMPTY =  "-"
FEHER =  FG_CIANK + "w" + RESET
FEKETE =  FG_SARGA+ "b" + RESET
FEHER_KIRALY =  FG_CIANK + "W" + RESET
FEKETE_KIRALY =  FG_SARGA+ "B" + RESET

def kepernyo_torles():
    # Windows esetén 'cls', Linux/Mac esetén 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def tablan_belul(sor, oszlop):
    # Megnézi, hogy a sor-oszlop koordináta a táblán belül van-e (0–7)
    return 0 <= sor < tabla_meret and 0 <= oszlop < tabla_meret

def ellenfel(jatekos):
    # Visszaadja az ellenfél színét ("w" → "b", "b" → "w")
    return "b" if jatekos.lower() == "w" else "w"

def jatekos_babu(babu, jatekos):
    # Megmondja, hogy az adott babu az aktuális játékosé-e
    if jatekos == "w":
        return babu in (FEHER, FEHER_KIRALY)
    return babu in (FEKETE, FEKETE_KIRALY)

def kiralye(babu):
    # Király-e a bábu? (nagybetűs W vagy B)
    return babu in (FEHER_KIRALY, FEKETE_KIRALY)
