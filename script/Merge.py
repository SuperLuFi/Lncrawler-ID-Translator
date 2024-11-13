import os
import io
from alive_progress import alive_bar
# import deep_translator

W = r"C:\Users\Syaiful Bahri\Downloads\Lightnovels\novelhi-com\The Venerable Swordsman\text\c600-2436"
L = r"/media/MXS/A04A8FCD4A8F9EA2/Documents and Settings/Syaiful Bahri/Downloads/Lightnovels/novelhi-com/The Venerable Swordsman/text/c600-2436/"
inputFolder = L
outpFile = ""

  

# Create an empty string to store the content
merged_content = content = daftarFile = ""
i=0


# Iterate through all files in the folder
daftarFile = os.listdir(inputFolder)
daftarFile.sort()
print("Scan directory ...")
print(daftarFile)
print()


print("Menyiapkan nama file ...")
firstFile=daftarFile[0]
print(firstFile)
lastFile=daftarFile[-1]
print(lastFile)
outpFile=firstFile[:-4]+"-"+lastFile
print(outpFile)


# Mengecek ketersediaan file
if os.path.exists(outpFile):
    print("Merged file is detected. Deleting and create the new one ...")
    os.remove(outpFile)
else:
    print("Merged file doesn't exist. Creating ...")


# Merge files in Folder
for filename in daftarFile:
    # Check if the file is a text file (ends with .txt)
    if filename.endswith(".txt"):
      # Construct the full file path
      file_path = os.path.join(inputFolder, filename)
      
      # Open the file and read its content
      with open(file_path, "r", encoding="utf-8") as f:
        # Remove unnecessary enter
        content = f.read().replace('\n\n\n\n', '\n')
        merged_content += content + "\n\n\n\n\n\n\n\n\n"


merged_content=merged_content.replace('\n\nChapter ', '<NyZ>')
# print('merged_content = '+merged_content)
with open("tmp.txt", "w", encoding="utf-8") as f:
    f.write(merged_content)


merged_content=shortened_content=content=""        
with open("tmp.txt", "r", encoding="utf-8") as merged_content:
    i = 0
    for line in merged_content: 
        # process the line 
        i+=1
        kalimat=line.strip()
        if type(kalimat) is str:
            content = str(kalimat)
            # print(terjemahanFix)
            if i%20 == 0:
                shortened_content += "\n"+content 
            else:
                shortened_content += " " +content 
        else:
            shortened_content += "\n"

shortened_content = shortened_content.replace('<NyZ>','\n\n\n\n\n\n\nChapter ')
# print('shortened_content = '+shortened_content)


with open(outpFile, "w", encoding="utf-8") as f:
    f.write(shortened_content)


os.remove("tmp.txt")
# # Translate
# i = 0
# kalimat = ""
# for line in content:
#   kalimat = line.strip()
#   i += 1
#   print("kalimat = "+kalimat)
#   persentase = (i/len(kalimat))*100
#   print("Progress "+persentase+"% ...")
#   if type(kalimat) is str:
#       terjemahan = GoogleTranslator(source='auto', target='id').translate(text=kalimat)
#       terjemahanFix = str(terjemahan)
#       print(terjemahanFix)
#       with open(namaFileTerj, 'a', encoding='UTF-8') as file:
#           file.write("\n"+terjemahanFix)
#   else:
#       with open(namaFileTerj, 'a', encoding='UTF-8') as file:
#           file.write('\n')

# # Write the merged content to an output file named "merged.txt"


print("All text files in the folder have been merged ...")




























# #Cek dan hapus file terjemahan terdahulu
# if os.path.exists(outpFile):
#   os.remove(outpFile)
# else:
#   print("The file does not exist")
    
# open(outpFile, "x") #Buat file terjemahan

# # find all the txt files in the dataset folder
# inputs = []
# for file in os.listdir(inputFolder):
#     if file.endswith(".txt"):
#         inputs.append(os.path.join(inputFolder, file))
 
 
# with open(outpFile, 'w') as outfile:
#     for fname in inputs:
#         with open(fname, encoding="utf-8", errors='ignore') as infile:
#             for line in infile:
#                 outfile.write(line)





'''
chapterAwal=
chaptherAkhir=

namaFileAwal=chapterAwal+".txt"
namaFileAkhir=chaptherAkhir+".txt"
namaFileOutp=chapterAwal+"-"+chaptherAkhir+".txt"

# Reading data from file1
with open(namaFileAwal) as fp:
    data = fp.read()
 
# Reading data from file2
with open('00602.txt') as fp:
    data2 = fp.read()


# Merging 2 files
# To add the data of file2
# from next line
data += "\n\n\n\n\n\n"
data += data2
 

#Save to output file
with open ('file3.txt', 'w') as fp:
    fp.write(data)


    with open(namaFile, 'r') as isiFile: 
    for line in isiFile: 
        # process the line 
        kalimat=line.strip()
        if type(kalimat) is str:
            terjemahan = GoogleTranslator(source='auto', target='id').translate(text=kalimat)
            terjemahanFix = str(terjemahan)
            with open(namaFileTerj, 'a') as file:
                file.write("\n"+terjemahanFix)
'''
