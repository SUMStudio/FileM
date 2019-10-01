from database.algo.ConceptAlgo import ConceptAlgo
from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from database.model.lattice.LatticeModel import LatticeModel
from typing import Set, List
import copy


def add_concept(lattice_model: LatticeModel, new_concept: ConceptNodeModel):
    # 概念格为空时
    if lattice_model.get_node_count() == 0:
        # 初始化最顶层节点
        sup  = ConceptNodeModel(intents=set(),extents=new_concept.extents)
        lattice_model.add_node(sup)
        lattice_model.set_sup_or_inf_node(sup.id, 0)
        # 初始化最底层节点
        inf = ConceptNodeModel(intents=new_concept.intents, extents=set())
        lattice_model.add_node(inf)
        lattice_model.set_sup_or_inf_node(inf.id, 1)
        # 加入新概念
        lattice_model.add_node(new_concept)
        # 连接新概念和上下两个节点
        lattice_model.add_edge(node_id_from=sup.id,node_id_to=new_concept.id)
        lattice_model.add_edge(node_id_from=new_concept.id, node_id_to=inf.id)
        print("初始化概念格")
        return
    # 加入新属性时
    # 取底层节点
    inf = lattice_model.get_node_base_on_category(1)
    if not (ConceptAlgo.is_inclusion(new_concept.intents, inf.intents)):
        if len(inf.extents) == 0:
            new_intents = inf.intents | new_concept.intents
            # 在数据库中更新内涵
            lattice_model.update_node_property(node_id=inf.id, intents=new_intents)
    # 存储不同内涵势取交集后概念集合的集合
    all_intersection_concepts: List[Set[int]] = list()
    # 取最顶层节点
    sup = lattice_model.get_node_base_on_category(0)
    # 更新其外延
    lattice_model.update_node_property(sup.id,extents = sup.extents|new_concept.extents)
    # 该节点加入交集集合
    LatticeModel.update_list(sup, all_intersection_concepts)
    # 遍历数据库按内涵势排序生成id
    for lattice_concept_id in lattice_model.get_node_id_order_by_intents_length():
        lattice_concept = lattice_model.get_node_base_on_id(lattice_concept_id)
        # 判断属于哪种情况
        is_update_concept, is_generate_new_concept = ConceptAlgo.get_intersection_result(
            lattice_concept.intents,
            new_concept.intents,
            all_intersection_concepts, lattice_model)
        # 更新概念
        if is_update_concept & (lattice_concept_id != inf.id):
            # 更新外延取并集
            lattice_concept.extents = lattice_concept.extents | new_concept.extents
            # 在数据库中更新
            lattice_model.update_node_property(lattice_concept.id, extents=lattice_concept.extents)
            # 该概念加入交集集合
            LatticeModel.update_list(lattice_concept, all_intersection_concepts)
            # 内涵相等则结束算法(双包含=相等）
            if ConceptAlgo.is_inclusion(new_concept.intents, lattice_concept.intents):
                return
        # 产生新概念
        elif is_generate_new_concept:
            generate_concept = ConceptNodeModel(intents=set(lattice_concept.intents & new_concept.intents),
                                                extents=set(lattice_concept.extents | new_concept.extents))
            # 拓展矩阵,加点
            lattice_model.add_node(generate_concept)
            # 连接新边
            lattice_model.add_edge(node_id_from=generate_concept.id, node_id_to=lattice_concept.id)
            # 该点加入交集集合
            LatticeModel.update_list(generate_concept, all_intersection_concepts)
            # 找父概念来更新边
            # 遍历交集集合
            for index in range(0, len(generate_concept.intents)):
                for concept_intersection_id in all_intersection_concepts[index]:
                    concept_intersection = lattice_model.get_node_base_on_id(concept_intersection_id)
                    if ConceptAlgo.is_properly_inclusion(concept_intersection.intents, generate_concept.intents):
                        # 潜在的父节点
                        parent = True
                        for children_id in lattice_model.get_children(concept_intersection.id):
                            children = lattice_model.get_node_base_on_id(children_id)
                            if ConceptAlgo.is_properly_inclusion(
                                    children.intents, generate_concept.intents):
                                parent = False
                        if parent:
                            if lattice_model.is_parent(concept_intersection, lattice_concept):
                                # 是父子关系就消边
                                lattice_model.remove_edge(concept_intersection.id, lattice_concept.id)
                            # 与生成子加边
                            lattice_model.add_edge(concept_intersection.id, generate_concept.id)
            # 内涵相等结束算法
            if ConceptAlgo.is_equal(new_concept.intents, generate_concept.intents) & ConceptAlgo.is_inclusion(
                    generate_concept.intents, new_concept.intents):
                return


