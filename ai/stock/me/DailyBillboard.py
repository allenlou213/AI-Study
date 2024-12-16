import efinance as ef
import pandas as pd
import os
from openpyxl import load_workbook
from datetime import datetime

# 获取最新一个公开的龙虎榜数据(后面还有获取指定日期区间的示例代码)
result = ef.stock.get_daily_billboard()

# 保存结果到Excel文件
result_df = pd.DataFrame(result)
file_path = 'E:/study/ai/stock/me/daily_billboard.xlsx'
sheet_name = datetime.now().strftime('%Y-%m-%d')

# 获取目录路径
directory = os.path.dirname(file_path)

# 如果目录不存在，则创建
if not os.path.exists(directory):
    os.makedirs(directory)

# 保存到Excel文件
try:
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a' if os.path.exists(file_path) else 'w', if_sheet_exists='replace') as writer:
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)
    print('数据保存成功！')
except Exception as e:
    print(f"保存文件时出错: {e}")