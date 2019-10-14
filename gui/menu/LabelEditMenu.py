from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMenu, QAction, QInputDialog

from util.SingletonFileLabelManager import SingletonFileLabelManager


class LabelEditMenu(QMenu):
    def __init__(self,index:QModelIndex):
        super(LabelEditMenu, self).__init__()
        self._index = index

        self.act_add_label = QAction('新增标签')
        self.addAction(self.act_add_label)

        self.act_remove_label = QAction('删除标签')
        self.addAction(self.act_remove_label)

        self.act_label_info = QAction('标签信息')
        self.addAction(self.act_label_info)

        self.triggered[QAction].connect(self.process_trigger)

    def process_trigger(self, act):
        if act == self.act_add_label:
            new_label, ok = QInputDialog.getText(None, "新增标签", "请输入新标签名：")
            if ok:
                if SingletonFileLabelManager.instance().add_label(new_label):
                    print('添加标签成功')
        elif act == self.act_remove_label:
            SingletonFileLabelManager.instance().remove_label(self._index)
        elif act == self.act_label_info:
            pass