def remove_attribute(lattice_model: LatticeModel, attribute: str):
    # 先判断这个属性在不在格里
    inf = lattice_model.get_node_base_on_category(1)
    if attribute not in inf.intents:
        raise Exception('格中没有这个属性', attribute)
    inf.intents.remove(attribute)
    # 已访问过的节点
    # visit: Set[int] = set()
    # 判断该节点是否已判断过
    vs: Set[int] = set()
    # 该节点为更新或删除节点
    cs: Set[int] = set()
    # 保存待处理的删除和更新的节点,最后一个节点inf单独处理,且第一个节点不需要遍历
    all_concepts: List[int] = list()
    for concept in lattice_model.get_node_id_order_by_intents_length()[1:-1]:
        all_concepts += concept
    # 自底向上开始遍历
    while len(all_concepts) != 0:
        # 选取最底层的节点
        concept_id = all_concepts.pop()
        concept = lattice_model.get_node_base_on_id(concept_id)
        # 若属性在内涵里
        if attribute in concept.intents:
            # 移除掉这个属性 并 更新其在内涵势中位置
            new_intents: set = copy.deepcopy(concept.intents)
            new_intents.remove(attribute)
            # 在数据库中更新
            lattice_model.update_node_property(concept.id, intents = new_intents)
        # 节点C的删除基节点
        concept_db: ConceptNodeModel = ConceptNodeModel(set(), set())
        # 遍历他的父节点
        for concept_parent_id in lattice_model.get_parents(concept.id):
            concept_parent = lattice_model.get_node_base_on_id(concept_parent_id)
            # 若原删除基节点为空，且选取节点移除属性后于其父节点属性相同
            if (concept_db.id == -1) & (ConceptAlgo.is_equal(concept.intents, concept_parent.intents)):
                # 那么这个父节点就是删除基节点，该待处理节点为删除节点，记录删除节点的删除基节点
                concept_db = concept_parent

            # 如果他的父节点不是删除基节点的话，那么这个父节点有可能是保留节点、更新节点或删除节点
            else:
                # 若该父节点未被访问，且满足当前遍历节点删除基节点不为空 或 删除属性在父节点属性集合中
                if (concept_parent_id not in vs) & (
                        (concept_db.id != -1) | (attribute in concept_parent.intents)):
                    # 那么先移除父节点
                    all_concepts.remove(concept_parent_id)
                    # 再添加父节点到遍历列表all_concepts尾部
                    all_concepts.append(concept_parent_id)
                    # 父节点为更新或删除节点
                    cs.add(concept_parent_id)
                # TODO  添加父节点到保持访问过的节点集合 当知道VSet有何意义
                # visit.add(concept_parent_index)
                # 父节点置已访问标志位
                vs.add(concept_parent_id)

        # 如果存在删除基节点，那么就需要对删除节点的边进行调整
        if concept_db.id != -1:
            # 遍历删除节点的子节点
            for concept_child_id in lattice_model.get_children(concept.id):
                concept_child= lattice_model.get_node_base_on_id(concept_child_id)
                # 用于标志删除基节点和删除节点子节点间是否新增边
                need_edge = True
                # 遍历删除节点的子节点的父节点Ccp
                for concept_c_p_id in lattice_model.get_parents(concept_child.id):
                    concept_c_p = lattice_model.get_node_base_on_id(concept_c_p_id)
                    # 若Ccp没有cs标记，即不是更新或删除节点
                    # 且 Ccp不是原节点C
                    # 且 Ccp的外延包含于Cdb删除基外延(即两个节点间已经存在了偏序关系)
                    if (concept_c_p not in cs) & (concept_c_p != concept) & (
                            ConceptAlgo.is_inclusion(concept_c_p.extents, concept_db.extents)):
                        # 那么不需要新增边
                        need_edge = False
                        break
                if need_edge:
                    # 新增边
                    lattice_model.add_edge(concept_db.id, concept_child.id)
            # 删除删除节点
            lattice_model.delete_node(concept.id)

        # 若删除基节点不存在，即无删除节点
        else:
            # 取消该节点的cs标记
            cs.discard(concept.id)
        # TODO  取消集合VSet中节点的vs标记 当知道VSet有何意义
    # 遍历完成后，对最底层inf节点进行处理
    # 若其父节点只有一个，那么显然该父节点应该删除，由Inf节点代替他
    inf = lattice_model.get_node_base_on_category(1)
    parents = lattice_model.get_parents(inf.id)
    if len(parents) == 1:
        parent_id= parents.pop()
        # 将父节点增加category属性,则原inf节点删除
        lattice_model.set_sup_or_inf_node(parent_id,1)
        # 移除原Inf节点
        lattice_model.delete_node(inf.id)


