import shipane_sdk


# 注意：需将回测调成分钟级别
# 注意：SDK内部取今日时间来获取新股数据
# 注意：用于回测没有意义，需挂到“模拟交易”

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 每天的开市后10分钟进行新股申购。参数设置见：https://www.ricequant.com/api/python/chn#scheduler
    scheduler.run_daily(purchase_convertible_bonds, time_rule=market_open(minute=10))


def before_trading(context):
    # 创建 RiceQuantStrategyManagerFactory 对象
    # 参数为 shipane_sdk_config_template.yaml 中配置的 manager id
    context.__manager = shipane_sdk.RiceQuantStrategyManagerFactory(context).create('manager-1')


def purchase_convertible_bonds(context, bar_dict):
    try:
        context.__manager.purchase_convertible_bonds()
    except:
        import sys
        s = sys.exc_info()
        logger.error("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))
