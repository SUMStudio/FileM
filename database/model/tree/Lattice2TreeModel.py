from database.model.GraphModel import GraphModel
from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from database.model.tree.TreeNodeModel import TreeNodeModel


class Lattice2TreeModel(GraphModel):
    def __init__(self, label):
        # 继承父类方法
        GraphModel.__init__(self, label, 'child')
        self._label = label

    # 添加一个节点
    def add_node(self, tree_node: TreeNodeModel = None):
        if tree_node:
            node_id = super(Lattice2TreeModel, self).add_node(concept_id=tree_node.concept_id, value=tree_node.value,
                                                              is_obj=tree_node.is_obj, is_root=tree_node.is_root)
        else:
            node_id = super(Lattice2TreeModel, self).add_node()
        tree_node.id = node_id

    def add_edge(self, parent: int, child: int):
        # 概念节点与树节点是一对多的关系
        # 因此由一个父概念生成的树节点会出现在多个子树下（前提是该父概念存在多个父概念）
        # 我们一次性该父概念生成的所有树节点的边都添加上
        # 那么下次再由该节点作为父节点时，就不需要再进行一次遍历了
        statement = "match (f:{0}),(t:{0}) where f.concept_id={1} and f.is_obj=false and id(t)={2} merge (f)-[:{3}]->(t)".format(
            self._label, parent, child, 'child')
        super(Lattice2TreeModel, self).run_statement_without_return(statement)

    def add_edge_obj(self, parent: int, child: int):
        super(Lattice2TreeModel, self).add_edge(parent, child)

    # 取节点的所有孩子节点
    def get_children(self, parent_node_id: int):
        return super(Lattice2TreeModel, self).get_children(node_id_from=parent_node_id)

    # 拓展命令
    def is_children_exist(self, concept: ConceptNodeModel):
        statement = "match (n:{0})-[:child]->(c:{0}) where n.concept_id={1} and c.is_obj=false return count(c)".format(
            self._label, concept.id)
        statement_return = "count(c)"
        count = super(Lattice2TreeModel, self).run_statement(statement, statement_return).__next__()
        print(statement)
        print(count)
        if count > 0:
            return True
        return False

    # 取所有根节点到叶子节点的路径
    def get_root2leaf_path(self):
        statement = "MATCH p=(n:{0})-[*]->(r:{0}) where n.is_root=true and r.is_obj=true RETURN extract(x IN nodes(p)|x.value) as path".format(
            self._label)
        statement_return = "path"
        for path in super(Lattice2TreeModel, self).run_statement(statement, statement_return):
            yield path

    # 清空所有节点
    def delete_all(self):
        super(Lattice2TreeModel, self).delete_all()
