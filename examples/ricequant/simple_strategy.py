import shipane_sdk


def init(context):
    context.s1 = "000001.XSHE"

def before_trading(context):
    # 创建 RiceQuantStrategyManagerFactory 对象
    # 参数为 shipane_sdk_config_template.yaml 中配置的 manager id
    context.__manager = shipane_sdk.RiceQuantStrategyManagerFactory(context).create('manager-1')

def handle_bar(context, bar_dict):
    # 保存 order
    order_ = order_shares(context.s1, 100)
    # 实盘易依据 order_ 下单
    context.__manager.execute(order_)

    order_ = order_shares(context.s1, -100)
    context.__manager.execute(order_)

    cancel_order(order_)
    context.__manager.cancel(order_)
