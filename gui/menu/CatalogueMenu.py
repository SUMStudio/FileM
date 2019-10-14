from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QAction, QMenu, QTreeView

from util.GlobalVarManager import GlobalVarManager
from util.SingletonCatalogueManager import SingletonCatalogueManager


class CatalogueMenu(QMenu):
    def __init__(self, tv_catalogue: QTreeView,index: QModelIndex = None):
        super(CatalogueMenu, self).__init__()
        self._index = index
        self._tv_catalogue = tv_catalogue

        self.act_refresh = QAction('刷新目录')
        self.addAction(self.act_refresh)

        self.act_expand_all = QAction('展开所有节点')
        self.addAction(self.act_expand_all)

        self.act_collapse_all = QAction('收起所有节点')
        self.addAction(self.act_collapse_all)

        self.triggered[QAction].connect(self.process_trigger)

    def process_trigger(self, act):
        if act == self.act_refresh:
            # 图转树
            GlobalVarManager.lattice_editor.translate_lattice_to_tree()
            # 从数据库中加载目录树
            SingletonCatalogueManager.instance().init_catalogue()
            # 初始化目录参数
            self._tv_catalogue.setColumnWidth(0, 300)
        elif act == self.act_expand_all:
            self._tv_catalogue.expandAll()
        elif act == self.act_collapse_all:
            self._tv_catalogue.collapseAll()
