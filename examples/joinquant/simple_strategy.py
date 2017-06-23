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
    # 保存 order 对象
    order_ = order(g.security, 100)
    # 实盘易依据聚宽的 order 对象下单
    g.__manager.execute(order_)

    order_ = order(g.security, -100)
    g.__manager.execute(order_)

    # 撤单
    g.__manager.cancel(order_)
