import copy
import json
import os
import time
import unittest
from concurrent.futures.thread import ThreadPoolExecutor
from json import JSONDecodeError

from jinja2 import Environment, FileSystemLoader

from common.notice.dingding import DingTalk
from common.notice.email_client import SendEmail
from common.notice.weChat import WeChat
from ..core.testResult import ReRunResult

Load = unittest.defaultTestLoader


class TestRunner:

    def __init__(self, suite: unittest.TestSuite,
                 filename="report.html",
                 report_dir="./reports",
                 title='接口测试报告',
                 tester='测试人员',
                 desc="接口自动化测试报告",
                 templates=2
                 ):
        """
        测试运行器，用于执行测试套件并生成测试报告
        :param suite: 测试套件
        :param filename: 报告文件名
        :param report_dir: 报告保存路径
        :param title: 报告标题
        :param tester: 测试人员
        :param desc: 报告描述
         :param templates: 报告模板选择
        """
        # super().__init__()
        if not isinstance(suite, unittest.TestSuite):
            raise TypeError("suite 参数不是一个测试套件")
        if not isinstance(filename, str):
            raise TypeError("filename 不是字符串类型")
        if not filename.endswith(".html"):
            filename = filename + ".html"
        self.suite = suite
        self.filename = filename
        self.title = title
        self.tester = tester
        self.desc = desc
        self.templates = templates
        self.report_dir = report_dir
        self.result = []
        self.starttime = time.time()
        self.res = None
        self.env = None
        self.template_path = os.path.join(os.path.dirname(__file__), '../../templates')
        self.env = Environment(loader=FileSystemLoader(self.template_path))

    def __classification_suite(self):
        """将测试套件按类别划分"""
        suites_list = []

        def find_test_cases(suite):
            for item in suite:
                if isinstance(item, unittest.TestCase):
                    suites_list.append(suite)
                    break
                else:
                    find_test_cases(item)

        find_test_cases(copy.deepcopy(self.suite))
        return suites_list

    def __get_reports(self):
        """生成测试报告"""
        print("所有用例执行完毕，正在生成测试报告中......")
        test_result = self.__calculate_test_result()
        test_result['runtime'] = '{:.2f} S'.format(time.time() - self.starttime)
        test_result["begin_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.starttime))
        test_result["title"] = self.title
        test_result["tester"] = self.tester
        test_result['desc'] = self.desc
        test_result['pass_rate'] = int(test_result['success'] / test_result['all'] * 100) if test_result['all'] else 0

        # 判断是否要生产测试报告
        os.makedirs(self.report_dir, exist_ok=True)

        # 获取历史执行数据
        test_result['history'] = self.__handle_history_data(test_result)

        self.template_file = self.__get_template_file()

        report_content = self.__generating_templates_and_report_content(self.template_file, test_result)
        # 写入报告文件
        self.file_path = os.path.join(self.report_dir, self.filename)
        with open(self.file_path, 'wb') as f:
            f.write(report_content.encode('utf8'))
        self.test_result = test_result
        print(f"测试报告已经生成，报告路径为:{self.file_path}")
        return test_result

    def __calculate_test_result(self):
        """计算结果"""
        test_result = {"success": 0, "all": 0, "fail": 0, "skip": 0, "error": 0, "results": [], "testClass": []}
        for report_content in self.result:
            for item in test_result:
                test_result[item] += report_content.fields[item]
        return test_result

    def __get_template_file(self):
        """获取模板文件"""
        template_file_mapping = {
            2: "templates2.html",
            3: "templates3.html"
        }

        return template_file_mapping.get(self.templates, "templates.html")

    def __generating_templates_and_report_content(self, template_file, test_result):
        """渲染模板并生成报告内容"""
        return self.env.get_template(template_file).render(test_result)

    def __handle_history_data(self, test_result):
        """
        处理历史数据
        :return:
        """
        try:
            with open(os.path.join(self.report_dir, 'history.json'), 'r', encoding='utf-8') as f:
                history = json.load(f)
        except FileNotFoundError as e:
            history = []
        except JSONDecodeError as e:
            history = []
        history.append({'success': test_result['success'],
                        'all': test_result['all'],
                        'fail': test_result['fail'],
                        'skip': test_result['skip'],
                        'error': test_result['error'],
                        'runtime': test_result['runtime'],
                        'begin_time': test_result['begin_time'],
                        'pass_rate': test_result['pass_rate'],
                        })

        with open(os.path.join(self.report_dir, 'history.json'), 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=True)
        return history

    def run(self, thread_count=1, count=0, interval=2):
        """
        The entrance to running tests
        Note: if multiple test classes share a global variable, errors may occur due to resource competition
        :param thread_count:Number of threads. default 1
        :param count: Rerun times,  default 0
        :param interval: Rerun interval, default 2
        :return: Test run results
        """
        suites = self.__classification_suite()

        if thread_count > 1:
            with ThreadPoolExecutor(max_workers=thread_count) as ts:
                for i in suites:
                    self.res = ReRunResult(count=count, interval=interval)
                    self.result.append(self.res)
                    ts.submit(i.run, result=self.res).add_done_callback(self.res.stopTestRun)
        else:
            self.res = ReRunResult(count=count, interval=interval)
            self.result.append(self.res)
            self.suite.run(self.res)
            self.res.stopTestRun()
        result = self.__get_reports()
        return result

    def rerun_run(self, count=0, interval=2):
        """
        重新运行测试用例，包括失败和错误的用例
        :param count: 重新运行次数，默认为0
        :param interval: 重新运行间隔，默认为2秒
        :return: 重新运行间隔，默认为2秒
        """
        self.res = ReRunResult(count=count, interval=interval)
        self.result.append(self.res)
        test_case_suites = self.__classification_suite()
        for test_case_suite in test_case_suites:
            test_case_suite.run(self.res)
        self.res.stopTestRun()
        result = self.__get_reports()
        return result

    def get_except_info(self):
        """Get error reporting information for error cases and failure cases"""
        except_info = []
        num = 0
        for i in self.result:
            for texts in i.failures:
                t, content = texts
                num += 1
                except_info.append("*{}、用例【{}】执行失败*，\n失败信息如下：".format(num, t._testMethodDoc))
                except_info.append(content)
            for texts in i.errors:
                num += 1
                t, content = texts
                except_info.append("*{}、用例【{}】执行错误*，\n错误信息如下：".format(num, t._testMethodDoc))
                except_info.append(content)
        except_str = "\n".join(except_info)
        return except_str

    def get_failed_test_cases(self):
        """get error or failed testcase info"""
        failed_test_cases = []
        for res in self.result:
            for failure in res.failures:
                failed_test_cases.append(failure[0])
            for error in res.errors:
                failed_test_cases.append(error[0])
            return failed_test_cases

    def email_notice(self):
        """
        发送邮件通知
        """
        email_content = {"file": [os.path.abspath(self.file_path)],
                         "content": self.__generating_templates_and_report_content("templates03.html", self.test_result)
                         }
        sm = SendEmail()
        file_path = email_content["file"]
        content = email_content["content"]
        sm.send_mail(content=content, file_path=file_path)

    def dingtalk_notice(self):
        """
        发送钉钉机器人通知
        """

        notice_content = self.__generating_templates_and_report_content('dingtalk.md', self.test_result)
        except_info = self.get_except_info()
        ding = DingTalk(self.title, notice_content, except_info)
        ding.send_info()

    def weixin_notice(self):
        """
        推送企业微信机器人
        """
        notice_content = self.__generating_templates_and_report_content('weChat.md', self.test_result)
        wx = WeChat(notice_content)
        wx.send_main()
