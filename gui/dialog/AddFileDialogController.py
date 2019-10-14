from PyQt5.QtWidgets import QInputDialog, QDialog

from model.FileModel import FileModel
from util.SingletonFileLabelManager import SingletonFileLabelManager
from util.SingletonFileManager import SingletonFileManager


class AddFileDialogController:
    def __init__(self, dialog):
        self._dialog:QDialog = dialog

    def on_btn_clicked(self):
        sender = self._dialog.sender()
        if sender == self._dialog.btn_addselect:
            file_model:FileModel= self._dialog.file_model
            # 判断是否需要删除原文件
            if self._dialog.index:
                SingletonFileManager.instance().delete_file(self._dialog.index)
            # 文件模型中填充标签
            for index in self._dialog.lv_label.selectedIndexes():
                data = index.data()
                file_model.add_file_label(data)
            # 写到文件配置项
            if not SingletonFileManager.instance().add_file(self._dialog.file_model):
                print('文件{}已添加'.format(file_model.file_name))
                return
            #关闭弹窗
            self._dialog.close()
        elif sender == self._dialog.btn_newlabel:
            new_label, ok = QInputDialog.getText(None, "新增标签", "请输入新标签名：")
            if ok:
                if SingletonFileLabelManager.instance().add_label(new_label):
                    print('添加标签成功')

        elif sender == self._dialog.btn_removelabel:
            SingletonFileLabelManager.instance().remove_labels(self._dialog.lv_label.selectedIndexes())

    def remove_attribute(self, attribute: str):
        lattice_model = self._lattice_model
        # 已访问过的节点
        visit: List[int] = list()
        # 判断该节点是否已判断过
        vs: Set[int] = set()
        # 该节点为更新或删除节点
        cs: Set[int] = set()
        # 保存待处理的删除和更新的节点
        all_concepts: List[int] = list()
        for concept_id in lattice_model.get_node_id_order_by_intents_length():
            all_concepts.append(concept_id)
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
                    inf = lattice_model.get_node_base_on_category(1)
                    if concept.id == inf.id:
                        # 则其父节点充当其成为新的inf节点
                        lattice_model.set_sup_or_inf_node(concept_parent.id, 1)

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