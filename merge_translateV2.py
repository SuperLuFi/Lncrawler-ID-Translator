import os
import io
import multiprocessing
import progressbar
import logging
import argparse
from deep_translator import GoogleTranslator


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def multiline_to_single_line(input_file, output_file, max_chars=4990):
    try:
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

    except Exception as e:
        logging.error(f"Error processing multiline to single line: {e}")


def translate_line(line):
    """Translate a single line using GoogleTranslator"""
    kalimat = line.strip()
    if kalimat:
        try:
            terjemahan = GoogleTranslator(source='auto', target='id').translate(text=kalimat)
            return terjemahan
        except Exception as e:
            logging.error(f"Translation error for line: {kalimat}. Error: {e}")
            return kalimat  # Return the original line in case of error
    else:
        return ''

def main(input_folder, output_folder, max_chars):
    try:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Iterate through all files in the folder
        daftar_file = os.listdir(input_folder)
        daftar_file.sort()

        if not daftar_file:
            logging.warning("No text files found in the specified directory.")
            return

        firstFile = daftar_file[0]
        lastFile = daftar_file[-1]
        output_file_name = f"{firstFile[:-4]}-{lastFile}"  # Just the filename
        output_file = os.path.join(output_folder, output_file_name)  # Full path for output file

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
                    merged_content += formatted_title + "\n\n" + content

        tmp_file = os.path.join(output_folder, "tmp.txt")
        with open(tmp_file, "w", encoding="utf-8") as f:
            f.write(merged_content)

        multiline_to_single_line(tmp_file, output_file, max_chars)

        with open(output_file, "r", encoding="utf-8") as f:
            a = f.read().replace("         ", " ")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(a)

        os.remove(tmp_file)

        logging.info("All text files in the folder have been merged ...")

        # Translate the output file
        nama_file_terj = os.path.join(output_folder, f'id_{output_file_name}')  # Correctly construct the translation file path
        if os.path.exists(nama_file_terj):
            os.remove(nama_file_terj)
            logging.info(f"Existing translation file '{nama_file_terj}' removed.")
        else:
            logging.info("The translation file does not exist. Creating ...")

        open(nama_file_terj, "x")  # Create translation file

        with open(output_file, 'r', encoding='UTF-8') as isi_file:
            lines = isi_file.read().splitlines()

        logging.info("Translating ...")

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
                logging.error(f"Translation error: {e}")
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

        logging.info("Translation completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge and translate text files.')
    parser.add_argument('--input_folder', type=str, default='./txt', help='Directory containing text files to merge.')
    parser.add_argument('--output_folder', type=str, default='./', help='Directory to save the output files.')
    parser.add_argument('--max_chars', type=int, default=4990, help='Maximum characters per line in the output file.')

    args = parser.parse_args()
    main(args.input_folder, args.output_folder, args.max_chars)