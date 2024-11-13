import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def multiline_to_single_line(input_file, output_file, max_chars=4990):
    try:
        with open(input_file, 'r', encoding="utf-8") as file:
            lines = file.readlines()
        
        lines = [line.strip() for line in lines if line.strip()]
        output_lines = []
        current_line = ''

        for line in lines:
            while len(line) > max_chars:
                output_lines.append(line[:max_chars])
                line = line[max_chars:]

            if len(current_line) + len(line) + (1 if current_line else 0) > max_chars:
                if current_line:
                    output_lines.append(current_line)
                current_line = line
            else:
                if current_line:
                    current_line += ' '
                current_line += line

        if current_line:
            output_lines.append(current_line)

        with open(output_file, 'w', encoding="utf-8") as file:
            for line in output_lines:
                file.write(line + '\n')

    except Exception as e:
        logging.error(f"Error processing multiline to single line: {e}")