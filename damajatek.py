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

def tabla_keszites():
    # A tábla létrehozása és kezdőállás beállítása
    tabla = [[EMPTY for _ in range(tabla_meret)] for _ in range(tabla_meret)]

    # Fekete bábuk: sor 0..2, csak sötét mezőkön
    for s in range(3):
        for o in range(tabla_meret):
            if (s + o) % 2 == 1:
                tabla[s][o] = FEKETE

    # Fehér bábuk: sor 5..7, csak sötét mezőkön
    for s in range(5, 8):
        for o in range(tabla_meret):
            if (s + o) % 2 == 1:
                tabla[s][o] = FEHER

    return tabla

def tabla_rajzolas(tabla, jatekos1, jatekos2):
    # A tábla kiírása színesen
    kepernyo_torles() # képernyő törlése
    print("\n"+jatekos1+" (Fekete: "+FG_SARGA+"b/B"+RESET+")  vs  "+jatekos2+" (Fehér: "+FG_CIANK+"w/W"+RESET+")"+"\n")
    print("   "+BG_SZURKE+"   "+" ".join(str(c + 1) for c in range(tabla_meret))+"   "+RESET) # oszlopok számai
    for r in range(tabla_meret): # sorok
        print("   "+f"{BG_SZURKE}{r+1:2}{RESET} " + " ".join(tabla[r][c] for c in range(tabla_meret))+" "+f"{BG_SZURKE}{r+1:<2}{RESET}") # sor száma
    print("   "+BG_SZURKE+"   "+" ".join(str(c + 1) for c in range(tabla_meret))+"   "+RESET) # oszlopok számai
    print() # üres sor a végén

def szabalyos_lepes(babu, jatekos):
    # Mely irányokba léphet/üthet az adott bábu (normál vs király, fehér vs fekete)
    # Normál bábu csak előre mehet, király mindkét irányba
    if kiralye(babu):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if jatekos == "w":
        return [(-1, -1), (-1, 1)]  # fehér felfelé
    return [(1, -1), (1, 1)]        # fekete lefelé

def lehetseges_utesek_kereses(tabla, s, o, jatekos):
    # Listázza az összes lehetséges ütést az adott bábuból
    """Visszaadja az összes ütést ebből a mezőből: list of (to_r, to_c, mid_r, mid_c)."""
    babu = tabla[s][o]
    dirs = szabalyos_lepes(babu, jatekos)
    caps = []

    for dr, dc in dirs:
        mid_r, mid_c = s + dr, o + dc
        to_r, to_c = s + 2 * dr, o + 2 * dc

        if tablan_belul(to_r, to_c) and tablan_belul(mid_r, mid_c):
            mid_babu = tabla[mid_r][mid_c]
            if mid_babu != EMPTY and not jatekos_babu(mid_babu, jatekos):
                if tabla[to_r][to_c] == EMPTY:
                    caps.append((to_r, to_c, mid_r, mid_c))

    return caps

def jatekos_van_utes(tabla, jatekos):
    # Van-e bármilyen ütés az egész táblán az aktuális játékosnak?
    for r in range(tabla_meret):
        for c in range(tabla_meret):
            if jatekos_babu(tabla[r][c], jatekos):
                if lehetseges_utesek_kereses(tabla, r, c, jatekos):
                    return True
    return False

def normal_lepes_kereses(tabla, s, o, jatekos):
    """Normál (nem ütő) lépések: list of (to_r, to_c)."""
    babu = tabla[s][o]
    dirs = szabalyos_lepes(babu, jatekos)
    moves = []

    for dr, dc in dirs:
        to_r, to_c = s + dr, o + dc
        if tablan_belul(to_r, to_c) and tabla[to_r][to_c] == EMPTY:
            moves.append((to_r, to_c))

    return moves

def kiralya_valas(tabla, r, c): # Királlyá alakítás, ha elérte a túloldalt
    babu = tabla[r][c]
    if babu == FEHER and r == 0:
        tabla[r][c] = FEHER_KIRALY
    elif babu == FEKETE and r == tabla_meret - 1:
        tabla[r][c] = FEKETE_KIRALY

def babuk_szama(tabla, jatekos): # Megszámolja az adott játékos bábuit a táblán
    cnt = 0
    for row in tabla:
        for cell in row:
            if jatekos_babu(cell, jatekos):
                cnt += 1
    return cnt

