import pandas as pd


# 读取上传的 Excel 文件
def read_uploaded_file(uploaded_file):
    return pd.read_excel(uploaded_file)
