import csv
from database.model.lattice.ConceptNodeModel import ConceptNodeModel


def read_csv(path: str, max_line: int = -1):
    with open(path, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        if max_line == -1:
            max_line = len(reader)
        for index, line in enumerate(reader):
            if index == 0:
                continue
            if index < max_line:
                extents = {line[1]}
                intents = set(line[2].split('|'))
                yield ConceptNodeModel(extents=extents, intents=intents)
            else:
                break


if __name__ == '__main__':
    for concept in read_csv('C:\\Users\\lijunan\\Downloads\\movies.csv', 30):
        print(concept)
