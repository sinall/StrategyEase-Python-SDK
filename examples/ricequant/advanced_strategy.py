import strategyease_sdk


def init(context):
    context.s1 = "000001.XSHE"

def before_trading(context):
    # 创建 RiceQuantStrategyManagerFactory 对象
    # 参数为 strategyease_sdk_config_template.yaml 中配置的 manager id
    context.__manager = strategyease_sdk.RiceQuantStrategyManagerFactory(context).create('manager-1')

def handle_bar(context, bar_dict):
    try:
        order_target_value(context.s1, 0)
        order_target_value(context.s1, 500)

        order_ = order_shares(context.s1, 100, style=LimitOrder(bar_dict[context.s1].limit_down))
        cancel_order(order_)
    finally:
        # 放在 finally 块中，以防原有代码抛出异常或者 return
        # 在函数结尾处加入以下语句，用来将模拟盘同步至实盘
        context.__manager.work()
