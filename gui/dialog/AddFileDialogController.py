from PyQt5.QtWidgets import QInputDialog, QDialog

from model.FileModel import FileModel
from util.FileLabelManager import FileLabelManager
from util.FileManager import FileManager



class AddFileDialogController:
    def __init__(self, dialog):
        self._dialog:QDialog = dialog

    def on_btn_clicked(self):
        sender = self._dialog.sender()
        if sender == self._dialog.btn_addselect:
            file_model:FileModel= self._dialog.file_model
            # 判断是否需要删除原文件
            if self._dialog.index:
                FileManager().delete_file(self._dialog.index)
            # 文件模型中填充标签
            for index in self._dialog.lv_label.selectedIndexes():
                data = index.data()
                file_model.add_file_label(data)
            # 写到文件配置项
            if not FileManager().add_file(self._dialog.file_model):
                print('文件{}已添加'.format(file_model.file_name))
                return
            #关闭弹窗
            self._dialog.close()
        elif sender == self._dialog.btn_newlabel:
            new_label, ok = QInputDialog.getText(None, "新增标签", "请输入新标签名：")
            if ok:
                if FileLabelManager().add_label(new_label):
                    print('添加标签成功')

        elif sender == self._dialog.btn_removelabel:
            FileLabelManager().remove_labels(self._dialog.lv_label.selectedIndexes())
