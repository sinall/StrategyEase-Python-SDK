# ShiPanE-Python-SDK
实盘易（ShiPanE）Python SDK，通达信自动化交易 API。

实盘易是[爱股网](http://www.iguuu.com)旗下的股票自动化解决方案；可管理通达信等交易终端，并为用户提供基于 HTTP 协议的 RESTFul service。  
详情见：http://www.iguuu.com/e  
交流QQ群：11527956 [![实盘易-股票自动交易](http://pub.idqqimg.com/wpa/images/group.png)](http://shang.qq.com/wpa/qunwpa?idkey=1ce867356702f5f7c56d07d5c694e37a3b9a523efce199bb0f6ff30410c6185d")

## 聚宽集成
### 一. 推送方式
适用于云服务器环境，例如阿里云；特点是稳定、高效，集成简单。

#### 先决条件
* 部署实盘易成功
* 手动测试通过
* 聚宽（公网）可访问实盘易

#### 步骤
* 将 shipane_sdk/client.py 上传至聚宽“投资研究”根目录，并重命名为 shipane_sdk.py。
* 将 shipane_sdk/joinquant/executor.py 追加到 shpane_sdk.py 中。
* 用法请参考 examples/joinquant/simply_strategy.py (注意将其中的 xxx.xxx.xxx.xxx 替换为实际 IP)。

### 二. 抓取方式
无需云服务器，采用定时轮询的方式，实时性不如"推送方式"。

#### 先决条件
* 部署实盘易成功
* 手动测试通过

#### 步骤
* git clone 或下载项目到本地。
* 安装必要的依赖 "pip install requests"。
* 参考 examples/joinquant/config/config.ini.template 创建 examples/joinquant/config/config.ini，并完善配置。
* 命令行运行 "python ./examples/joinquant/simple_runner.py"。
