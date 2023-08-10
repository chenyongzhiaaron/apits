"""
@author: kira
@contact: 262667641@qq.com
@file: generate_tree.py
@time: 2023/7/21 17:44
@desc: 目录树生成器
"""

import os


def generate_directory_tree(directory, file, indent=''):
    items = os.listdir(directory)
    folders = []
    files = []
    
    # 排除的文件后缀名、文件夹名称和隐藏文件
    exclude_extensions = ('.png', '.gif', '.jmx', '.logger', 'pyc')
    exclude_folders = ('__pycache__')
    
    for item in items:
        item_path = os.path.join(directory, item)
        
        if item in exclude_folders:
            continue
        
        if any(item.endswith(ext) for ext in exclude_extensions):
            continue
        
        if item.startswith('.'):
            continue
        
        if os.path.isdir(item_path):
            folders.append(item)
        else:
            files.append(item)
    
    # 按首字母排序文件夹（不区分大小写）
    folders.sort(key=lambda x: x.lower())
    
    for folder in folders:
        folder_path = os.path.join(directory, folder)
        file.write(f"{indent}└── {folder}/\n")
        generate_directory_tree(folder_path, file, indent + '    ')
    
    # 按首字母排序文件（不区分大小写）
    files.sort(key=lambda x: x.lower())
    
    for file_name in files:
        file.write(f"{indent}└── {file_name}\n")


root_directory = '.'  # 当前目录

output_file = 'directory_tree.txt'

with open(output_file, 'w') as file:
    file.write(root_directory + '\n')
    generate_directory_tree(root_directory, file)

print("目录树已保存到文件：", output_file)
