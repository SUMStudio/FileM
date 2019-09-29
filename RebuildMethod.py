# from PyQt5.Qt import *
from PyQt5.QtWidgets import QListWidget


class QListWidgetRebuild(QListWidget):
    def mousePressEvent(self, evt):
        pos = evt.pos()
        item = self.itemAt(pos)
        if not item:
            self.setCurrentRow(-1)
        else:
            QListWidget.mousePressEvent(self, evt)


