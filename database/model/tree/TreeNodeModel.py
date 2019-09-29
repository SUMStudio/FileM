from typing import Set

from database.model.NodeModel import NodeModel


class TreeNodeModel(NodeModel):
    def __init__(self, concept_id: int, is_obj=False, node_id: int = -1, value: Set[str] = None,is_root:bool=False):
        NodeModel.__init__(self, node_id)
        # 标志他来自哪个概念
        self.concept_id: int = concept_id
        # 节点的值
        if value:
            self.value: Set[str] = value
        else:
            self.value = set()
        # 判断节点是否是文件
        self.is_obj = is_obj
        # 是否为根节点
        self.is_root = is_root

    # 打印对象
    def __str__(self):
        info = dict()
        info['tree_id'] = self.id
        info['concept_index'] = self.concept_id
        info['value'] = self.value
        info['is_obj'] = self.is_obj
        return str(info)
