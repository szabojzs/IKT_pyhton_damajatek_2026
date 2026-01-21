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
