# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import shipane_sdk


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.s1 = "000001.XSHE"
    # 实时打印日志
    logger.info("Interested at stock: " + str(context.s1))

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

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！
    # 保存 order_id
    order_id = order_shares(context.s1, 100)
    # 实盘易依据 order_id 下单
    context.__executor.execute(order_id)

    order_id = order_shares(context.s1, -100)
    context.__executor.execute(order_id)

    cancel_order(order_id)
    context.__executor.cancel(order_id)
