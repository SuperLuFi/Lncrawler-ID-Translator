import logging
from deep_translator import GoogleTranslator
import progressbar
import multiprocessing

def translate_line(line, target_language):
    """Translate a single line using GoogleTranslator"""
    kalimat = line.strip()
    if kalimat:
        try:
            terjemahan = GoogleTranslator(source='auto', target=target_language).translate(text=kalimat)
            return terjemahan
        except Exception as e:
            logging.error(f"Translation error for line: {kalimat}. Error: {e}")
            return kalimat  # Return the original line in case of error
    else:
        return ''

def translate_line_with_target(args):
    """Wrapper function to unpack arguments for translation"""
    line, target_language = args
    return translate_line(line, target_language)

def translate_file(file_path, target_language):
    with open(file_path, 'r', encoding='UTF-8') as isi_file:
        lines = isi_file.read().splitlines()

    logging.info("Translating ...")

    # Create progress bar with explicit initialization
    bar = progressbar.ProgressBar(
        maxval=len(lines) or 1,
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

    translated_lines = []
    with multiprocessing.Pool() as pool:
        bar.start()
        try:
            # Prepare arguments for translation
            args = [(line, target_language) for line in lines]
            for i, result in enumerate(pool.imap(translate_line_with_target, args), 1):
                translated_lines.append(result)
                bar.update(i)
        except Exception as e:
            logging.error(f"Translation error: {e}")
        finally:
            bar.finish()

    return translated_lines