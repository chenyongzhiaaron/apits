import importlib.util
import os

from common.utils.mylogger import MyLogger

log = MyLogger()


def load_script(script_path):
    """
    加载脚本文件并返回模块对象

    Args:
        script_path (str): 脚本文件的路径

    Returns:
        module: 脚本文件对应的模块对象
    """
    try:
        spec = importlib.util.spec_from_file_location(os.path.basename(script_path), script_path)
        script_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script_module)
        return script_module
    except FileNotFoundError:
        log.info(f"{script_path}: 脚本文件不存在")


def load_and_execute_script(script_directory, script_name, method_name, request):
    """
    加载并执行脚本文件中的指定方法

    Args:
        request: 请求数据
        script_directory (str): 脚本文件所在的目录
        script_name (str): 脚本文件的名称
        method_name (str): 要执行的方法的名称
    """
    script_path = os.path.join(script_directory, script_name)
    script = load_script(script_path)
    log.info(f"------开始加载脚本------{script_name}")
    if hasattr(script, method_name):
        method = getattr(script, method_name)
        return method(request)


if __name__ == '__main__':
    from common.config import Config

    SCRIPTS_DIR = Config.SCRIPTS_DIR
    load_and_execute_script(SCRIPTS_DIR, 'request_script_sheetname_id.py', 'setup', {"y": "z"})
