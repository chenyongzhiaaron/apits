import warnings
from common.base_datas import BaseDates
from common.files_tools.do_excel import DoExcel
from common.tools.logger import MyLog
from common.tools.req import req
from common.dependence import Dependence


@MyLog().decorator_log("登录失败")
def login(host, username, password):
    warnings.simplefilter("ignore", ResourceWarning)
    url = "/auth/loginByNotBip"
    data = {"account": username, "password": password}
    headers = {"Content-Type": "application/json"}
    try:
        res = req(host, url, 'POST', data=data, headers=headers).json()
        MyLog().my_log(f"====登录成功====", "info")
        token = res.get("data").get("bspToken")
        current_tenant_id = res.get("data").get("currentTenantId")
        Dependence.update_dep('BSP_TOKEN', token)
        Dependence.update_dep('BSP_USER_TENANT', current_tenant_id)
        return {**headers, **{"BSP_TOKEN": token, "BSP_USER_TENANT": current_tenant_id}}
    except:
        raise


if __name__ == '__main__':
    init_data = DoExcel(BaseDates.test_api).get_excel_init()
    h = init_data.get('host')
    path = init_data.get("path")
    account = eval(init_data.get("initialize_data")).get('{{account}}')
    passwd = eval(init_data.get("initialize_data")).get('{{passwd}}')
    header = login(h + path, account, passwd)
    print(header)
