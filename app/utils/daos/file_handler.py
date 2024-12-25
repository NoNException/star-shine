import pandas as pd
from pandas import DataFrame


# 读取上传的 Excel 文件
def read_uploaded_file(uploaded_file, date_cols=[]) -> DataFrame:
    data = pd.read_excel(uploaded_file)
    for col in date_cols:
        data[col] = pd.to_datetime(data[col], origin="1899-12-30", unit="D").dt.date
    return data
