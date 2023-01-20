
# 我觉得这个文件就这样子结束了。
# 每个文件都import一下即可。
# 当然可能会有更好的办法？菜鸡啥都不懂。

_global_dict = {}

def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        print("Err:Not Found")
        return None
    except:
        print("Err:Unknown error.")
        return None
