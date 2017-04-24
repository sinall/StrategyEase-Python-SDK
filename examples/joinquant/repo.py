import tushare as ts

import shipane_sdk


# 注意：需将回测调成分钟级别
# 注意：用于回测没有意义，需挂到“我的交易”

def initialize(context):
    # 每天的收盘前5分钟进行逆回购，参数设置见：https://www.joinquant.com/api#定时运行
    run_daily(repo, '14:55')


def process_initialize(context):
    # 创建 JoinQuantExecutor 对象
    # 可选参数包括：host, port, key, client, timeout 等
    # 请将下面的 IP 替换为实际 IP
    g.__executor = shipane_sdk.JoinQuantExecutor(
        host='xxx.xxx.xxx.xxx',
        port=8888,
        key='',
        client=''
    )


def repo(context):
    if context.run_params.type == 'sim_trade':
        security = '131810'
        df = ts.get_realtime_quotes(security)
        order = {
            'action': 'SELL',
            'symbol': security,
            'type': 'LIMIT',
            'price': float(df['bid'][0]),
            'amountProportion': 'ALL'
        }
        g.__executor.client.execute(**order)
    else:
        log.info('回测中不进行逆回购')
