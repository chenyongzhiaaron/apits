
"""
unittestreport基于unittest扩展了5个功能：
1、html测试报告的生成(三个风格)
2、测试用例失败重运行
3、测试报告邮件发送功能
4、数据驱动
5、多线程执行测试用例
"""

from .core.testRunner import TestRunner,Load
from common.utils.decorators import list_data,json_data,yaml_data
from common.utils.decorators import rerun,run_count
# from .core.reRun import rerun