# 与remove_attribute形成对偶
def remove_object(lattice_model: LatticeModel, object: str):
    # 先判断这个属性在不在格里
    sup = lattice_model.get_node_base_on_category(0)
    if object not in sup.extents:
        raise Exception('格中没有这个对象', object)
    sup.extents.remove(object)
    # 已访问过的节点
    # visit: Set[int] = set()
    # 判断该节点是否已判断过
    vs: Set[int] = set()
    # 该节点为更新或删除节点
    cs: Set[int] = set()
    # 保存待处理的删除和更新的节点,第一个节点sup独处理,且最后一个节点不需要遍历
    all_concepts: List[int] = list()
    for concept in lattice_model.get_node_id_order_by_intents_length_desc()[1:-1]:
        all_concepts += concept
    # 自顶向下开始遍历
    while len(all_concepts) != 0:
        # 选取最底层的节点
        concept_id = all_concepts.pop()
        concept = lattice_model.get_node_base_on_id(concept_id)
        # 若属性在外延里
        if object in concept.extents:
            # 移除掉这个对象
            concept.extents.remove(object)
        # 节点C的删除基节点
        concept_db: ConceptNodeModel = ConceptNodeModel(set(), set())
        # 遍历他的子节点
        for concept_child_id in lattice_model.get_children(concept.id):
            concept_child = lattice_model.get_node_base_on_id(concept_child_id)
            # 若原删除基节点为空，且选取节点移除对象后与其子节点属性相同
            if (concept_db.id == -1) & (ConceptAlgo.is_equal(concept.extents, concept_child.extents)):
                # 那么这个子节点就是删除基节点，该待处理节点为删除节点，记录删除节点的删除基节点
                concept_db = concept_child

            # 如果他的子节点不是删除基节点的话，那么这个子节点有可能是保留节点、更新节点或删除节点
            else:
                # 若该子节点未被访问，且满足当前遍历节点删除基节点不为空 或 删除属性在子节点属性集合中
                if (concept_child_id not in vs) & (
                        (concept_db.id != -1) | (object in concept_child.extents)):
                    # 那么先移除子节点
                    all_concepts.remove(concept_child_id)
                    # 再添加子节点到遍历列表all_concepts尾部
                    all_concepts.append(concept_child_id)
                    # 父节点为更新或删除节点
                    cs.add(concept_child_id)
                # TODO  添加子节点到保持访问过的节点集合 当知道VSet有何意义
                # visit.add(concept_parent_index)
                # 子节点置已访问标志位
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
                    if (concept_p_c not in cs) & (concept_p_c != concept) & (
                            ConceptAlgo.is_inclusion(concept_db.intents, concept_p_c.intents)):
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
        # TODO  取消集合VSet中节点的vs标记 当知道VSet有何意义
    # 遍历完成后，对最顶层sup节点进行处理
    # 若其子节点只有一个，那么显然该子节点应该删除，由sup节点代替他
    children = lattice_model.get_children(sup.id)
    if len(children) == 1:
        child_id = children.pop()
        # 将子节点增加category属性,则原sup节点删除
        lattice_model.set_sup_or_inf_node(child_id, 0)
        # 移除原inf节点
        lattice_model.delete_node(sup.id)