# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator
import os
from alive_progress import alive_bar



W = r"C:\Users\Syaiful Bahri\Downloads\Lightnovels\novelhi-com\The Venerable Swordsman\text\c600-2436"
L = r"/media/MXS/A04A8FCD4A8F9EA2/Documents and Settings/Syaiful Bahri/Downloads/Lightnovels/novelhi-com/The Venerable Swordsman/text/c600-2436/"
inputFolder = L


# Iterate through all files in the folder
daftarFile = os.listdir(inputFolder)
daftarFile.sort()
print("Scan directory ...")
print()


print("Menyiapkan nama file ...")
firstFile=daftarFile[0]
lastFile=daftarFile[-1]
outpFile=firstFile[:-4]+"-"+lastFile



# Mendefinisikan nama file
namaFileTerj = 'id_'+outpFile
i=0

#Cek dan hapus file terjemahan terdahulu
if os.path.exists(namaFileTerj):
  os.remove(namaFileTerj)
else:
  print("The file does not exist. Creating ...")
    
open(namaFileTerj, "x") #Buat file terjemahan

with open(outpFile, 'r', encoding='UTF-8') as isiFile: 
    lines = len(isiFile.readlines())

print()
print("Menerjemahkan ...")

with alive_bar(lines) as bar:
    with open(outpFile, 'r', encoding='UTF-8') as isiFile: 
        for line in isiFile: 
            # process the line 
            # process the line 
            i += 1
            bar()
            kalimat=line.strip()
            persentase = (i/lines)*100
            # print("Progress "+str(round(persentase,2))+"% ...")
            if type(kalimat) is str:
                terjemahan = GoogleTranslator(source='auto', target='id').translate(text=kalimat)
                terjemahanFix = str(terjemahan)
                # print(terjemahanFix)
                with open(namaFileTerj, 'a', encoding='UTF-8') as file:
                    file.write("\n"+terjemahanFix)
            else:
                with open(namaFileTerj, 'a', encoding='UTF-8') as file:
                    file.write('\n')


"""
        #Verifikasi baris, jika kosong skip
        kalimatKosong = "{}"
        cek = kalimatKosong.format(kalimat or "Kosong")
        print(type(cek))

        #Translate Baris yang tidak kosong
        if cek!="Kosong":
            terjemahan=translated = GoogleTranslator(source='auto', target='id').translate(text=kalimat)
            with open(namaFileTerj, 'a') as file:
                file.write('\n'+terjemahan)
        else:
            with open(namaFileTerj, 'a') as file:
                file.write('\n')


translated = GoogleTranslator(source='auto', target='de').translate(text=text)
translated = GoogleTranslator(source='auto', target='id').translate_file('00600.txt')
print (translated)
"""