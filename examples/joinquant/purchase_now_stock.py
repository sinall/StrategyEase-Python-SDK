import shipane_sdk


# 注意：需将回测调成分钟级别，否则daily_mission不会运行
# 注意：SDK内部取今日时间来获取新股数据
# 注意：用于回测没有意义，需挂到“我的交易”

def initialize(context):
    # 申购新股的时间的时间
    run_daily(daily_mission, '09:50', reference_security='000001.XSHG')


def process_initialize(context):
    # 创建 JoinQuantExecutor 对象
    # 可选参数包括：host, port, key, client, timeout 等
    # 请将下面的 IP 替换为实际 IP
    g.__executor = shipane_sdk.JoinQuantExecutor(
        host='xxx.xxx.xxx.xxx',
        port=8888,
        key='',
        client=''
    )


def daily_mission(context):
    g.__executor.purchase_new_stocks()
