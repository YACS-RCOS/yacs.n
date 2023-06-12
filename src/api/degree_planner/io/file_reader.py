import csv

NOUNS_PATH = 'data/dictionary/parts of speech/nouns.csv'
VERBS_PATH = 'data/dictionary/parts of speech/verbs.csv'
ADVERBS_PATH = 'data/dictionary/parts of speech/adverbs.csv'
ADJECTIVES_PATH = 'data/dictionary/parts of speech/adjectives.csv'

def import_csv_as_set(file_path) -> set:
    file = open(file_path, 'r')
    data_set = set()
    reader = csv.reader(file, delimiter=',')
    
    for row in reader:
        for e in row:
            data_set.add(e)

    return data_set