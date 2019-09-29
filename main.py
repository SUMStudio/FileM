# -*- coding:utf-8 -*-
"""
调用主程序、异常处理
"""

from tkinter import messagebox

if __name__ == '__main__':
    # 防止初始化异常
    try:
        from FileM import main
        main()
    except Exception as e:
        print("系统异常", str(e))
        messagebox.showerror("系统异常", str(e))    