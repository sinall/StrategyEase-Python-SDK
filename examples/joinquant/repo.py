import strategyease_sdk


# 注意：需将回测调成分钟级别
# 注意：用于回测没有意义，需挂到“我的交易”

def initialize(context):
    # 每天的收盘前5分钟进行逆回购，参数设置见：https://www.joinquant.com/api#定时运行
    run_daily(repo, '14:55')


def process_initialize(context):
    # 创建 StrategyManager 对象
    # 参数为配置文件中的 manager id
    g.__manager = strategyease_sdk.JoinQuantStrategyManagerFactory(context).create('manager-1')


def repo(context):
    g.__manager.repo()
