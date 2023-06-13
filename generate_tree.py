import os

from treelib import Tree


def generate_directory_tree(directory, tree, parent=None, indent=''):
    items = os.listdir(directory)
    items.sort()  # 对目录列表按照字符排序

    # 排除的文件后缀名、文件夹名称和隐藏文件
    exclude_extensions = ('.png', '.gif', '.jmx', '.log', 'pyc')
    exclude_folders = ('__pycache__')

    for i, item in enumerate(items):
        item_path = os.path.join(directory, item)

        if item in exclude_folders:
            continue

        if any(item.endswith(ext) for ext in exclude_extensions):
            continue

        if item.startswith('.'):
            continue

        if os.path.isdir(item_path):
            node = tree.create_node(item, item_path, parent=parent)
            generate_directory_tree(item_path, tree, parent=node.identifier, indent=indent + '  ')
        else:
            tree.create_node(item, item_path, parent=parent)


def save_directory_tree(tree, node, file, indent=''):
    if node is None:
        return

    file.write(f"{indent}{node}\n")
    for child_id in tree.children(node):
        child_node = tree.get_node(child_id)
        save_directory_tree(tree, child_node.identifier, file, indent=indent + '  ')


root_directory = '.'  # 当前目录

directory_tree = Tree()
root_node = directory_tree.create_node(root_directory, root_directory)

generate_directory_tree(root_directory, directory_tree, parent=root_node.identifier)

# 保存目录树到文件
with open('directory_tree.txt', 'w') as file:
    save_directory_tree(directory_tree, root_node.identifier, file)

print("目录树已保存到文件：directory_tree.txt")
