from typing import List, Set

from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from database.model.lattice.LatticeModel import LatticeModel
from database.model.tree.Lattice2TreeModel import Lattice2TreeModel
from database.model.tree.TreeNodeModel import TreeNodeModel


class LatticeEditor:
    def __init__(self, g_lb_name: str):
        self._g_lb_name = g_lb_name.replace('.', '')
        try:
            self._lattice_model = LatticeModel(self._g_lb_name + '_lattice')
            self._tree_model = Lattice2TreeModel(self._g_lb_name + '_tree')
        except Exception as e:
            print('连接数据库失败')
        pass

    def add_concept(self, new_concept: ConceptNodeModel):
        lattice_model = self._lattice_model
        # 概念格为空时
        if lattice_model.get_node_count() == 0:
            # 加入新概念
            lattice_model.add_node(new_concept)
            # 该节点既是sup节点也是inf节点
            lattice_model.set_inf_node(new_concept.id)
            lattice_model.set_sup_node(new_concept.id)
            print("初始化概念格")
            return
        else:
            inf = lattice_model.get_inf_node()
            if not new_concept.intents.issubset(inf.intents):
                if len(inf.extents) == 0:
                    inf.intents = inf.intents | new_concept.intents
                    # 在数据库中更新
                    lattice_model.update_node_property(inf.id, intents=inf.intents)
                else:
                    # 新建一个节点作为inf节点
                    new_inf = ConceptNodeModel(extents=set(), intents=inf.intents | new_concept.intents)
                    lattice_model.add_node(new_inf)
                    # 替换原有的inf节点
                    lattice_model.set_inf_node(new_inf.id)
                    lattice_model.remove_node_property(inf.id, 'is_inf')
                    # 加边
                    lattice_model.add_edge(inf.id, new_inf.id)
        # 存储已访问概念集合
        visited_cs: List[Set[int]] = list()
        # 遍历数据库按内涵势排序生成id
        for lattice_concept_id in lattice_model.get_node_id_order_by_intents_length():
            lattice_concept = lattice_model.get_node_base_on_id(lattice_concept_id)
            # 如果是更新概念
            if lattice_concept.intents.issubset(new_concept.intents):
                # 更新外延取并集
                lattice_concept.extents = lattice_concept.extents | new_concept.extents
                # 在数据库中更新
                lattice_model.update_node_property(lattice_concept.id, extents=lattice_concept.extents)
                # 记录访问节点
                LatticeModel.update_list(lattice_concept, visited_cs)
            else:
                new_intents = lattice_concept.intents & new_concept.intents
                # 若在已访问概念集合中，不存在概念内涵与new_intents相等，则产生新概念节点
                is_gen = True
                if len(visited_cs) > len(new_intents):
                    for visited_c_id in visited_cs[len(new_intents)]:
                        visited_c = lattice_model.get_node_base_on_id(visited_c_id)
                        if visited_c.intents == new_intents:
                            is_gen = False
                if is_gen:
                    gen_concept = ConceptNodeModel(intents=new_intents,
                                                   extents=lattice_concept.extents | new_concept.extents)
                    lattice_model.add_node(gen_concept)
                    # 连接生成节点和当前遍历节点
                    lattice_model.add_edge(node_id_from=gen_concept.id, node_id_to=lattice_concept.id)

                    # 该点加入已访问点集合
                    LatticeModel.update_list(gen_concept, visited_cs)
                    # 找父概念来更新边
                    # 遍历交集集合
                    for index in range(0, len(gen_concept.intents)):
                        for visited_c_id in visited_cs[index]:
                            visited_c = lattice_model.get_node_base_on_id(visited_c_id)
                            if visited_c.intents.issubset(gen_concept.intents):
                                # 潜在的父节点
                                parent = True
                                for child_id in lattice_model.get_children(visited_c_id):
                                    child = lattice_model.get_node_base_on_id(child_id)
                                    if child.intents.issubset(gen_concept.intents):
                                        parent = False
                                        break
                                if parent:
                                    if lattice_model.is_parent(visited_c, lattice_concept):
                                        # 是父子关系就消边
                                        lattice_model.remove_edge(visited_c.id, lattice_concept.id)
                                    # 与生成子加边
                                    lattice_model.add_edge(visited_c.id, gen_concept.id)

        # 更新sup节点标记
        sup = lattice_model.get_sup_node()
        lattice_model.remove_node_property(sup.id, "is_sup")
        lattice_model.set_sup_node()

    def remove_attribute(self, attribute: str):
        lattice_model = self._lattice_model
        # 已访问过的节点
        visit: List[int] = list()
        # 判断该节点是否已判断过
        vs: Set[int] = set()
        # 该节点为更新或删除节点
        cs: Set[int] = set()
        # 保存待处理的删除和更新的节点
        all_concepts: List[int] = [lattice_model.get_inf_node().id]
        # 如果节点只剩下一个，且其內延移除后为空，则直接移除整个格
        if lattice_model.get_node_count() == 1:
            concept = lattice_model.get_node_base_on_id(all_concepts[0])
            if (attribute in concept.intents) & len(concept.intents) == 1:
                lattice_model.delete_all()
                return
        # 自底向上开始遍历
        while len(all_concepts) != 0:
            # 选取最底层的节点
            concept_id = all_concepts.pop()
            concept = lattice_model.get_node_base_on_id(concept_id)
            # 若属性在内涵里
            if attribute in concept.intents:
                # 移除掉这个属性
                concept.intents.remove(attribute)
                # 在数据库中更新
                lattice_model.update_node_property(concept.id, intents=concept.intents)
            # 节点C的删除基节点
            concept_db: ConceptNodeModel = ConceptNodeModel(set(), set())
            # 遍历他的父节点
            for concept_parent_id in lattice_model.get_parents(concept.id):
                concept_parent = lattice_model.get_node_base_on_id(concept_parent_id)
                # 若原删除基节点为空，且选取节点移除属性后于其父节点属性相同
                if (concept_db.id == -1) & (concept.intents == concept_parent.intents):
                    # 那么这个父节点就是删除基节点，该待处理节点为删除节点，记录删除节点的删除基节点
                    concept_db = concept_parent
                    # 如果这个节点恰好是inf节点
                    inf = lattice_model.get_inf_node()
                    if concept.id == inf.id:
                        # 则其父节点充当其成为新的inf节点
                        lattice_model.set_inf_node(concept_parent.id)

                # 如果他的父节点不是删除基节点的话，那么这个父节点有可能是保留节点、更新节点或删除节点
                else:
                    # 若该父节点未被访问，且满足当前遍历节点删除基节点不为空 或 删除属性在父节点属性集合中
                    if (concept_parent_id not in vs) & (
                            (concept_db.id != -1) | (attribute in concept_parent.intents)):
                        # 再添加父节点到遍历列表all_concepts尾部
                        all_concepts.append(concept_parent_id)
                        # 父节点置cs标志位
                        cs.add(concept_parent_id)
                    # 添加父节点到保持访问过的节点集合尾
                    visit.append(concept_parent_id)
                    # 父节点置vs标志位
                    vs.add(concept_parent_id)

            # 如果存在删除基节点，那么就需要对删除节点的边进行调整
            if concept_db.id != -1:
                # 遍历删除节点的子节点c
                for concept_child_id in lattice_model.get_children(concept.id):
                    concept_child = lattice_model.get_node_base_on_id(concept_child_id)
                    # 用于标志删除基节点和删除节点子节点间是否新增边
                    need_edge = True
                    # 遍历删除节点的子节点的父节点Ccp
                    for concept_c_p_id in lattice_model.get_parents(concept_child.id):
                        concept_c_p = lattice_model.get_node_base_on_id(concept_c_p_id)
                        # 若Ccp没有cs标记，即不是更新或删除节点
                        # 且 Ccp不是原节点C
                        # 且 Ccp的外延包含于Cdb删除基外延(即两个节点间已经存在了偏序关系)
                        if (concept_c_p not in cs) & (concept_c_p != concept) & concept_c_p.extents.issubset(
                                concept_db.extents):
                            # 那么不需要新增边
                            need_edge = False
                            break
                    if need_edge:
                        # 新增边
                        lattice_model.add_edge(concept_db.id, concept_child.id)
                # 删除节点及其关联的边
                lattice_model.delete_node(concept.id)
            # 若删除基节点不存在，即无删除节点
            else:
                # 取消该节点的cs标记
                cs.discard(concept.id)
        # TODO  取消集合VSet中节点的vs标记

    # 与remove_attribute形成对偶
    def remove_object(self, object: str):
        lattice_model = self._lattice_model
        # 已访问过的节点
        visit: List[int] = list()
        # 判断该节点是否已判断过
        vs: Set[int] = set()
        # 该节点为更新或删除节点
        cs: Set[int] = set()
        # 保存待处理的删除和更新的节点
        all_concepts: List[int] = [lattice_model.get_sup_node().id]
        # 如果节点只剩下一个，且其外延移除后为空，则直接移除整个格
        if lattice_model.get_node_count() == 1:
            concept = lattice_model.get_node_base_on_id(all_concepts[0])
            if (object in concept.extents) & len(concept.extents) == 1:
                lattice_model.delete_all()
                return
        # 自顶向下开始遍历
        while len(all_concepts) != 0:
            # 选取最底层的节点
            concept_id = all_concepts.pop()
            concept = lattice_model.get_node_base_on_id(concept_id)
            # 若属性在外延里
            if object in concept.extents:
                # 移除掉这个对象
                concept.extents.remove(object)
                # 在数据库中更新这个节点
                lattice_model.update_node_property(concept.id, extents=concept.extents)
            # 节点C的删除基节点
            concept_db: ConceptNodeModel = ConceptNodeModel(set(), set())
            # 遍历他的子节点
            for concept_child_id in lattice_model.get_children(concept.id):
                concept_child = lattice_model.get_node_base_on_id(concept_child_id)
                # 若原删除基节点为空，且选取节点移除对象后与其子节点对象相同
                if (concept_db.id == -1) & (concept.extents == concept_child.extents):
                    # 那么这个子节点就是删除基节点，该待处理节点为删除节点，记录删除节点的删除基节点
                    concept_db = concept_child
                    # 如果这个节点恰好是sup节点
                    sup = lattice_model.get_sup_node()
                    if concept.id == sup.id:
                        # 则其子节点充当其成为新的sup节点
                        lattice_model.set_sup_node(concept_child.id)

                # 如果他的子节点不是删除基节点的话，那么这个子节点有可能是保留节点、更新节点或删除节点
                else:
                    # 若该子节点未被访问，且满足当前遍历节点删除基节点不为空 或 删除属性在子节点属性集合中
                    if (concept_child_id not in vs) & (
                            (concept_db.id != -1) | (object in concept_child.extents)):
                        # 再添加子节点到遍历列表all_concepts尾部
                        all_concepts.append(concept_child_id)
                        # 子节点为更新或删除节点
                        cs.add(concept_child_id)
                    # 添加子节点到保持访问过的节点集合尾
                    visit.append(concept_child_id)
                    # 子节点置vs标志位
                    vs.add(concept_child_id)

            # 如果存在删除基节点，那么就需要对删除节点的边进行调整
            if concept_db.id != -1:
                # 遍历删除节点的父节点
                for concept_parent_id in lattice_model.get_parents(concept.id):
                    concept_parent = lattice_model.get_node_base_on_id(concept_parent_id)
                    # 用于标志删除基节点和删除节点子节点间是否新增边
                    need_edge = True
                    # 遍历删除节点的父节点的子节点Cpc
                    for concept_p_c_id in lattice_model.get_children(concept_parent_id):
                        concept_p_c = lattice_model.get_node_base_on_id(concept_p_c_id)
                        # 若Cpc没有cs标记，即不是更新或删除节点
                        # 且 Cpc不是原节点C
                        # 且 Cdb删除基内涵包含于Cpc的内涵(即两个节点间已经存在了偏序关系)
                        if (concept_p_c not in cs) & (concept_p_c != concept) & concept_db.intents.issubset(
                                concept_p_c.intents):
                            # 那么不需要新增边
                            need_edge = False
                            break
                    if need_edge:
                        # 新增边
                        lattice_model.add_edge(concept_parent.id, concept_db.id)

                # 删除删除节点
                lattice_model.delete_node(concept.id)
            # 若删除基节点不存在，即无删除节点
            else:
                # 取消该节点的cs标记
                cs.discard(concept.id)
        # TODO  取消集合VSet中节点的vs标记

    def translate_lattice_to_tree(self):
        tree_model = self._tree_model
        lattice_model = self._lattice_model
        # 先清空树
        tree_model.delete_all()

        sup = lattice_model.get_sup_node()
        count = 0
        # 遍历数据库按内涵势排序生成id
        for lattice_concept_id in lattice_model.get_node_id_order_by_intents_length():
            lattice_concept = lattice_model.get_node_base_on_id(lattice_concept_id)
            # 对sup节点处理
            if lattice_concept.id == sup.id:
                # 如果sup节点内涵不为空
                if len(sup.intents) > 0:
                    # 创建root节点
                    root = TreeNodeModel(concept_id=-1, is_root=True, value={'root'})
                    tree_model.add_node(root)
                    # 创建sup对应树节点
                    tree_node = TreeNodeModel(concept_id=sup.id, value=sup.intents)
                    tree_model.add_node(tree_node)
                    # 连接两个树节点
                    tree_model.add_edge(-1, tree_node.id)
                    # 创建对象节点
                    tree_node_obj = TreeNodeModel(concept_id=sup.id, value=sup.extents, is_obj=True)
                    tree_model.add_node(tree_node_obj)
                    # 加边 孩子和文件加边
                    tree_model.add_edge_obj(parent=tree_node.id, child=tree_node_obj.id)
                else:
                    # 创建root节点
                    root = TreeNodeModel(concept_id=sup.id, is_root=True, value={'root'})
                    tree_model.add_node(root)
            # 遍历孩子
            for child_id in lattice_model.get_children(lattice_concept_id):
                child = lattice_model.get_node_base_on_id(child_id)
                if len(child.extents) == 0:
                    break
                # 取属性差集
                attri_exc = child.intents - lattice_concept.intents
                # 创建孩子节点
                tree_node = TreeNodeModel(concept_id=child_id, value=set(attri_exc))
                tree_model.add_node(tree_node)
                print(tree_node)
                count += 1
                # 加边
                tree_model.add_edge(parent=lattice_concept.id, child=tree_node.id)
                # 创建对象节点
                tree_node_obj = TreeNodeModel(concept_id=child_id, value=child.extents, is_obj=True)
                tree_model.add_node(tree_node_obj)
                print(tree_node_obj)
                count += 1
                # 加边 孩子和文件加边
                tree_model.add_edge_obj(parent=tree_node.id, child=tree_node_obj.id)
        print(count)

    @property
    def lattice_model(self):
        return self._lattice_model

    @property
    def tree_model(self):
        return self._tree_model
