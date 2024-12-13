import baostock as bs
import pandas as pd
import datetime
import os
import time
import random

def baostock_login():
    max_tries = 5
    for i in range(max_tries):
        lg = bs.login()
        if lg.error_code == '0':
            return True
        else:
            print(f"登录失败，尝试重新登录 ({i+1}/{max_tries})")
            time.sleep(5)
    return False

def baostock_logout():
    bs.logout()

def get_gem_stocks():
    if not baostock_login():
        print("无法登录 baostock")
        return []

    rs = bs.query_stock_basic()
    stock_list = []
    while (rs.error_code == '0') & rs.next():
        stock = rs.get_row_data()
        if stock[0].startswith('sz.300'):
            stock_list.append(stock)
    
    baostock_logout()
    return stock_list

def get_stock_data(stock_code, days=30):
    if not baostock_login():
        print(f"无法获取股票 {stock_code} 的数据")
        return None

    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.datetime.now() - datetime.timedelta(days=days*2)).strftime('%Y-%m-%d')
    
    max_tries = 3
    for _ in range(max_tries):
        try:
            rs = bs.query_history_k_data_plus(stock_code,
                "date,code,open,high,low,close,volume,amount,turn,pctChg",
                start_date=start_date, end_date=end_date,
                frequency="d", adjustflag="3")
            
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if data_list:
                df = pd.DataFrame(data_list, columns=rs.fields)
                for field in ['open', 'high', 'low', 'close', 'volume', 'amount', 'turn', 'pctChg']:
                    df[field] = pd.to_numeric(df[field], errors='coerce')
                baostock_logout()
                return df.tail(30)
            else:
                print(f"未能获取到 {stock_code} 的数据，尝试重新获取")
                time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"获取 {stock_code} 数据时发生错误: {str(e)}，尝试重新获取")
            time.sleep(random.uniform(1, 3))
    
    baostock_logout()
    return None

def get_market_cap(stock_code):
    if not baostock_login():
        print(f"无法登录 baostock 以获取股票 {stock_code} 的市值数据")
        return None

    try:
        # 获取最新的收盘价
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        rs_price = bs.query_history_k_data_plus(stock_code,
            "date,close",
            start_date=start_date, end_date=end_date,
            frequency="d", adjustflag="3")
        
        if rs_price.error_code != '0':
            print(f"查询股票 {stock_code} 的价格数据失败: {rs_price.error_msg}")
            return None

        price_data = []
        while (rs_price.error_code == '0') & rs_price.next():
            price_data.append(rs_price.get_row_data())

        if not price_data:
            print(f"未找到股票 {stock_code} 的最新价格数据")
            return None

        latest_price = float(price_data[-1][1])

        # 获取股票基本信息（包括总股本）
        rs_basic = bs.query_stock_basic(code=stock_code)
        if rs_basic.error_code != '0':
            print(f"查询股票 {stock_code} 的基本信息失败: {rs_basic.error_msg}")
            return None

        if rs_basic.next():
            stock_info = rs_basic.get_row_data()
            if len(stock_info) > 9:  # 确保有足够的字段
                total_share = float(stock_info[9]) if stock_info[9] else None
                if total_share is not None:
                    market_cap = latest_price * total_share / 100000000  # 转换为亿元
                    print(f"股票 {stock_code} 的估算市值为 {market_cap:.2f} 亿元")
                    return market_cap
                else:
                    print(f"股票 {stock_code} 的总股本数据不可用")
            else:
                print(f"股票 {stock_code} 的基本信息不完整")
        else:
            print(f"未找到股票 {stock_code} 的基本信息")

    except Exception as e:
        print(f"获取股票 {stock_code} 的市值数据时发生异常: {str(e)}")
    finally:
        baostock_logout()

    return None

    if not baostock_login():
        print(f"无法登录 baostock 以获取股票 {stock_code} 的市值数据")
        return None

    try:
        # 获取最新的日K线数据
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        rs = bs.query_history_k_data_plus(stock_code,
            "date,code,close,totalShare",
            start_date=start_date, end_date=end_date,
            frequency="d", adjustflag="3")
        
        if rs.error_code != '0':
            print(f"查询股票 {stock_code} 的K线数据失败: {rs.error_msg}")
            return None

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())

        if data_list:
            latest_data = data_list[-1]
            close_price = float(latest_data[2])
            total_share = float(latest_data[3])
            market_cap = close_price * total_share / 100000000  # 转换为亿元
            print(f"股票 {stock_code} 的估算市值为 {market_cap:.2f} 亿元")
            return market_cap
        else:
            print(f"未找到股票 {stock_code} 的最新交易数据")

    except Exception as e:
        print(f"获取股票 {stock_code} 的市值数据时发生异常: {str(e)}")
    finally:
        baostock_logout()

    return None

    if not baostock_login():
        print(f"无法获取股票 {stock_code} 的市值数据")
        return None

    try:
        rs = bs.query_stock_basic(code=stock_code)
        if rs.error_code == '0' and rs.next():
            stock_info = rs.get_row_data()
            if len(stock_info) > 7 and stock_info[7]:
                market_cap = float(stock_info[7])
                baostock_logout()
                return market_cap
        print(f"无法获取股票 {stock_code} 的市值数据")
    except Exception as e:
        print(f"获取股票 {stock_code} 的市值数据时发生错误: {str(e)}")
    
    baostock_logout()
    return None

def check_conditions(df):
    if len(df) < 30:
        return False
    
    limit_up_days = df[df['pctChg'] >= 9.9]
    if len(limit_up_days) < 2:
        return False
    
    if df['turn'].mean() <= 5:
        return False
    
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ma30'] = df['close'].rolling(window=30).mean()
    
    latest = df.iloc[-1]
    if not (latest['ma5'] > latest['ma10'] > latest['ma20'] > latest['ma30']):
        return False
    
    return True

def main():
    gem_stocks = get_gem_stocks()
    print(f"找到 {len(gem_stocks)} 只创业板股票")
    
    filtered_stocks = []
    
    for stock in gem_stocks:
        stock_code = stock[0]
        print(f"Processing {stock_code}")
        
        try:
            time.sleep(random.uniform(0.5, 1.5))  # 添加随机延迟
            
            # market_cap = get_market_cap(stock_code)
            # if market_cap is None or market_cap > 60:
            #     continue
            
            df = get_stock_data(stock_code)
            if df is None or df.empty:
                continue
            
            if check_conditions(df):
                filtered_stocks.append({
                    'code': stock_code,
                    'name': stock[1],
                    'market_cap': market_cap,
                    'avg_turnover': df['turn'].mean(),
                    'limit_up_count': len(df[df['pctChg'] >= 9.9]),
                    'latest_close': df['close'].iloc[-1],
                    'latest_ma5': df['ma5'].iloc[-1],
                    'latest_ma10': df['ma10'].iloc[-1],
                    'latest_ma20': df['ma20'].iloc[-1],
                    'latest_ma30': df['ma30'].iloc[-1]
                })
        except Exception as e:
            print(f"处理股票 {stock_code} 时发生错误: {str(e)}")
            continue
    
    if filtered_stocks:
        result_df = pd.DataFrame(filtered_stocks)
        excel_file = 'filtered_stocks.xlsx'
        result_df.to_excel(excel_file, index=False)
        print(f"Results saved to {os.path.abspath(excel_file)}")
    else:
        print("No stocks found matching the criteria.")

if __name__ == "__main__":
    main()
