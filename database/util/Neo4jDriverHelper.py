from neo4j.v1 import GraphDatabase


class Neo4jDriverHelper:

    def __init__(self, label, username='neo4j', password='123456'):
        self._driver = GraphDatabase.driver('bolt://localhost', auth=(username, password))
        self._label = label

    # 添加一个节点,并返回ID
    def add_node(self, **properties):
        properties_str = self.dict2str(properties)
        statement = "create (n:{}{}) return id(n)".format(self._label, properties_str)
        with self._driver.session() as session:
            result = session.run(statement)
        node_id = result.peek()["id(n)"]
        return node_id

    # 添加节点的属性
    def add_properties(self, node_id, **properties):
        properties_str = self.dict2str(properties)
        statement = "match (n:{}) where id(n)={} set n += {}".format(self._label, node_id,
                                                                     properties_str)
        with self._driver.session() as session:
            session.run(statement)

    # 修改节点的属性
    def update_node_property(self, node_id, **properties):
        statement = "match (n:{}) where id(n)={} set".format(self._label, node_id)
        for key, value in properties.items():
            if type(value) == set:
                value = list(value)
            if type(value) == list:
                #Neo4jDriverHelper.list2str(value)
                property_str = " n.{}={},".format(key, value)
                statement += property_str
        statement = statement[0:-1]
        with self._driver.session() as session:
            session.run(statement)

    # 添加节点间关系
    def add_relationship(self, node_id_from, node_id_to, relationship_name):
        statement = "match (f:{0}),(t:{0}) WHERE id(f)={1} and id(t)={2} merge (f)-[:{3}]->(t)".format(self._label,
                                                                                                       node_id_from,
                                                                                                       node_id_to,
                                                                                                       relationship_name)
        with self._driver.session() as session:
            session.run(statement)

    # 根据属性值取节点信息
    def get_node_base_on_property(self, property_name, value, limit=0):
        statement = ""
        if limit == 0:
            statement = "match (n:{}) where n.{}={} return n".format(self._label, property_name, value)
        elif limit > 0:
            statement = "match (n:{}) where n.{}={} return n limit {}".format(self._label, property_name, value,
                                                                              limit)

        statement_return = "n"
        with self._driver.session() as session:
            result = session.run(statement)
        for record in result:
            yield record[statement_return]

    # 根据ID取节点信息
    def get_node_base_on_id(self, node_id: int):
        statement = "match (n:{}) where id(n) = {} return n".format(self._label, node_id)
        statement_return = "n"
        with self._driver.session() as session:
            result = session.run(statement)
        return result.peek()[statement_return]

    # 删除节点间关系
    def remove_relationship(self, node_id_from, node_id_to, relationship_name):
        statement = "match (f:{0})-[r:{1}]->(t:{0}) where id(f)={2} and id(t)={3} delete r".format(self._label,
                                                                                                   relationship_name,
                                                                                                   node_id_from,
                                                                                                   node_id_to)

        with self._driver.session() as session:
            session.run(statement)

    # 根据边关系找节点列表
    def get_node_base_on_relationship(self, relationship_name, node_id_from=None, node_id_to=None):
        statement = ""
        statement_return = ''
        if node_id_from is not None:
            statement = "match (f)-[:{}]->(t) where id(f)={} return ".format(relationship_name, node_id_from)
            statement_return = "id(t)"
        elif node_id_to is not None:
            statement = "match (f)-[:{}]->(t) where id(t)={} return ".format(relationship_name, node_id_to)
            statement_return = "id(f)"
        statement += statement_return
        with self._driver.session() as session:
            result = session.run(statement)
        for record in result:
            yield record[statement_return]

    # 删除节点及其边关系
    def delete_node(self, node_id):
        statement = "match (n:{}) where id(n)={} detach delete n".format(self._label, node_id)
        with self._driver.session() as session:
            session.run(statement)

    # 节点排序输出id
    def get_node_order(self, order_statement):
        statement = "match (n:{}) return id(n) order by ".format(self._label) + order_statement
        statement_return = "id(n)"
        with self._driver.session() as session:
            result = session.run(statement)
        for record in result:
            yield record[statement_return]

    # 节点逆序排序输出id
    def get_node_order_desc(self,order_statement):
        statement = "match (n:{}) return id(n) order by ".format(self._label) + order_statement +" desc"
        statement_return = "id(n)"
        with self._driver.session() as session:
            result = session.run(statement)
        for record in result:
            yield record[statement_return]



    # 清空标签下所有节点
    def delete_all(self):
        statement = "match (n:{}) detach delete n".format(self._label)
        with self._driver.session() as session:
            session.run(statement)

    # 取节点数量
    def get_node_count(self):
        statement = "match (n:{}) return ".format(self._label)
        statement_return = "count(n)"
        with self._driver.session() as session:
            result = session.run(statement + statement_return)
        return result.peek()[statement_return]

    # 预留语句执行接口
    def run_statement(self, statement, statement_return):
        with self._driver.session() as session:
            result = session.run(statement)
        for record in result:
            yield record[statement_return]

    def run_statement_without_return(self,statement):
        with self._driver.session() as session:
             session.run(statement)


    # 字典转字符串
    @staticmethod
    def dict2str(d):
        for k, v in d.items():
            if type(v) == str:
                d[k] = "\"" + v + "\""
            elif type(v) == set:
                v = list(v)
            if type(v) == list:
                Neo4jDriverHelper.list2str(v)
                d[k] = v
        return str(d).replace('\'', '')

    # 列表转字符串
    @staticmethod
    def list2str(l):
        for i, v in enumerate(l):
            if type(v) == str:
                l[i] = "\"" + v + "\""
