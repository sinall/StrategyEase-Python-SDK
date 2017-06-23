import tushare as ts

import shipane_sdk


# 注意：需将回测调成分钟级别
# 注意：用于回测没有意义，需挂到“我的交易”

def initialize(context):
    # 每天的收盘前5分钟进行逆回购，参数设置见：https://www.joinquant.com/api#定时运行
    run_daily(repo, '14:55')


def process_initialize(context):
    # 创建 StrategyManager 对象
    # 参数为配置文件中的 manager id
    g.__manager = shipane_sdk.JoinQuantStrategyManagerFactory(context).create('manager-1')


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
        g.__manager.execute(**order)
    else:
        log.info('回测中不进行逆回购')
