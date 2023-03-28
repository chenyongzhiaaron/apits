from jsonpath import jsonpath

from common.base_datas import BaseDates
from common.files_tools.do_excel import DoExcel
from common.tools.logger import MyLog
from common.tools.req import req


@MyLog().decorator_log("登录")
def login(host, account, password):
    url = "/login"
    data = {"account": account, "password": password}
    headers = {"Content-Type": "application/json"}
    try:
        res = req(host, 'POST', url, data=data, headers=headers).json()
        MyLog().my_log(f"======================== 登录成功:{res} ========================", "info")
        token = res.get("token")
    except Exception as e:
        MyLog().my_log(f"======================== 登录失败： {e} ========================", "error")
    else:
        headers_ = {**headers, **{"token": token}}
        return headers_


if __name__ == '__main__':
    init_data = DoExcel(BaseDates.test_api).get_excel_init()
    print("init_data------》", init_data)
    host = init_data.get('host')
    url_ = init_data.get("url_")
    account = eval(init_data.get("constant")).get('{{account}}')
    passwd = eval(init_data.get("constant")).get('{{passwd}}')
    headers = login(host + url_, account, passwd)
    print(headers)
