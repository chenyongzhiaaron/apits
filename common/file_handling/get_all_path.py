# -*- coding: utf-8 -*-
import os


def get_all_path(open_file_path):
    """
    递归获取目录下所有的文件的路径
    Args:
        open_file_path:

    Returns:

    """
    rootdir = open_file_path
    path_list = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    if "__pycache__" in list:
        list.remove("__pycache__")
    for i in range(0, len(list)):
        com_path = os.path.join(rootdir, list[i])
        if os.path.isfile(com_path):
            path_list.append(com_path)
        if os.path.isdir(com_path):
            print("--")
            path_list.extend(get_all_path(com_path))
    return path_list


if __name__ == "__main__":
    ret = get_all_path(r'D:\apk_api\api-test-project\OutPut\Reports')
    print(ret)
