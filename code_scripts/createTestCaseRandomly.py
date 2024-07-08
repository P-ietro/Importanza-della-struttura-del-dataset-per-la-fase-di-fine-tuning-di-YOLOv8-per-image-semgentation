# Qeusto script serve a generare il file di configurazione e il file di struttura che definiscono il dataset che poi verrà generato con lo script "produceTestCase.py".
# Da console vengono inserite le caratteristiche della struttura voluta e in automatico genera due file randomici che raccolgono tutte le informazioni che definiscono
# il dataset. Successivamente con "produceTestcase.py" si può creare il dataset vero e proprio con le immagini specificate.
# IMPORTANTE: potrebbe essere necessario modificare i percorsi relativi a cartelle e file. 

import os
import sqlite3
import random


def create_test_set(cursor, logoName, syn_n, real_n, filename):
    cursor.execute("SELECT img FROM syn WHERE logo = ?", [logoName])
    rows = cursor.fetchall()

    rows = [item[0] for item in rows]
    img = random.sample(rows, syn_n)

    for element in img:
        print(element, file=filename)

    cursor.execute("SELECT img FROM real WHERE logo = ?", [logoName])
    rows = cursor.fetchall()

    rows = [item[0] for item in rows]
    img = random.sample(rows, real_n)

    for element in img:
        print(element, file=filename)


def controllo_fattibilita(set, real, syn, richieste):
    disp = 0

    for e in set:
        if e[1] >= syn and e[2] >= real:
            disp += 1
    if disp < richieste:
        print("Non ci sono abbastanza loghi con le caratteristiche necessarie")
        exit(1)



if __name__ == "__main__":
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM logos")
    logos = cursor.fetchall()

    numberOfLogos = int(input("Inserire il numero di loghi: "))

    max_s = 1324
    max_r = 35
    numberOfSynthetic = int(input("Inserire il numero di immagini sinthetiche (Max " + str(max_s) + "): "))
    while numberOfSynthetic < 0 or numberOfSynthetic > max_s:
        numberOfSynthetic = int(input("Inserire il numero di immagini sinthetiche (Max " + str(max_s) + "): "))

    numberOfReal = int(input("Inserire il numero di immagini reali (Max " + str(max_r) + "): "))
    while numberOfReal < 0 or numberOfReal > max_r:
        numberOfReal = int(input("Inserire il numero di immagini reali (Max " + str(max_r) + "): "))


    subSet = random.sample(logos, numberOfLogos)
    subSetCorrect = []
    ImgSetInv = logos
    ImgSet = []

    controllo_fattibilita(ImgSetInv, numberOfReal, numberOfSynthetic, numberOfLogos)

    added = 0
    needToAdd = True
    while needToAdd:
        for l in subSet:
            if l[1] >= numberOfSynthetic and l[2] >= numberOfReal:
                subSetCorrect.append(l)
                added += 1

        ImgSet.extend(subSetCorrect)
        for e in subSetCorrect:
            ImgSetInv.remove(e)

        if added < numberOfLogos:
            subSet = random.sample(ImgSetInv, (numberOfLogos - added))
            controllo_fattibilita(ImgSetInv, numberOfReal, numberOfSynthetic, (numberOfLogos - added))
            subSetCorrect.clear()
        else:
            needToAdd = False

    #Additional Check
    for element in ImgSet:
        if element[1] < numberOfSynthetic or element[2] < numberOfReal:
            print("Qualcosa è andato storto con ", element[0])
            exit(1)


    path = os.getcwd() + "\\test_run" + "\\test_" + str(numberOfLogos)
    if not os.path.exists(path):
        os.mkdir(path)
    path += "\\s" + str(numberOfSynthetic) + "_r" + str(numberOfReal)
    if not os.path.exists(path):
        os.mkdir(path)
    biggest = 0
    if len(os.listdir(path)) > 0:
        biggest = max(os.listdir(path))
        biggest = int(biggest[4:])
    path += "\\run_" + "{:02d}".format(biggest + 1)
    if not os.path.exists(path):
        os.mkdir(path)

    configFilePath = path + "\\configuration.txt"
    config_file = open(configFilePath, 'a')
    print("Number of logos used:", str(numberOfLogos), file=config_file)
    print("Number of synthetic images:", str(numberOfSynthetic), "\tNumber of real images:", str(numberOfReal), "\n", file=config_file)
    for e in ImgSet:
        print(e[0], file=config_file)
    config_file.close()

    setFilePath = path + "\\structure.txt"
    set_file = open(setFilePath, 'a')
    for e in ImgSet:
        create_test_set(cursor, e[0], numberOfSynthetic, numberOfReal, set_file)
    set_file.close()

    cursor.close()
    connection.close()
