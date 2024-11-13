import argparse
from file_operations import main as file_operations_main
from utils import setup_logging

if __name__ == '__main__':
    setup_logging()
    parser = argparse.ArgumentParser(description='Merge and translate text files.')
    parser.add_argument('--input_folder', type=str, default='./txt', help='Directory containing text files to merge.')
    parser.add_argument('--output_folder', type=str, default='./', help='Directory to save the output files.')
    parser.add_argument('--max_chars', type=int, default=4990, help='Maximum characters per line in the output file.')
    parser.add_argument('--target_language', type=str, default='id', help='Target language for translation (e.g., "id" for Indonesian).')

    args = parser.parse_args()
    file_operations_main(args.input_folder, args.output_folder, args.max_chars, args.target_language)