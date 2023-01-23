import pickle
from argparse import ArgumentParser


def save_text_extraction(dic):
    with open('tmp.pickle', 'wb') as f:
        pickle.dump(dic, f)


def load_text_extraction():
    with open('tmp.pickle', 'rb') as f:
        obj = pickle.load(f)
    return obj


def read_command_line():
    parser = ArgumentParser()
    parser.add_argument("-k", "--keyword", dest="keyword",
                        help="The keyword to look in files")
    parser.add_argument("-d", "--dir", dest="dir_path", nargs='?',
                        help="The path where the pdf used for text extraction can be found.")
    parser.add_argument("-f", "--filter", dest="filter",
                        help="The minimum number of hits required for the paper to be printed to screen.")

    args = parser.parse_args()
    return args.keyword, args.dir_path or '', int(args.filter or "1")
