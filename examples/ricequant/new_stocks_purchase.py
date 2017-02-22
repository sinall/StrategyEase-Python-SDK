import shipane_sdk


# 注意：需将回测调成分钟级别
# 注意：SDK内部取今日时间来获取新股数据
# 注意：用于回测没有意义，需挂到“模拟交易”

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 每天的开市后10分钟进行新股申购。参数设置见：https://www.ricequant.com/api/python/chn#scheduler
    scheduler.run_daily(purchase_new_stocks, time_rule=market_open(minute=10))


def before_trading(context):
    # 创建 RiceQuantExecutor 对象
    # 可选参数包括：host, port, key, client, timeout 等
    # 请将下面的 IP 替换为实际 IP
    context.__executor = shipane_sdk.RiceQuantExecutor(
        host='xxx.xxx.xxx.xxx',
        port=8888,
        key='',
        client=''
    )


def purchase_new_stocks(context, bar_dict):
    context.__executor.purchase_new_stocks()
