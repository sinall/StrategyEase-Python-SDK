import shipane_sdk


# 注意：需将回测调成分钟级别
# 注意：用于回测没有意义，需挂到“我的交易”

def initialize(context):
    # 每天的收盘前5分钟进行逆回购。参数设置见：https://www.ricequant.com/api/python/chn#scheduler
    scheduler.run_daily(repo, time_rule=market_close(minute=5))


def process_initialize(context):
    # 创建 RiceQuantStrategyManagerFactory 对象
    # 参数为 shipane_sdk_config_template.yaml 中配置的 manager id
    context.__manager = shipane_sdk.RiceQuantStrategyManagerFactory(context).create('manager-1')


def repo(context):
    try:
        context.__manager.repo()
    except:
        import sys
        s = sys.exc_info()
        logger.error("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))
