from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from typing import List


def read_rcf(path: str):
    with open(path) as f:
        file_list = f.readlines()
    extents_list = file_list[4].split('|')
    intents_list = file_list[5].split('|')
    remove_newline(extents_list)
    remove_newline(intents_list)
    matrix: List[List[str]] = list()
    for i in range(6, len(file_list) - 1):
        if len(file_list[i]) <= 1:
            continue
        temp_list: List[str] = file_list[i].split(' ')
        remove_newline(temp_list)
        matrix.append(temp_list)
    for i, extents in enumerate(extents_list):
        concept = ConceptNodeModel(extents={extents}, intents=set())
        for j, intents in enumerate(intents_list):
            if matrix[i][j] == '1':
                concept.intents.add(intents)
        # print(concept)
        yield concept


def remove_newline(l: list):
    for i, x in enumerate(l):
        x = x.strip()
        l[i] = x
        if x == '':
            l.remove(x)


if __name__ == '__main__':
    read_rcf('c:\\Users\\lijunan\\Desktop\\jabref\\example.rcf')
