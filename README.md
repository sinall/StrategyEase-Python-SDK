# ShiPanE-Python-SDK
实盘易（ShiPanE）Python SDK，通达信自动化交易 API。

实盘易是[爱股网](http://www.iguuu.com)旗下的股票自动化解决方案；可管理通达信等交易终端，并为用户提供基于 HTTP 协议的 RESTFul service。  
详情见：http://www.iguuu.com/e  
交流QQ群：11527956 [![实盘易-股票自动交易](http://pub.idqqimg.com/wpa/images/group.png)](http://shang.qq.com/wpa/qunwpa?idkey=1ce867356702f5f7c56d07d5c694e37a3b9a523efce199bb0f6ff30410c6185d")

## 聚宽集成
### 一. 推送方式
适用于云服务器环境，例如阿里云；特点是稳定、高效，集成简单。

#### 先决条件
* 已经成功部署实盘易
* 测试通过
* 聚宽（公网）可访问实盘易

#### 步骤
* 将 shipane_sdk/client.py 上传至聚宽“投资研究”根目录，并重命名为 shipane_sdk.py。
* 将 shipane_sdk/joinquant_executor.py 追加到 shpane_sdk.py 中。
* 用法请参考 examples/simply_joinquant_strategy.py。

### 二. 抓取方式
开发中
