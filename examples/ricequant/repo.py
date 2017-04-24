import tushare as ts

import shipane_sdk


# 注意：需将回测调成分钟级别
# 注意：用于回测没有意义，需挂到“我的交易”

def initialize(context):
    # 每天的收盘前5分钟进行逆回购。参数设置见：https://www.ricequant.com/api/python/chn#scheduler
    scheduler.run_daily(repo, time_rule=market_close(minute=5))


def process_initialize(context):
    # 创建 JoinQuantExecutor 对象
    # 可选参数包括：host, port, key, client, timeout 等
    # 请将下面的 IP 替换为实际 IP
    g.__executor = shipane_sdk.RiceQuantExecutor(
        host='xxx.xxx.xxx.xxx',
        port=8888,
        key='',
        client=''
    )


def repo(context):
    if context.run_info.run_type == RUN_TYPE.PAPER_TRADING:
        security = '131810'
        quote_df = ts.get_realtime_quotes(security)
        order = {
            'action': 'SELL',
            'symbol': security,
            'type': 'LIMIT',
            'price': float(quote_df['bid'][0]),
            'amountProportion': 'ALL'
        }
        g.__executor.client.execute(**order)
    else:
        log.info('回测中不进行逆回购')
