# Tema 1

## Introducere

Se doreste implementarea unei infrastructuri de comunicatie (server-client) ce utilizeaza criptosistemul AES si modurile de operare pentru cifrurile block CBC si CFB pentru criptarea traficului intre doua noduri A si B.

## Librarii folosite
In implementarea acestei infrastructuri am avut nevoie de urmatoarele librarii:
**socket** - pentru a efectua comunicarea dintre server si cei doi clienti
**Crypto** - pentru criptare ( pentru instalare: **pip3 install pycryptodome**)
**pickle** - pentru trimiterea datelor sub forma unui obiect

## Arhitectura aplicatiei
1. **Alegerea modului de operare** de catre nodul **A**, urmand ca nodul **B** sa primeasca modul de operare ramas
2. Se face schimbul de chei ( **A** primeste **Key1**, iar **B** primeste **Key2**
3. **A** cripteaza continutul fisierului cu cheia **Key1** si il trimite catre **KM**
4. **KM** decripteaza mesajul primit de la **A** cu cheia **Key1**, il cripteaza cu cheia **Key2** si il trimite catre **B**
5. **B** decripteaza mesajul primit de la **KM** cu cheia **Key2** si trimite catre **KM** un mesaj de confirmare criptat cu cheia **Key2**
6. **KM** decripteaza mesajul primit de la **B** cu cheia **Key2**, il cripteaza cu cheia **Key1** si il trimite catre **A**

![architecture](https://user-images.githubusercontent.com/58566863/97672303-79721880-1a92-11eb-8387-913ad1016b0e.png)

## Criptarea si decriptarea
Criptarea si decriptarea au fost efectuate prin impartirea in blocuri, aplicarea
operatiei XOR intre vectorul de initializare si un bloc sau intre doua blocuri
si utilizarea obiectului AES din libraria Crypto.
In cazul in care ultimul bloc nu avea dimensiunea corespunzatoarea celor 128 biti, 
atunci se aplica un padding.

## Pornire infrastructura
1. python KM.py
2. python A.py
3. python B.py
4. introduceti **0** sau **1** in terminalul lui **A** , in functie de modul ales dintre cele doua afisate.

