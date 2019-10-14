from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileIconProvider


class IconExtractor:
    def __init__(self, file_path: str):
        self._file_path = file_path

    def get_icon(self) -> QIcon:
        file_info = QFileInfo(self._file_path)
        icon_provider = QFileIconProvider()
        icon = icon_provider.icon(file_info)
        return icon
