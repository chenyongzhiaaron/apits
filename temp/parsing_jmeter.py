#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: parsing_jmeter.py
@time: 2023/5/18 8:51
@desc:
"""
import xml.etree.ElementTree as ET

import xml.etree.ElementTree as ET


def parse_jmeter_test_case(file_path):
    test_cases = []

    # 解析 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 提取线程组名称
    thread_group_element = root.find("./hashTree/TestPlan")
    thread_group_name = thread_group_element.get("testname")

    # 遍历所有的 HTTPSamplerProxy 元素
    for index, sampler in enumerate(root.iter('HTTPSamplerProxy')):
        test_case = {}
        test_case['id'] = index + 1
        test_case['name'] = thread_group_name

        # 提取测试用例描述
        sample_name = sampler.attrib.get('testname')
        test_case['description'] = sample_name

        # 提取 URL
        ip = sampler.find("./stringProp[@name='HTTPSampler.domain']").text
        port = sampler.find("./stringProp[@name='HTTPSampler.port']").text
        path = sampler.find("./stringProp[@name='HTTPSampler.path']").text
        test_case['url'] = ip + port + path

        # 提取 Method
        test_case['method'] = sampler.find("./stringProp[@name='HTTPSampler.method']").text

        # 提取 Headers
        headers = {}
        default_headers_element = root.find("./hashTree/HeaderManager/collectionProp[@name='HeaderManager.headers']")
        sampler_headers_element = sampler.find("./hashTree/HeaderManager/collectionProp[@name='HeaderManager.headers']")
        if default_headers_element is not None:
            for header_element in default_headers_element.findall("./elementProp[@elementType='Header']"):
                name = header_element.find("./stringProp[@name='Header.name']").text
                value = header_element.find("./stringProp[@name='Header.value']").text
                headers[name] = value
        if sampler_headers_element is not None:
            for header_element in sampler_headers_element.findall("./elementProp[@elementType='Header']"):
                name = header_element.find("./stringProp[@name='Header.name']").text
                value = header_element.find("./stringProp[@name='Header.value']").text
                headers[name] = value
        test_case['headers'] = headers

        # 提取 Body
        body_element = sampler.find("./elementProp[@name='HTTPsampler.Arguments']")
        if body_element is not None:
            body = body_element.find("./collectionProp/elementProp[@elementType='HTTPArgument']").find(
                "./stringProp[@name='Argument.value']").text
            test_case['body'] = body

        # 提取 Params
        params = {}
        param_elements = sampler.findall(
            "./elementProp[@name='HTTPsampler.Arguments']/collectionProp[@name='Arguments.arguments']/elementProp[@elementType='HTTPArgument']")
        for param_element in param_elements:
            name = param_element.attrib.get('name')
            value = param_element.find("./stringProp[@name='Argument.value']").text
            params[name] = value
        test_case['params'] = params

        test_cases.append(test_case)

    return test_cases


if __name__ == '__main__':
    # 调用函数进行解析
    file_path = 'jobRequire.jmx'  # 替换为你的 JMeter 导出文件的路径
    parsed_test_cases = parse_jmeter_test_case(file_path)
    print("====", parsed_test_cases)
    # 打印解析结果
    # for test_case in parsed_test_cases:
    #     print('URL:', test_case['url'])
    #     print('Method:', test_case['method'])
    #     print('Headers:', test_case['headers'])
    #     print('Body:', test_case.get('body'))
    #     print('Params:', test_case['params'])
    #     print('---')
