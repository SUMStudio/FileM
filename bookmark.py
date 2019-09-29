"""
标签管理
待完善
"""
# import json
from fmconfig import cf


def get_bookmark():
    if cf.has_option("global", "bookmark"):     # 检查global是否存在,且是否包含bookmark项
        string_bookmark = cf.get("global", "bookmark")      # 获取bookmark下的值，可使用字典
        # return set(json.loads(string_bookmark))
        return set(eval(string_bookmark))   # 获取bookmark列表
