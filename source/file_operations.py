import os
import logging
from translator import translate_file
from utils import multiline_to_single_line

def merge_files(input_folder):
    merged_content = ''
    daftar_file = os.listdir(input_folder)
    daftar_file.sort()

    if not daftar_file:
        logging.warning("No text files found in the specified directory.")
        return ''

    for filename in daftar_file:
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                title = lines[0].strip()
                content = ''.join(lines[1:])
                formatted_title = f'<Ny>{title}<NyZ>'
                content = content.replace(title, formatted_title)
                merged_content += formatted_title + "\n\n" + content

    return merged_content

def main(input_folder, output_folder, max_chars, target_language):
    try:
        os.makedirs(output_folder, exist_ok=True)
        merged_content = merge_files(input_folder)

        if not merged_content:
            return

        tmp_file = os.path.join(output_folder, "tmp.txt")
        with open(tmp_file, "w", encoding="utf-8") as f:
            f.write(merged_content)

        output_file = os.path.join(output_folder, f'merged_output.txt')
        multiline_to_single_line(tmp_file, output_file, max_chars)
        os.remove(tmp_file)

        logging.info("All text files in the folder have been merged ...")

        # Translate the output file
        translated_lines = translate_file(output_file, target_language)
        translated_file_name = os.path.join(output_folder, f'translated_{target_language}_output.txt')

        with open(translated_file_name, 'w', encoding='UTF-8') as f:
            f.write('\n'.join(translated_lines))

        with open(translated_file_name, "r", encoding="utf-8") as f:
            content = f.read().replace('<Ny>', '\n\n\n\n\n\n\n')
            content = content.replace('<NyZ>', '\n\n\n')

        with open(translated_file_name, "w", encoding="utf-8") as f:
            f.write(content)

        logging.info("Translation completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")