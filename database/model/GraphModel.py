# 拉链法存储图
from typing import TypeVar

from database.util.Neo4jDriverHelper import Neo4jDriverHelper

T = TypeVar('T')


class GraphModel:
    def __init__(self, label, relationship_name):
        # 初始化数据库
        self._neo4j = Neo4jDriverHelper(label=label)
        self._relationship_name = relationship_name

    # 添加一个节点
    def add_node(self, **properties) -> int:
        node_id = self._neo4j.add_node(**properties)
        return node_id

    # 删除一个节点及其相关边
    def delete_node(self, delete_node_id: int):
        self._neo4j.delete_node(delete_node_id)

    # 添加一条边
    def add_edge(self, node_id_from: int, node_id_to: int):
        self._neo4j.add_relationship(node_id_from=node_id_from, node_id_to=node_id_to,
                                     relationship_name=self._relationship_name)

    # 删除一条边
    def remove_edge(self, node_id_from: int, node_id_to: int):
        self._neo4j.remove_relationship(node_id_from=node_id_from, node_id_to=node_id_to,
                                        relationship_name=self._relationship_name)

    # 取节点的所有孩子节点
    def get_children(self, node_id_from: int):
        return self._neo4j.get_node_base_on_relationship(node_id_from=node_id_from,
                                                         relationship_name=self._relationship_name)

    # 取节点的所有父亲节点
    def get_parents(self, node_id_to: int):
        return self._neo4j.get_node_base_on_relationship(node_id_to=node_id_to,
                                                         relationship_name=self._relationship_name)

    # 取节点的数量
    def get_node_count(self) -> int:
        return self._neo4j.get_node_count()

    # 添加节点其他属性
    def add_node_property(self, node_id: int, **properties):
        self._neo4j.add_properties(node_id=node_id, **properties)

    # 修改节点的属性
    def update_node_property(self, node_id, **properties):
        self._neo4j.update_node_property(node_id, **properties)

    # 根据属性值取节点信息
    def get_node_base_on_property(self, property_name, value, limit=0):
        return self._neo4j.get_node_base_on_property(property_name, value, limit)

    # 根据ID取节点信息
    def get_node_base_on_id(self, node_id: int):
        return self._neo4j.get_node_base_on_id(node_id)

    # 节点排序输出id
    def get_node_order(self, order_statement):
        return self._neo4j.get_node_order(order_statement)

    # 节点逆序排序输出id
    def get_node_order_desc(self, order_statement):
        return self._neo4j.get_node_order_desc(order_statement)

    # 清空所有节点
    def delete_all(self):
        self._neo4j.delete_all()

    # 预留执行接口
    def run_statement(self, statement, statement_return):
        return self._neo4j.run_statement(statement, statement_return)

    def run_statement_without_return(self, statement):
        self._neo4j.run_statement_without_return(statement)