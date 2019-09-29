
from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from database.model.lattice.LatticeModel import LatticeModel
import database.util.CSVReader as Csv_reader
import database.util.RCFReader as Rcf_reader
from database.model.tree.Lattice2TreeModel import Lattice2TreeModel
from database.util.ConstructeLattice import add_concept, remove_attribute, remove_object
from database.util.Lattice2Tree import translate_lattice_to_tree


def import_from_csv(lattice_model: LatticeModel, path: str = None, max_line: int = 30):
    # 从CSV导入
    if path is None:
        path = 'D:\\python工作空间\\概念格算法\\godin算法实现\\example.csv'
    for concept in Csv_reader.read_csv(path, max_line):
        add_concept(new_concept=concept, lattice_model=lattice_model)


def import_from_rcf(lattice_model: LatticeModel):
    # 从RCF导入
    for concept in Rcf_reader.read_rcf('c:\\Users\\lijunan\\Desktop\\jabref\\example.rcf'):
        add_concept(new_concept=concept, lattice_model=lattice_model)


def import_from_example(lattice_model: LatticeModel):
    # 生成例子
    concept1 = ConceptNodeModel(intents={'a1', 'a2'}, extents={'o1', 'o2'})
    concept2 = ConceptNodeModel(intents={'a3', 'a2'}, extents={'o2', 'o5'})
    concept3 = ConceptNodeModel(intents={'a4', 'a2'}, extents={'o3', 'o2'})
    concept4 = ConceptNodeModel(intents={'a5', 'a3'}, extents={'o4', 'o5'})
    concept5 = ConceptNodeModel(intents={'a6', 'a1'}, extents={'o2', 'o7'})
    concept6 = ConceptNodeModel(intents={'a3', 'a1'}, extents={'o4', 'o8'})

    concept_set = [concept1, concept2, concept3, concept4, concept5, concept6]

    # 遍历所有待加入的概念
    for concept in concept_set:
        add_concept(new_concept=concept, lattice_model=lattice_model)


if __name__ == '__main__':
    # 导入文件名
    file_name = 'music.csv'
    lattice_model1 = LatticeModel(file_name.replace('.', '') + '_lattice')
    # 清空标签下的所有节点
    lattice_model1.delete_all()
    # 导入节点
    import_from_csv(lattice_model1, file_name, 20)

    tree_model = Lattice2TreeModel(file_name.replace('.', '') + '_tree')
    # 清空标签下所有节点
    tree_model.delete_all()
    translate_lattice_to_tree(lattice_model=lattice_model1, tree_model=tree_model)
    # print(tree_model)
    # tree_data = tree_model_to_tree_data(tree_model=tree_model, root_name='根目录')
    # print(tree_data)
    # main_page([tree_data]).render()
    # pos_array, text_dict, edge_list = translate_3d_info(lattice_model1)
    # axview = MainAxesView(pos_array, text_dict, edge_list)
    # axview.main_ax()
    # try:
    #     remove_attribute(lattice_model1, 'asf')
    #     remove_object(lattice_model1, '9')
    #     print(lattice_model1)
    # except Exception as err:
    #     print(err)
