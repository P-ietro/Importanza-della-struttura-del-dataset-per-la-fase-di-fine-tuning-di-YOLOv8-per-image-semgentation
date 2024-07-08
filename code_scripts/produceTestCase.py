# Questo script server a generare il dataset vero e proprio con i file che dovranno poi essere dati in pasto alla rete, a partire da un file di struttura creato in precedenza
# con "createTestCaseRandomli.py".
# Questo script si occupa di dividere le immagini totali in due sezioni, una per il training e l'altra per la validation.
# IMPORTANTE: potrebbe essere necessario modificare il path di cartelle e file.

import os
import random
import shutil

if __name__ == "__main__":
    nol = input("numero di loghi diversi: ")
    nos = input("numero di loghi sintetici: ")
    nor = input("numero di loghi reali: ")

    destinationPath = os.getcwd() + "\\test_run\\test_" + nol + "\\s" + nos + "_r" + nor

    allRun = os.listdir(destinationPath)
    if len(allRun) <= 0:
        print("No run")
        exit(1)

    print(allRun)
    biggest = max(os.listdir(destinationPath))
    biggest = int(biggest[4:])

    run = int(input("selec a run number: "))
    while run < 1 or run > biggest:
        run = int(input("selec a run number: "))

    destinationPath += "\\run_" + "{:02d}".format(run)

    images_syn_source_path = os.getcwd() + "\\images_synthetic"
    label_syn_source_path = os.getcwd() + "\\truth_synthetic_txt"
    images_real_source_path = os.getcwd() + "\\images_real"
    label_real_source_path = os.getcwd() + "\\truth_real_txt"
    train_image_path = destinationPath + "\\dataset" + "\\images" + "\\train"
    val_image_path = destinationPath + "\\dataset" + "\\images" + "\\val"
    train_label_path = destinationPath + "\\dataset" + "\\labels" + "\\train"
    val_label_path = destinationPath + "\\dataset" + "\\labels" + "\\val"

    os.mkdir(destinationPath + "\\dataset")
    os.mkdir(destinationPath + "\\dataset" + "\\images")
    os.mkdir(destinationPath + "\\dataset" + "\\labels")
    os.mkdir(train_label_path)
    os.mkdir(train_image_path)
    os.mkdir(val_label_path)
    os.mkdir(val_image_path)

    yaml_file = open(destinationPath + "\\dataset\\config.yaml", "w")
    print("path: /kaggle/input/test-" + nol + "s" + nos + "-r" + nor + "run-{:02d}".format(run) + " # dataset root dir", file=yaml_file)


    print("train: images/train # train images", file=yaml_file)
    print("val: images/val # val images", file=yaml_file)
    print("test: # test images (optional)", file=yaml_file)
    print("\n", file=yaml_file)
    print("nc: 1", file=yaml_file)
    print("names: ['logo']", file=yaml_file)
    yaml_file.close()

    struct_file = open(destinationPath + "\\structure.txt", "r")
    lines = struct_file.readlines()
    struct_file.close()

    lines = [l.split("\n")[0] for l in lines]

    nol = int(nol)
    nos = int(nos)
    nor = int(nor)

    for index in range(nol):
        subset_syn = lines[(index * (nos + nor)):((index * (nos + nor)) + nos)]
        validation_subset_syn = random.sample(subset_syn, (nos // 10))
        train_subset_syn = [x for x in subset_syn if x not in validation_subset_syn]

        subset_real = lines[(index * (nor + nos) + nos):((index + 1) * (nos + nor))]
        validation_subset_real = random.sample(subset_real, (1 if (nor < 10 and nor != 0) else nor // 10))
        train_subset_real = [x for x in subset_real if x not in validation_subset_real]

        for e in train_subset_syn:
            #print("train_syn ", e.zfill(8))
            shutil.copyfile((images_syn_source_path + "\\" + e.zfill(8) + ".jpg"), (train_image_path + "\\" + e.zfill(8) + ".jpg"))
            shutil.copyfile((label_syn_source_path + "\\" + e.zfill(8) + ".txt"), (train_label_path + "\\" + e.zfill(8) + ".txt"))

        for e in train_subset_real:
            #print("train_real ", e.zfill(8))
            shutil.copyfile((images_real_source_path + "\\" + e.zfill(8) + ".jpg"), (train_image_path + "\\" + e.zfill(8) + ".jpg"))
            shutil.copyfile((label_real_source_path + "\\" + e.zfill(8) + ".txt"), (train_label_path + "\\" + e.zfill(8) + ".txt"))

        for e in validation_subset_syn:
            #print("val_syn ", e.zfill(8))
            shutil.copyfile((images_syn_source_path + "\\" + e.zfill(8) + ".jpg"), (val_image_path + "\\" + e.zfill(8) + ".jpg"))
            shutil.copyfile((label_syn_source_path + "\\" + e.zfill(8) + ".txt"), (val_label_path + "\\" + e.zfill(8) + ".txt"))

        for e in validation_subset_real:
            #print("val_real ", e.zfill(8))
            shutil.copyfile((images_real_source_path + "\\" + e.zfill(8) + ".jpg"), (val_image_path + "\\" + e.zfill(8) + ".jpg"))
            shutil.copyfile((label_real_source_path + "\\" + e.zfill(8) + ".txt"), (val_label_path + "\\" + e.zfill(8) + ".txt"))

    shutil.make_archive((destinationPath + "\\dataset"), 'zip', root_dir=(destinationPath + "\\dataset"))
    shutil.rmtree((destinationPath + "\\dataset"))