def lepes_ellenorzes(text):
    # Szövegből (pl. "6 1 5 2") → 0-alapú koordinátákká alakítja
    """
    Vár: "from_row from_col to_row to_col" (1..8)
    Példa: 6 1 5 2
    """
    parts = text.strip().split()
    if len(parts) != 4:
        return None
    try:
        ks, ko, cs, co = [int(x) for x in parts] # ks: kezdő sor, ko: kezdő oszlop, cs: cél sor, co: cél oszlop
        # átírjuk 0-indexre
        return ks - 1, ko - 1, cs - 1, co - 1
    except ValueError:
        return None

def game(tabla, jatekos1, jatekos2, kezdo_jatekos="b"):
    #A fő játékciklus
    jatekos = kezdo_jatekos  # kezdő játékos
    jatek_vege = False
    while True and not jatek_vege:
        tabla_rajzolas(tabla, jatekos1, jatekos2)

        # Megnézi, van-e győztes (valakinek elfogyott minden bábuja)
        if babuk_szama(tabla, "w") == 0:
            print(jatekos1 + " nyert! ("+jatekos2+" elfogyott a bábuja)")
            break
        if babuk_szama(tabla, "b") == 0:
            print(jatekos2 + " nyert! ("+jatekos1+" elfogyott a bábuja)")
            break

        must_capture = jatekos_van_utes(tabla, jatekos) # Van-e bármilyen ütés az egész táblán az aktuális játékosnak?
        p_name = jatekos2+"(Fehér)" if jatekos == "w" else jatekos1+"(Fekete)"
        print(f"{p_name} jön. ({BG_SZURKE+'Kötelező ütés van!'+ RESET if must_capture else 'Nincs kötelező ütés.'})")
        print("Add meg a lépést így: kezdő_sor kezdő_oszlop cél_sor cél_oszlop  (pl.: 6 1 5 2)")

        #Bekér egy lépést a felhasználótól:
        move = None
        while move is None:
            text = input("Lépés(pl.: 6 1 5 2) vagy Mentés (m): ").strip().lower()
            if text == "m":
                with open("damajatekmentes.txt", "w") as f:
                    for row in tabla:
                        f.write("".join(cell if cell != EMPTY else "." for cell in row) + "\n")
                    f.write(jatekos + "\n")
                with open("damajatekmentes_jatekos.txt", "w") as f:
                    f.write(jatekos1 + "\n")
                    f.write(jatekos2 + "\n")
                    f.write(jatekos + "\n")
                print("Játék mentve!")
                jatek_vege = True
                break

            move = lepes_ellenorzes(text)
            if move is None:
                print("Hibás formátum. Példa: 6 1 5 2")
                continue

            ks, ko, cs, co = move
            if not (tablan_belul(ks, ko) and tablan_belul(cs, co)): # Megnézi, hogy a sor-oszlop koordináta a táblán belül van-e (0–7)
                print("Tábla határon kívül.")
                move = None
                continue

            babu = tabla[ks][ko]
            if not jatekos_babu(babu, jatekos): # A kezdő mezőn a játékos bábúja van-e?
                print("Ott nincs a te bábud.")
                move = None
                continue

            if tabla[cs][co] != EMPTY: # A cél mező üres-e?
                print("A cél mező nem üres.")
                move = None
                continue

            d_sor = cs - ks
            d_oszlop = co - ko

            # Ütés ellenőrzés
            capture_options = lehetseges_utesek_kereses(tabla, ks, ko, jatekos) # Listázza az összes lehetséges ütést az adott bábuból
            is_capture = False
            cap_mid = None

            for (to_r, to_c, mid_r, mid_c) in capture_options: # végignézi az összes lehetséges ütést
                if to_r == cs and to_c == co:
                    is_capture = True
                    cap_mid = (mid_r, mid_c)
                    break

            if must_capture and not is_capture: # Ha van kötelező ütés, de a lépés nem ütés
                print("Most ütés kötelező! Válassz ütő lépést.")
                move = None
                continue

            if is_capture: # Ütés végrehajtása    
                # végrehajtás: ugrás + köztes levétele
                tabla[cs][co] = tabla[ks][ko]
                tabla[ks][ko] = EMPTY
                mid_r, mid_c = cap_mid
                tabla[mid_r][mid_c] = EMPTY

                kiralya_valas(tabla, cs, co)

                # többszörös ütés (ugyanazzal a bábuval)
                cur_r, cur_c = cs, co
                while True:
                    more_caps = lehetseges_utesek_kereses(tabla, cur_r, cur_c, jatekos) # Listázza az összes lehetséges ütést az adott bábuból
                    if not more_caps:
                        break

                    tabla_rajzolas(tabla)
                    print("Többszörös ütés lehetséges, folytatnod kell!")      
                    print(f"A bábu most itt van: {cur_r+1} {cur_c+1}") # aktuális pozíció kiírása
                    print("Add meg a következő cél mezőt: cel_sor cel_oszlop (pl.: 3 4)") 
                    nxt = input(">> ").strip().split() # Bekér egy lépést a felhasználótól:
                    if len(nxt) != 2: # Hibás formátum ellenőrzése
                        print("Hibás formátum, próbáld újra.")
                        continue
                    try:
                        ntr, ntc = int(nxt[0]) - 1, int(nxt[1]) - 1 # Szövegből (pl. "3 4") → 0-alapú koordinátákká alakítja
                    except ValueError:
                        print("Számokat adj meg.")
                        continue

                    # ellenőrizzük, hogy ez tényleg egy következő ütés-e
                    chosen = None
                    for (to_r, to_c, mid_r, mid_c) in more_caps: # végignézi az összes lehetséges ütést
                        if to_r == ntr and to_c == ntc:
                            chosen = (to_r, to_c, mid_r, mid_c) # végrehajtandó ütés
                            break
                    if chosen is None:
                        print("Ez nem érvényes ütés ezzel a bábuval.")
                        continue

                    # végrehajtás
                    to_r, to_c, mid_r, mid_c = chosen # végrehajtandó ütés
                    tabla[to_r][to_c] = tabla[cur_r][cur_c] # lépés célpontja lesz a bábu
                    tabla[cur_r][cur_c] = EMPTY # kiürítjük a kiinduló mezőt
                    tabla[mid_r][mid_c] = EMPTY # köztes mezőt is kiürítjük
                    kiralya_valas(tabla, to_r, to_c) # királlyá alakítás, ha elérte a túloldalt
                    cur_r, cur_c = to_r, to_c # aktuális pozíció frissítése

                # kör vége
                break

            else:
                # Normál lépés (1 átló)
                normal_lepesek = normal_lepes_kereses(tabla, ks, ko, jatekos) # Normál (nem ütő) lépések
                if (cs, co) not in normal_lepesek: #
                    print("Ez nem érvényes normál lépés.")
                    move = None
                    continue

                tabla[cs][co] = tabla[ks][ko] # lépés célpontja lesz a bábu
                tabla[ks][ko] = EMPTY # kiürítjük a kiinduló mezőt
                kiralya_valas(tabla, cs, co) # királlyá alakítás, ha elérte a túloldalt
                break

        # játékos csere
        jatekos = "w" if jatekos == "b" else "b"

