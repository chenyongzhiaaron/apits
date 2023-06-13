import json

from common.config import BaseDates
from common.file_handling.read_file import read_file

id_count = 0
result = []


def parsing_postman(path):
    """
    解析postman到处的json文件
    Args:
        path:

    Returns:

    """
    data = read_file(path)

    def _parse_api(content):
        global result
        global id_count
        api = {}
        if isinstance(content, list):
            for item in content:
                _parse_api(content=item)
        elif isinstance(content, dict):
            if 'item' in content.keys():
                _parse_api(content=content.get('item'))
            elif 'request' in content.keys():
                id_count += 1
                api['id'] = id_count
                api['name'] = 'postman'
                api['description'] = content.get('name')
                request = content.get('request')
                api['Run'] = 'yes'
                if request:
                    # api请求方法
                    api['Method'] = request.get('method', 'GET').upper()
                    header = request.get('header')
                    header = {item.get('key'): item.get('value') for item in header} if header else {}
                    auth = request.get('auth')
                    if auth:
                        auth_type = auth.get('type')
                        if auth.get(auth_type):
                            auth_value = {item.get('key'): item.get('value') for item in auth.get(auth_type) if
                                          (item and item.get('key'))}
                            header.update(auth_value)
                    # api 请求地址
                    url = request.get('url')
                    if url:
                        api['Url'] = url.get('raw')
                    # if url and url.get('path'):
                    #     # api请求URL
                    #     api['Url'] = r'/'.join(url.get('path'))
                    #
                    # if url and url.get('query'):
                    #     # api查询参数
                    #     api['Request Data'] = '&'.join(
                    #         [item.get('key') + '=' + (item.get('value') or '') for item in url.get('query') if item])
                    # api请求头
                    api['Headers'] = json.dumps(header, ensure_ascii=False)
                    api['Headers是否加密'] = ''
                    api['params'] = ''
                    body = request.get('body')
                    if body:
                        # api接口请求参数类型
                        request_mode = body.get('mode')
                        if 'raw' == request_mode:
                            api['request_data_type'] = 'json'
                        elif 'formdata' == request_mode:
                            api['request_data_type'] = 'data'
                        elif 'urlencoded' == request_mode:
                            api['request_data_type'] = 'data'

                        # api接口请求参数
                        request_data = body.get(request_mode)
                        api['Request Data'] = {}
                        if request_data and 'raw' == request_mode:
                            api['Request Data'].update(
                                json.loads(request_data.replace('\t', '').replace('\n', '').replace('\r', '')))
                        elif request_data and 'formdata' == request_mode:
                            if isinstance(request_data, list):
                                for item in request_data:
                                    if item.get("type") == "text":
                                        api['Request Data'].update({item.get('key'): item.get("value", "")})
                                    elif item.get("type") == "file":
                                        api["Request Data"].update({item.get('key'): item.get("src", "")})
                                        api["request_data_type"] = "files"
                        api["Request Data"] = json.dumps(api["Request Data"], ensure_ascii=False)
                        api['请求参数是否加密'] = ''
                        api['提取请求参数'] = ''
                        api['Jsonpath'] = ''
                        api['正则表达式'] = ''
                        api['正则变量'] = ''
                        api['绝对路径表达式'] = ''
                        api['SQL'] = ''
                        api['sql变量'] = ''
                        api['预期结果'] = ''
                        api['响应结果'] = ''
                        api['断言结果'] = ''
                        api['报错日志'] = ''

                result.append(api)

    for _ in data:
        _parse_api(content=data)
    return result


if __name__ == '__main__':
    pat = r'D:\apk_api\api-test-project\temp\postman.json'
    res = parsing_postman(pat)
    # from temp.tests import DoExcel
    #
    # templates = BaseDates.templates  # 使用标准模板
    # ex = DoExcel(templates)
    # ex.do_main("postman.xlsx", *res)
