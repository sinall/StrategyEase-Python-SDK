import shipane_sdk


# 注意：需将回测调成分钟级别
# 注意：SDK内部取今日时间来获取新股数据
# 注意：用于回测没有意义，需挂到“我的交易”

def initialize(context):
    # 每天的开市后10分钟进行新股申购，参数设置见：https://www.joinquant.com/api#定时运行
    run_daily(purchase_new_stocks, '9:40')


def process_initialize(context):
    # 创建 StrategyManager 对象
    # 参数为配置文件中的 manager id
    g.__manager = shipane_sdk.JoinQuantStrategyManagerFactory(context).create('manager-1')


def purchase_new_stocks(context):
    if context.run_params.type == 'sim_trade':
        g.__manager.purchase_new_stocks()
    else:
        log.info('回测中不进行新股申购')
