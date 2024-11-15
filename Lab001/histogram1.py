import argparse
from collections import Counter
from ascii_graph import Pyasciigraph
from ascii_graph import colors
from ascii_graph.colordata import vcolor
from rich.progress import track
import rich.traceback
import rich
import time
import collections
from _collections_abc import Iterable
collections.Iterable = Iterable

rich.traceback.install()

parser = argparse.ArgumentParser(description='Program making histogram of words in files')
parser.add_argument('filenames', nargs='+', type=str, help='filenames to process')
parser.add_argument('--limit', '-l', type=int, default=10, help='number of words to display')
parser.add_argument('--min_length', '-m', type=int, default=0, help='minimal lenght of the word')
parser.add_argument('--ignore_list', '-i', nargs='*', type=str, default=[], help='list of words to ignore')
parser.add_argument('--wanted_strings', '-w', nargs='*', type=str, default=[], help='list of wanted strings')
parser.add_argument('--unwanted_strings', '-u', nargs='*', type=str, default=[], help='list of unwanted strings')
args = parser.parse_args()

rich.get_console().clear()

for filename in args.filenames:
    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()
        words = file_content.split()

    filtered_words = [word for word in words if len(word) >= args.min_length] 
    filtered_words= [word for word in filtered_words if word not in args.ignore_list]
    if args.wanted_strings:
        filtered_words = [word for word in filtered_words if any(wanted_string in word for wanted_string in args.wanted_strings)]
    filtered_words = [word for word in filtered_words if not any(unwanted_string in word for unwanted_string in args.unwanted_strings)]
    word_counts = Counter(filtered_words).most_common(args.limit)
    color_scheme = [colors.IGre, colors.IYel, colors.IBlu, colors.IRed, colors.IPur, colors.ICya, colors.IWhi]
    colored_data = vcolor(word_counts, color_scheme)

    for i in track(range(5), description=f'Processing file {filename}'):
            time.sleep(0.5)

    rich.get_console().rule(f'Histogram of {filename}', style='bold magenta')
    graph = Pyasciigraph(graphsymbol='●')
    for line in graph.graph(data=colored_data):
        print(line)
    rich.get_console().rule(style='bold magenta')
