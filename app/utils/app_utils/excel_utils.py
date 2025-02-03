from openpyxl.workbook import Workbook

from app.utils.app_utils.common_utils import app_log


@app_log
def write_to_excel(file_name, data_list, headers=None):
    """
    将对象列表写入 Excel 文件

    参数:
    - file_name (str): 要保存的 Excel 文件名（例如 'output.xlsx'）
    - data_list (list of list/tuple): 要写入的数据，每个子列表/元组表示一行
    - headers (list): 可选，表头数据（如列名），默认为 None

    返回:
    - None
    """
    # 创建工作簿和工作表
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # 写入表头（如果提供）
    if headers:
        ws.append(headers)
    sheet = wb.active

    if data_list:
        headers = list(vars(data_list[0]).keys())
        sheet.append(headers)
        # 遍历对象列表
    for obj in data_list:
        # 获取对象的属性值
        values = list(vars(obj).values())
        # 将属性值作为一行数据写入工作表
        sheet.append(values)
    wb.save(file_name)
    print(f"Data written to {file_name}")
