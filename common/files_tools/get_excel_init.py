# from common.Base_datas import BaseDates
# from common.GetParams import Params
# from common.do_excel import DoExcel


# def get_excel_init():
#     test_file = BaseDates.test_api  # 获取 excel 文件路径
#     excel_init = DoExcel(test_file).get_excel_init()  # 获取初始化数据
#     for i in excel_init:
#         if i.get("run") == "yes":
#             mysql_base = eval(excel_init["test_databases"])  # 获取初始化数据中的数据库信息
#             if excel_init.get("url_") is not None or excel_init.get("url_") != "":
#                 host = excel_init.get("host") + excel_init.get("url_")  # 获取项目的 host
#             else:
#                 host = excel_init.get("host")
#             # 初始化常量存入关联字典
#             constant = eval(excel_init["constant"])
#             correct = getattr(Params, "correlation_dict")
#             for k, v in constant.items():
#                 correct[k] = v
#                 setattr(Params, "correlation_dict", correct)
#             return host, Params.correlation_dict, mysql_base


# if __name__ == '__main__':
    # print(get_excel_init())
