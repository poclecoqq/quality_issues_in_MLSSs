from pypdf import PdfReader
from pathlib import Path
from tqdm import tqdm
import os
import re
from utils import save_text_extraction, load_text_extraction, read_command_line


def read_pdfs(dir):
    text_content = {}
    # Taken from: https://stackoverflow.com/questions/3883138/how-do-i-read-the-number-of-files-in-a-folder-using-python
    num_files = len([f for f in os.listdir(dir)
                     if os.path.isfile(os.path.join(dir, f))])
    for file in tqdm(dir.iterdir(), total=num_files):
        text = ""
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        text_content[file.name] = text
    return text_content


def search_texts(keyword, text_content, n_filter):
    for file_name in text_content:
        n_matches = len(re.findall(keyword, text_content[file_name]))
        if n_matches >= n_filter:
            print(f'File name:{file_name}; n matches: {n_matches}')


def main():
    keyword, dir_path, n_filter = read_command_line()

    # Text extraction from pdfs
    if dir_path != '':
        # /home/poclecoqq/files/ecole/maitrise/memoire/papers
        text_content = read_pdfs(Path(dir_path))
        save_text_extraction(text_content)

    # Search in texts the keyword
    text_content = load_text_extraction()
    search_texts(keyword, text_content, n_filter)


if __name__ == "__main__":
    main()
