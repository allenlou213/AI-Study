import efinance as ef
import pandas as pd
import xml.etree.ElementTree as ET

# 获取创业板股票列表
gem_stocks = ef.stock.get_realtime_quotes('创业板')

# 获取过去30个交易日的股票数据
def get_stock_data(stock_code):
    return ef.stock.get_quote_history(stock_code, klt=101, fqt=1, beg='2024-11-01', end='2024-12-12')

# 筛选符合条件的股票
def filter_stocks(stock_data):
    # 检查是否有两个涨停
    limit_up_days = stock_data[stock_data['涨跌幅'] >= 9.9]
    if len(limit_up_days) < 1:
        return False
    
    # # 检查每天的换手率是否不低于5%
    # if (stock_data['换手率'] < 5).any():
    #     return False
    
    # # 检查均线多头排列
    # stock_data['MA5'] = stock_data['收盘价'].rolling(window=5).mean()
    # stock_data['MA10'] = stock_data['收盘价'].rolling(window=10).mean()
    # stock_data['MA20'] = stock_data['收盘价'].rolling(window=20).mean()
    # if not ((stock_data['MA5'] > stock_data['MA10']) & (stock_data['MA10'] > stock_data['MA20'])).all():
    #     return False
    
    return True

# 获取符合条件的股票代码和名称
filtered_stocks = []
for index, row in gem_stocks.iterrows():
    stock_code = row['股票代码']
    stock_name = row['股票名称']
    stock_data = get_stock_data(stock_code)
    if filter_stocks(stock_data):
        filtered_stocks.append({stock_code, stock_name})

# 创建包含筛选后股票的DataFrame
filtered_df = pd.DataFrame(filtered_stocks, columns=['股票代码', '股票名称'])

# 设置Excel文件的路径
excel_filename = "filtered_stocks.xlsx"

# 尝试保存文件，并进行错误处理
try:
    # 使用 'w' 模式打开文件，这会覆盖已存在的文件
    with pd.ExcelWriter(excel_filename, mode='w') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name='筛选结果')
    print(f"筛选后的股票已保存到 {excel_filename}")
except PermissionError:
    print(f"保存到 {excel_filename} 时被拒绝访问")
    print("请确保文件未被其他程序打开，且您有写入权限。")
except Exception as e:
    print(f"保存文件时发生错误：{str(e)}")