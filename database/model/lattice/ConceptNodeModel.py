from typing import Set

from database.model.NodeModel import NodeModel


class ConceptNodeModel(NodeModel):
    def __init__(self, intents: Set[str], extents: Set[str], node_id: int = -1):
        # 继承父类方法
        NodeModel.__init__(self, node_id)
        self.intents: Set[str] = intents
        self.extents: Set[str] = extents