if __name__ == "__main__":
    uj_jatek = input("Új játék / folytatás mentettből (u/f)? ").strip().lower()
    if uj_jatek == "f":
        try:
            with open("damajatekmentes.txt", "r") as f:
                tabla = []
                for _ in range(tabla_meret):
                    line = f.readline().strip()
                    row = []
                    for ch in line:
                        if ch == ".":
                            row.append(EMPTY)
                        elif ch == "w":
                            row.append(FEHER)
                        elif ch == "b":
                            row.append(FEKETE)
                        elif ch == "W":
                            row.append(FEHER_KIRALY)
                        elif ch == "B":
                            row.append(FEKETE_KIRALY)
                    tabla.append(row)
                jatekos = f.readline().strip()
            with open("damajatekmentes_jatekos.txt", "r") as f:
                jatekos1 = f.readline().strip()
                jatekos2 = f.readline().strip()
                kezdo_jatekos = f.readline().strip()
        except FileNotFoundError:
            print("Nincs mentett játék, új játék indul.")
            tabla = tabla_keszites()
            jatekos1 = input("Első játkos neve: ").strip()
            jatekos2 = input("Második játkos neve: ").strip()
            kezdo_jatekos = "b"
    else:
        jatekos1 = input("Első játkos neve: ").strip()
        jatekos2 = input("Második játkos neve: ").strip()
        tabla = tabla_keszites()
    
    game(tabla, jatekos1, jatekos2, kezdo_jatekos if uj_jatek == "f" else "b")