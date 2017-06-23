import shipane_sdk


# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 定义一个全局变量, 保存要操作的股票
    # 000001(股票:平安银行)
    g.security = '000001.XSHE'
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')


def process_initialize(context):
    # 创建 StrategyManager 对象
    # 参数为配置文件中的 manager id
    g.__manager = shipane_sdk.JoinQuantStrategyManagerFactory(context).create('manager-1')


# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    try:
        order(g.security, 100)

    finally:
        # 放在 finally 块中，以防原有代码抛出异常或者 return
        # 在函数结尾处加入以下语句，用来将模拟盘同步至实盘
        g.__manager.sync()
