"""
程序异常处理

"""
from traceback import format_exception
import sys
from PyQt5.QtWidgets import QMessageBox


class GlobalExceptionHandEr:
    def new_except_hook(self, etype, evalue, tb):
        print(''.join(format_exception(etype, evalue, tb)))
        QMessageBox.information(None, str('error'), ''.join(format_exception(etype, evalue, tb)))
        sys.exit()  # 异常退出
    
    # 注册全局异常处理类
    def patch_except_hook(self):
        sys.excepthook = self.new_except_hook
