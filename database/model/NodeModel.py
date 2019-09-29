from typing import Set


class NodeModel:
    def __init__(self, node_id: int):
        # 图节点序号
        self._id: int = node_id
        # 存储孩子节点
        self._node_children: Set[int] = set()
        # 存储父亲节点
        self._node_parents: Set[int] = set()

    @property
    def id(self):
        return self._id

    @property
    def node_children(self) -> set:
        return self._node_children

    @property
    def node_parents(self) -> set:
        return self._node_parents

    @id.setter
    def id(self, value: int):
        self._id = value

    @node_children.setter
    def node_children(self, children: set):
        self._node_children = children

    @node_parents.setter
    def node_parents(self, parents: set):
        self._node_parents = parents
