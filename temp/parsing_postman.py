import json

from common.files_tools.read_file import read_file

result = []


def parsing_postman(path):
    data = read_file(path)

    # print("元數據", data)

    def _parse_api(content):
        global result
        api = {}
        if isinstance(content, list):
            for item in content:
                api['name'] = item.get('name')
                _parse_api(content=item)
        elif isinstance(content, dict):
            if 'item' in content.keys():
                _parse_api(content=content.get('item'))
            elif 'request' in content.keys():
                api['description'] = content.get('name')
                request = content.get('request')
                if request:
                    # api请求方法
                    api['Method'] = request.get('method', 'GET').upper()
                    # print('Method----->', api['Method'])
                    header = request.get('header')
                    header = {item.get('key'): item.get('value') for item in header} if header else {}

                    auth = request.get('auth')
                    if auth:
                        auth_type = auth.get('type')
                        if auth.get(auth_type):
                            auth_value = {item.get('key'): item.get('value') for item in auth.get(auth_type) if
                                          (item and item.get('key'))}
                            header.update(auth_value)
                    # api请求头
                    api['Headers'] = json.dumps(header, ensure_ascii=False)
                    # print('Headers---->:', api['Headers'])
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
                    # print('Url---->:', api['Url'])
                    body = request.get('body')
                    if body:
                        # api接口请求参数类型
                        request_mode = body.get('mode')
                        if 'raw' == request_mode:
                            api['request_data_type'] = 'Json'
                        elif 'formdata' == request_mode:
                            api['request_data_type'] = 'Form Data'
                        # print('------------------------>Body', body)
                        # api接口请求参数
                        request_data = body.get(request_mode)
                        if request_data and 'raw' == request_mode:
                            api['Request Data'] = request_data.replace('\t', '').replace('\n', '')
                            # print('Body------>1:', api['Request Data'])
                        elif request_data and 'formdata' == request_mode:
                            if isinstance(request_data, list):
                                api['Request Data'] = json.dumps({item.get('key'): '' for item in request_data},
                                                                 ensure_ascii=False)
                            # print('Body------>2:', api['Request Data'])
                result.append(api)
    for d in data:
        _parse_api(content=data)
    return result




if __name__ == '__main__':
    pat = r'C:\Users\chenyongzhi11\Desktop\市调情报系统.postman_collection.json'
    res = parsing_postman(pat)
    print('结果：', res)
