import os
import io
import argparse
import multiprocessing
import progressbar
from deep_translator import GoogleTranslator


def multiline_to_single_line(input_file, output_file, max_chars=4990):
    with open(input_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()
    
    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    output_lines = []
    current_line = ''

    for line in lines:
        # Handle lines that exceed max_chars individually
        while len(line) > max_chars:
            output_lines.append(line[:max_chars])  # Append the first max_chars characters
            line = line[max_chars:]  # Remainder of the line

        # Now handle the line that is less than or equal to max_chars
        if len(current_line) + len(line) + (1 if current_line else 0) > max_chars:  # +1 for the space
            if current_line:  # If there's something in current_line, append it
                output_lines.append(current_line)
            current_line = line  # Start a new current_line with the current line
        else:
            if current_line:
                current_line += ' '  # Add a space between lines
            current_line += line  # Append the current line to current_line

    if current_line:
        output_lines.append(current_line)  # Add any remaining line

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
    merged_content = title = ''
    for filename in daftar_file:
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                title = lines[0].strip()  # Use strip() to remove any leading/trailing whitespace
                content = ''.join(lines[1:])  # Join the rest of the lines back into a single string
                formatted_title = f'<Ny>{title}<NyZ>'
                content = content.replace(title, formatted_title)
                # print(formatted_title)
                merged_content += formatted_title + "\n\n" + content

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

    # Create progress bar with explicit initialization
    bar = progressbar.ProgressBar(
        maxval=len(lines) or 1,  # Prevent zero division
        widgets=[
            progressbar.Percentage(),
            ' ', 
            progressbar.Bar(marker='█'),
            ' ', 
            progressbar.ETA(),
            ' ',
            progressbar.Counter()
        ]
    )

    # Create a multiprocessing pool with the number of CPU cores
    with multiprocessing.Pool() as pool:
        translated_lines = []
        
        # Explicitly start the progress bar
        bar.start()
        
        try:
            for i, result in enumerate(pool.imap(translate_line, lines), 1):
                translated_lines.append(result)
                bar.update(i)
        except Exception as e:
            print(f"Translation error: {e}")
        finally:
            # Ensure progress bar is finished
            bar.finish()

    # Write translated lines to the output file
    with open(nama_file_terj, 'w', encoding='UTF-8') as file:
        file.write('\n'.join(translated_lines))

    with open(nama_file_terj, "r", encoding="utf-8") as f:
        content = f.read().replace('<Ny>', '\n\n\n\n\n\n\n')
        content = content.replace('<NyZ>', '\n\n\n')

    with open(nama_file_terj, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == '__main__':
    main()