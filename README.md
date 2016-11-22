# ShiPanE-Python-SDK
实盘易（ShiPanE）Python SDK，通达信自动化交易 API。

## 聚宽集成
* 将 shipane_sdk/client.py 上传至聚宽“投资研究”根目录，并重命名为 shipane_sdk.py。
* 将 shipane_sdk/joinquant_executor.py 中的 class JoinQuantExecutor（不包含 import）追加到 shpane_sdk.py 中。
* 用法请参考 examples/simply_joinquant_strategy.py。
