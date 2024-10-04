import os
import io
import argparse
import multiprocessing
from alive_progress import alive_bar
from deep_translator import GoogleTranslator


def multiline_to_single_line(input_file, output_file, max_chars=4985):
    with open(input_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]  # Remove newline characters and leading/trailing whitespace
    output_lines = []
    current_line = ''
    for line in lines:
        if len(current_line) + len(line) + 1 > max_chars:  # +1 for the space between lines
            output_lines.append(current_line)
            current_line = line
        else:
            if current_line:
                current_line += ' '  # Add a space between lines
            current_line += line

    if current_line:
        output_lines.append(current_line)

    with open(output_file, 'w', encoding="utf-8") as file:
        for line in output_lines:
            file.write(line + '\n')

def translate_line(line):
    """Translate a single line using GoogleTranslator"""
    kalimat = line.strip()
    if kalimat:
        terjemahan = GoogleTranslator(source='auto', target='id').translate(text=kalimat)
        return terjemahan
    else:
        return ''

def add_string(text, string):
    """Add a string after the number in each chapter title"""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        parts = line.split()
        if parts[0] == 'Chapter':
            parts.insert(2, string)
        lines[i] = ' '.join(parts)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Merge and translate text files')
    parser.add_argument('input_folder', help='Input folder containing text files')
    args = parser.parse_args()

    input_folder = args.input_folder

    # Iterate through all files in the folder
    daftar_file = os.listdir(input_folder)
    daftar_file.sort()
    firstFile=daftar_file[0]
    lastFile=daftar_file[-1]
    output_file=firstFile[:-4]+"-"+lastFile

    # Merge files in Folder
    merged_content = ''
    for filename in daftar_file:
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().replace('\n\n\n\n', '\n')
                content = add_string(content, '<N>')
                content = content.replace("Chapter", "<NyZ>", 1)
                merged_content += content + "\n\n\n\n\n\n\n\n\n"

    with open("tmp.txt", "w", encoding="utf-8") as f:
        f.write(merged_content)

    multiline_to_single_line('tmp.txt', output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        a = f.read().replace("         ", " ")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(a)

    os.remove("tmp.txt")

    print("All text files in the folder have been merged ...")

    # Translate the output file
    nama_file_terj = 'id_' + output_file
    if os.path.exists(nama_file_terj):
        os.remove(nama_file_terj)
    else:
        print("The file does not exist. Creating ...")

    open(nama_file_terj, "x")  # Create translation file

    with open(output_file, 'r', encoding='UTF-8') as isi_file:
        lines = len(isi_file.readlines())

    print()
    print("Translating ...")

    with open(output_file, 'r', encoding='UTF-8') as isi_file:
        lines = isi_file.read().splitlines()

    # Create a multiprocessing pool with the number of CPU cores
    with multiprocessing.Pool() as pool:
        # Translate lines in parallel
        with alive_bar(len(lines), title="Translating lines") as bar:
            translated_lines = []
            for result in pool.imap(translate_line, lines):
                translated_lines.append(result)
                bar()  # Update the progress bar

    # Write translated lines to the output file
    with open(nama_file_terj, 'w', encoding='UTF-8') as file:
        file.write('\n'.join(translated_lines))


    # with alive_bar(lines) as bar:
    #     with open(output_file, 'r', encoding='UTF-8') as isi_file:
    #         for line in isi_file:
    #             bar()
    #             kalimat = line.strip()
    #             if type(kalimat) is str:
    #                 terjemahan = GoogleTranslator(source='auto', target='id').translate(text=kalimat)
    #                 terjemahan_fix = str(terjemahan)
    #                 with open(nama_file_terj, 'a', encoding='UTF-8') as file:
    #                     file.write("\n" + terjemahan_fix)
    #             else:
    #                 with open(nama_file_terj, 'a', encoding='UTF-8') as file:
    #                     file.write('\n')

    with open(nama_file_terj, "r", encoding="utf-8") as f:
        content = f.read().replace('<NyZ>', '\n\n\n\n\n\n\nBAB')
        content = content.replace('<N>', '\n\n')

    with open(nama_file_terj, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == '__main__':
    main()