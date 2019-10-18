import os

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMenu, QAction

from gui.dialog.AddFileDialog import AddFileDialog
from model.FileModel import FileModel
from util.FileManager import FileManager


class FileEditMenu(QMenu):
    def __init__(self, index: QModelIndex):
        super(FileEditMenu, self).__init__()
        self._index = index

        self.act_open_file = QAction('打开文件')
        self.addAction(self.act_open_file)

        self.act_del_file = QAction('删除文件')
        self.addAction(self.act_del_file)

        self.act_edit_label = QAction('编辑标签')
        self.addAction(self.act_edit_label)

        self.triggered[QAction].connect(self.process_trigger)

    def process_trigger(self, act):
        if act == self.act_open_file:
            abs_path = FileManager().get_abs_path(self._index.data())
            os.system("\"{}\"".format(abs_path))
        elif act == self.act_del_file:
            FileManager().delete_file(self._index)
        elif act == self.act_edit_label:
            abs_path = FileManager().get_abs_path(self._index.data())
            file_model = FileModel()
            file_model.abs_path = abs_path
            AddFileDialog(file_model=file_model, index=self._index).exec_()
