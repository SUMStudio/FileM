import sys

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QDialog, QApplication
from gui.dialog.AddFileDialogController import AddFileDialogController
from gui.dialog.AddFileDialog_ui import Ui_AddFileDialog
from model.FileModel import FileModel
from util.SingletonFileLabelManager import SingletonFileLabelManager


class AddFileDialog(QDialog, Ui_AddFileDialog):
    def __init__(self, file_model: FileModel, index: QModelIndex = None):
        super(AddFileDialog, self).__init__()
        self.setupUi(self)
        # 初始化文件模型
        self._file_model = file_model
        self.setWindowTitle("{}-新增标签".format(self._file_model.file_name))
        # 如果窗口来源于文件标签编辑，则Index不为空
        self._index = index
        # 初始化控制器
        self._controller = AddFileDialogController(self)
        self.btn_addselect.clicked.connect(self._controller.on_btn_clicked)
        self.btn_newlabel.clicked.connect(self._controller.on_btn_clicked)
        self.btn_removelabel.clicked.connect(self._controller.on_btn_clicked)
        # 绑定数据源
        self.lv_label.setModel(SingletonFileLabelManager.instance().label_list_model)

    @property
    def file_model(self):
        return self._file_model

    @property
    def index(self):
        return self._index

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AddFileDialog()
    dialog.show()
    sys.exit(app.exec_())
