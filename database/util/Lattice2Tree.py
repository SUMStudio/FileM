from database.model.lattice.LatticeModel import LatticeModel
from database.model.tree.Lattice2TreeModel import Lattice2TreeModel
from database.model.tree.TreeNodeModel import TreeNodeModel


def translate_lattice_to_tree(lattice_model: LatticeModel, tree_model: Lattice2TreeModel):
    count = 0
    # 遍历数据库按内涵势排序生成id
    for lattice_concept_id in lattice_model.get_node_id_order_by_intents_length():
        lattice_concept = lattice_model.get_node_base_on_id(lattice_concept_id)
        # 先创建根节点
        if len(lattice_concept.intents) == 0:
            tree_node = TreeNodeModel(concept_id=lattice_concept.id,value={'root'},is_root=True)
            tree_model.add_node(tree_node)
            print(tree_node)
        # 最底层节点不遍历
        if len(lattice_concept.extents) == 0:
            continue
        # 判断该概念是否已经建立过父子关系
        #if tree_model.is_children_exist(lattice_concept):
            #continue
        # 遍历孩子
        for child_id in lattice_model.get_children(lattice_concept_id):
            child = lattice_model.get_node_base_on_id(child_id)
            if len(child.extents) == 0:
                continue
            # 取属性差集
            attri_exc = child.intents - lattice_concept.intents
            # 创建孩子节点
            tree_node = TreeNodeModel(concept_id=child_id, value=set(attri_exc))
            tree_model.add_node(tree_node)
            print(tree_node)
            count+=1
            # 加边
            tree_model.add_edge(parent=lattice_concept.id, child=tree_node.id)
            # 创建对象节点
            tree_node_obj = TreeNodeModel(concept_id=child_id, value=child.extents, is_obj=True)
            tree_model.add_node(tree_node_obj)
            print(tree_node_obj)
            count+=1
            # 加边 孩子和文件加边
            tree_model.add_edge_obj(parent=tree_node.id, child=tree_node_obj.id)
    print(count)