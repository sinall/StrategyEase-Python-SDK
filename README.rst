ShiPanE-Python-SDK
==================

实盘易（ShiPanE）Python SDK，通达信自动化交易 API。

| 实盘易是\ `爱股网 <http://www.iguuu.com>`__\ 旗下的股票自动化解决方案；提供基于 HTTP 协议的 RESTFul Service，从而管理通达信等交易终端。
| 详情见：http://www.iguuu.com/e
| 交流QQ群：11527956 |实盘易-股票自动交易|

原理概述
--------
- 实盘易通过调用 WINDOWS API 对通达信进行操作。
- 实盘易提供基于 HTTP 协议的 RESTFul Service/API。
- SDK 对 API 进行了封装（由 shipane_sdk/client.py 中的 Client 类实现）。
- 本地策略或量化交易平台（目前支持聚宽、米筐）的模拟交易通过调用 SDK 实现自动下单。

功能介绍
--------

- 简单的实盘易 HTTP API 封装，见 shipane_sdk/client.py
- 多账号自动新股申购（自动打新）
- 聚宽（JoinQuant）集成
- 米筐（RiceQuant）集成

定时任务调度
--------------

- 多账号自动新股申购（自动打新）
- 聚宽（JoinQuant）自动跟单（抓取方式）
- 米筐（RiceQuant）自动跟单（抓取方式）

Windows
~~~~~~~

安装
^^^^

- 安装 Python 3.5（建议安装 `Anaconda3 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/>`_）
- cmd 中运行：pip install --no-binary shipane_sdk shipane_sdk
- cmd 中运行：cd %UserProfile%\\.shipane_sdk\\config
- cmd 中运行：echo No | copy /-Y scheduler-example.ini scheduler.ini

配置
^^^^

- cmd 中运行：explorer %UserProfile%\\.shipane_sdk\\config
- 修改 scheduler.ini 中的配置（建议使用Notepad++）

运行
^^^^

- 找到 python 安装目录，例如：C:\\Program Files\\Anaconda3
- cmd 下执行（具体路径自行修改）：python "C:\\Program Files\\Anaconda3\\Scripts\\shipane-scheduler.py"

升级
^^^^

- cmd 中运行：pip install --upgrade --no-deps --no-binary shipane_sdk shipane_sdk
- 参考 scheduler-example.ini 修改 scheduler.ini

Mac/Linux
~~~~~~~~~

安装
^^^^

- 安装 Python 3.5
- terminal 中运行：pip install --no-binary shipane_sdk shipane_sdk
- terminal 中运行：cp -n ~/.shipane_sdk/config/scheduler-example.ini ~/.shipane_sdk/config/scheduler.ini

配置
^^^^

- 修改 ~/.shipane_sdk/config/scheduler.ini

运行
^^^^

- terminal 中运行：shipane-scheduler.py

升级
~~~~

- terminal 中运行：pip install --upgrade --no-deps --no-binary shipane_sdk shipane_sdk
- 参考 scheduler-example.ini 修改 scheduler.ini

聚宽（JoinQuant）集成
---------------------

一. 推送方式
~~~~~~~~~~~~

适用于云服务器环境，例如阿里云；特点是稳定、高效，集成简单。

准备工作
^^^^^^^^

- 部署实盘易。
- 本地测试通过。
- 远程测试通过。

步骤
^^^^

- 将 shipane\_sdk/client.py 上传至聚宽“投资研究”根目录，并重命名为 shipane\_sdk.py。
- 将 shipane\_sdk/joinquant/executor.py 拷贝粘贴到 shipane\_sdk.py 末尾。
- 用法请参考 examples/joinquant/simple\_strategy.py (注意将其中的 xxx.xxx.xxx.xxx 替换为实际 IP)。

二. 抓取方式
~~~~~~~~~~~~

无需云服务器，采用定时轮询的方式，实时性不如"推送方式"。

准备工作
^^^^^^^^

- 部署实盘易。
- 测试通过。

步骤
^^^^

见 `定时任务调度 <#定时任务调度>`__

米筐（RiceQuant）集成
---------------------

一. 推送方式
~~~~~~~~~~~~

适用于云服务器环境，例如阿里云；特点是稳定、高效，集成简单。

准备工作
^^^^^^^^

- 部署实盘易。
- 本地测试通过。
- 远程测试通过。

步骤
^^^^

- 将 shipane\_sdk/client.py 上传米筐“策略研究”根目录，并重命名为 shipane\_sdk.py。
- 将 shipane\_sdk/ricequant/executor.py 拷贝粘贴到 shipane\_sdk.py 末尾。
- 用法请参考 examples/ricequant/simple\_strategy.py (注意将其中的 xxx.xxx.xxx.xxx 替换为实际 IP)。

二. 抓取方式
~~~~~~~~~~~~

采用定时轮询的方式。

准备工作
^^^^^^^^

- 部署实盘易。
- 测试通过。

步骤
^^^^

见 `定时任务调度 <#定时任务调度>`__

其他语言 SDK
------------

C# SDK
~~~~~~

| 由网友 @YBO（QQ：259219140）开发。
| 见 `ShiPanETradingSDK <http://git.oschina.net/ybo1990/ShiPanETradingSDK>`_

.. |实盘易-股票自动交易| image:: http://pub.idqqimg.com/wpa/images/group.png
   :target: http://shang.qq.com/wpa/qunwpa?idkey=1ce867356702f5f7c56d07d5c694e37a3b9a523efce199bb0f6ff30410c6185d%22
