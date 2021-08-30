# 导入 efinance 库
import efinance as ef
# 股票代码
stock_code = '600519'
# 开始日期
beg = '20210101'
# 结束日期
end = '20210808'
# 获取股票日 K 数据
df = ef.stock.get_quote_history(stock_code, beg=beg, end=end)
print(df)


import efinance as ef
# 股票代码
stock_code = '600519'
# 获取个股十大流通股东信息, top = 4 表示最近的 4 次公开信息
df = ef.stock.get_top10_stock_holder_info(stock_code,top = 4)
print(df)