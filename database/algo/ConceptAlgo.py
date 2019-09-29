from typing import Set, List

from database.model.lattice.LatticeModel import LatticeModel


class ConceptAlgo:
    def __init__(self):
        pass

    @staticmethod
    def get_intersection_result(intents: set, add_intents: set, all_intersection_concepts: List[Set[int]],
                                lattice_model: LatticeModel):
        is_update_concept = False
        is_generate_new_concept = False
        intersection = intents & add_intents
        if len(intersection) == 0:
            pass
        elif ConceptAlgo.is_inclusion(intents, add_intents):
            is_update_concept = True
        else:
            if len(all_intersection_concepts) <= len(intersection):
                is_generate_new_concept = True
            else:
                for concept_id in all_intersection_concepts[len(intersection)]:
                    concept = lattice_model.get_node_base_on_id(concept_id)
                    # 同势概念内涵相等，则为重复节点不需要加入
                    if ConceptAlgo.is_equal(concept.intents, intersection):
                        is_generate_new_concept = False
                        break
                    else:
                        is_generate_new_concept = True

        return is_update_concept, is_generate_new_concept

    # 判断两个集合是否相等
    @staticmethod
    def is_equal(a: set, b: set) -> bool:
        return a==b

    # 判断集合a是否包含于集合b
    @staticmethod
    def is_inclusion(a: set, b: set) -> bool:
        return a.issubset(b)

    # 判断集合a是否包真含于集合b
    @staticmethod
    def is_properly_inclusion(a: set, b: set) -> bool:
        # 特殊情况
        if len(a) == len(b):
            return False
        return ConceptAlgo.is_inclusion(a, b)
