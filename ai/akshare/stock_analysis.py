import akshare as ak
import pandas as pd
import datetime
import time

def get_stock_list_with_retry(retries=3, delay=5):
    for i in range(retries):
        try:
            stock_list = ak.stock_zh_a_spot()
            return stock_list
        except Exception as e:
            print(f"获取股票列表失败，重试 {i+1}/{retries} 次。错误信息: {e}")
            time.sleep(delay)
    raise Exception("多次重试后仍然无法获取股票列表。")

# 获取所有中国股票的列表
stock_list = get_stock_list_with_retry()

# 获取今天的日期
today = datetime.datetime.today().strftime('%Y%m%d')

# 定义一个空的 DataFrame 来存储结果
result_df = pd.DataFrame(columns=['股票代码', '股票名称', '股票市值', '前10个交易日涨幅/跌幅', '板块'])

# 遍历每只股票
for index, row in stock_list.iterrows():
    stock_code = row['代码']
    stock_name = row['名称']
    
    # 过滤掉北京证券交易所的股票
    if stock_code.startswith('bj'):
        continue
    
    try:
        # 获取前10个交易日的历史数据
        stock_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=(datetime.datetime.today() - datetime.timedelta(days=20)).strftime('%Y%m%d'), end_date=today, adjust="qfq")
    except (KeyError, ValueError, TypeError) as e:
        print(f"无法获取股票 {stock_code} 的历史数据，跳过。错误信息: {e}")
        continue
    
    if len(stock_hist_df) < 11:
        continue
    
    # 计算涨停和跌幅
    stock_hist_df['涨停'] = stock_hist_df['收盘'] >= stock_hist_df['开盘'] * 1.1
    stock_hist_df['跌幅'] = (stock_hist_df['收盘'] - stock_hist_df['开盘']) / stock_hist_df['开盘']
    
    # 检查前10个交易日是否有至少5个涨停
    if stock_hist_df['涨停'][-11:-1].sum() >= 5:
        # 检查上个交易日是否没有涨停且没有下跌超过2%
        if not stock_hist_df['涨停'].iloc[-2] and stock_hist_df['跌幅'].iloc[-2] > -0.02:
            try:
                # 获取股票市值和板块信息
                stock_info = ak.stock_individual_info_em(symbol=stock_code)
                market_value = stock_info['总市值']
                sector = stock_info['所属板块']
            except Exception as e:
                print(f"无法获取股票 {stock_code} 的详细信息，跳过。错误信息: {e}")
                continue
            
            # 计算前10个交易日的涨幅/跌幅
            price_change = stock_hist_df['涨幅'][-11:-1].tolist()
            
            # 将结果添加到 DataFrame
            result_df = result_df.append({
                '股票代码': stock_code,
                '股票名称': stock_name,
                '股票市值': market_value,
import akshare as ak
import pandas as pd
import datetime
import time

def get_stock_list_with_retry(retries=3, delay=5):
    for i in range(retries):
        try:
            stock_list = ak.stock_zh_a_spot()
            return stock_list
        except Exception as e:
            print(f"获取股票列表失败，重试 {i+1}/{retries} 次。错误信息: {e}")
            time.sleep(delay)
    raise Exception("多次重试后仍然无法获取股票列表。")

# 获取所有中国股票的列表
stock_list = get_stock_list_with_retry()

# 获取今天的日期
today = datetime.datetime.today().strftime('%Y%m%d')

# 定义一个空的 DataFrame 来存储结果
result_df = pd.DataFrame(columns=['股票代码', '股票名称', '股票市值', '前10个交易日涨幅/跌幅', '板块'])

# 遍历每只股票
for index, row in stock_list.iterrows():
    stock_code = row['代码']
    stock_name = row['名称']
    
    # 过滤掉北京证券交易所的股票
    if stock_code.startswith('bj'):
        continue
    
    try:
        # 获取前10个交易日的历史数据
        stock_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=(datetime.datetime.today() - datetime.timedelta(days=20)).strftime('%Y%m%d'), end_date=today, adjust="qfq")
    except (KeyError, ValueError, TypeError) as e:
        print(f"无法获取股票 {stock_code} 的历史数据，跳过。错误信息: {e}")
        continue
    
    if len(stock_hist_df) < 11:
        continue
    
    # 计算涨停和跌幅
    stock_hist_df['涨停'] = stock_hist_df['收盘'] >= stock_hist_df['开盘'] * 1.1
    stock_hist_df['跌幅'] = (stock_hist_df['收盘'] - stock_hist_df['开盘']) / stock_hist_df['开盘']
    
    # 检查前10个交易日是否有至少5个涨停
    if stock_hist_df['涨停'][-11:-1].sum() >= 5:
        # 检查上个交易日是否没有涨停且没有下跌超过2%
        if not stock_hist_df['涨停'].iloc[-2] and stock_hist_df['跌幅'].iloc[-2] > -0.02:
            try:
                # 获取股票市值和板块信息
                stock_info = ak.stock_individual_info_em(symbol=stock_code)
                market_value = stock_info['总市值']
                sector = stock_info['所属板块']
            except Exception as e:
                print(f"无法获取股票 {stock_code} 的详细信息，跳过。错误信息: {e}")
                continue
            
            # 计算前10个交易日的涨幅/跌幅
            price_change = stock_hist_df['涨幅'][-11:-1].tolist()
            
            # 将结果添加到 DataFrame
            result_df = result_df.append({
                '股票代码': stock_code,
                '股票名称': stock_name,
                '股票市值': market_value,