StrategyEase-Python-SDK
==================

策略易（StrategyEase）Python SDK。

| 策略易是\ `爱股网 <http://www.iguuu.com>`__\ 旗下的股票自动化解决方案；提供基于 HTTP 协议的 RESTFul Service，从而管理通达信等交易终端。
| 详情见：http://www.iguuu.com/e
| 交流QQ群：11527956 |策略交流|
|

.. contents:: **目录**

原理概述
--------
- 策略易通过调用 WINDOWS API 对通达信进行操作。
- 策略易提供基于 HTTP 协议的 RESTFul Service/API。
- SDK 对 API 进行了封装（由 strategyease_sdk/client.py 中的 Client 类实现）。
- 本地策略或量化交易平台（目前支持聚宽、米筐、优矿）的模拟交易通过调用 SDK 实现自动下单。

功能介绍
--------

- 简单的策略易 HTTP API 封装，见 strategyease_sdk/client.py
- 多账号自动新股申购（自动打新）
- 多账号自动逆回购
- 定时批量下单
- 聚宽（JoinQuant）集成
- `米筐（RiceQuant）`_ 集成
- 优矿（Uqer）集成
- `果仁（Guorn）集成 <#果仁guorn集成>`__

基本用法
--------------

.. code:: python

  import logging

  import strategyease_sdk

  logging.basicConfig(level=logging.DEBUG)

  client = strategyease_sdk.Client(host='localhost', port=8888, key='')
  account_info = client.get_account('title:monijiaoyi')
  print(account_info)

详见：examples/basic_example.py

测试用例
--------------

策略易 HTTP API 封装对应的测试用例见：

+------------+------------------------------------------------------+
| 查询及下单 | tests/strategyease_sdk/test_client.py                |
+------------+------------------------------------------------------+
| 客户端管理 | tests/strategyease_sdk/test_client_management.py     |
+------------+------------------------------------------------------+
| 融资融券   | tests/strategyease_sdk/test_client_margin_trading.py |
+------------+------------------------------------------------------+
| 其他       | tests/strategyease_sdk/...                           |
+------------+------------------------------------------------------+

定时任务调度
--------------

- 多账号自动申购新股（自动打新）
- 多账号自动申购转债
- 多账号自动逆回购
- 定时批量下单
- 聚宽（JoinQuant）
   - 自动跟单模拟交易（抓取方式）
   - 自动同步擂台策略（抓取方式）
- `米筐（RiceQuant）`_ 自动跟单（抓取方式）
- 优矿（Uqer）自动跟单（抓取方式）

Windows
~~~~~~~

安装
^^^^

- 安装 Python 3.5（建议安装 `Anaconda3-4.2.0 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/>`_）
- cmd 中运行

+--------+-------------------------------------------------------------------------+
| 正式版 | :code:`pip install --no-binary strategyease_sdk strategyease_sdk`       |
+--------+-------------------------------------------------------------------------+
| 测试版 | :code:`pip install --pre --no-binary strategyease_sdk strategyease_sdk` |
+--------+-------------------------------------------------------------------------+

配置
^^^^

- cmd 中运行：:code:`explorer %UserProfile%\.strategyease_sdk\config`
- 修改 scheduler.ini 中的配置（建议使用Notepad++）

运行
^^^^

- cmd 下运行：:code:`strategyease-scheduler`

升级
^^^^

- cmd 中运行

+--------+---------------------------------------------------------------------------------------------+
| 正式版 | :code:`pip install --upgrade --no-deps --no-binary strategyease_sdk strategyease_sdk`       |
+--------+---------------------------------------------------------------------------------------------+
| 测试版 | :code:`pip install --upgrade --pre --no-deps --no-binary strategyease_sdk strategyease_sdk` |
+--------+---------------------------------------------------------------------------------------------+

- 参考 scheduler-template.ini 修改 scheduler.ini

日志
^^^^

- cmd 中运行：:code:`explorer %UserProfile%\AppData\Local\爱股网\策略易`

Mac/Linux
~~~~~~~~~

安装
^^^^

- 安装 Python 3.5
- terminal 中运行

+--------+-------------------------------------------------------------------------+
| 正式版 | :code:`pip install --no-binary strategyease_sdk strategyease_sdk`       |
+--------+-------------------------------------------------------------------------+
| 测试版 | :code:`pip install --pre --no-binary strategyease_sdk strategyease_sdk` |
+--------+-------------------------------------------------------------------------+

配置
^^^^

- 修改 ~/.strategyease_sdk/config/scheduler.ini

运行
^^^^

- terminal 中运行：:code:`strategyease-scheduler:code:`

升级
^^^^

- terminal 中运行

+--------+---------------------------------------------------------------------------------------------+
| 正式版 | :code:`pip install --upgrade --no-deps --no-binary strategyease_sdk strategyease_sdk`       |
+--------+---------------------------------------------------------------------------------------------+
| 测试版 | :code:`pip install --upgrade --pre --no-deps --no-binary strategyease_sdk strategyease_sdk` |
+--------+---------------------------------------------------------------------------------------------+

- 参考 scheduler-template.ini 修改 scheduler.ini

聚宽（JoinQuant）集成
---------------------

一. 推送方式
~~~~~~~~~~~~

适用于云服务器环境，例如阿里云；特点是稳定、高效，集成简单。

准备工作
^^^^^^^^

- 部署策略易。
- 本地测试通过。
- 远程测试通过。

步骤
^^^^

- 下载 `scripts/strategyease_sdk_installer.ipynb`_ 并上传至“投资研究”根目录。
- 打开该文件，设置参数：QUANT_NAME = 'joinquant'
- 查看其它参数并根据需要进行修改。
- 点击工具栏中的右箭头运行该文件，并检查窗口中打印的日志。
- 修改 strategyease_sdk_config.yaml，升级后需参考 strategyease_sdk_config_template.yaml 进行修改。
- 修改策略代码，可参考如下示例：

  - examples/joinquant/simple\_strategy.py - 基本跟单用法（侵入式设计，不推荐）
  - examples/joinquant/advanced\_strategy.py - 高级同步、跟单用法（非侵入式设计，推荐）
  - examples/joinquant/new\_stocks\_purchase.py - 新股申购
  - examples/joinquant/convertible\_bonds\_purchase.py - 转债申购
  - examples/joinquant/repo.py - 逆回购

同步操作注意事项：

- 同步操作根据模拟盘持仓比例对实盘进行调整。
- 同步操作依赖于“可用”资金。请留意配置文件中“撤销全部订单”相关选项。
- “新股申购”不影响“可用”资金，并且不可被撤销，因此不影响同步功能。
- 同步操作依赖于策略易 API /adjustments；因此也依赖于“查询投资组合”API，使用前请先做好测试及配置。
- 同步操作使用“市价单”。
- 如遇到策略报错“ImportError: No module named strategyease_sdk”，请稍后重试。
- 量化平台模拟交易运行中升级 SDK，需重启生效。

二. 抓取方式
~~~~~~~~~~~~

无需云服务器，采用定时轮询的方式，实时性不如"推送方式"。

准备工作
^^^^^^^^

- 部署策略易。
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

- 部署策略易。
- 本地测试通过。
- 远程测试通过。

步骤
^^^^

- 下载 `scripts/strategyease_sdk_installer.ipynb`_ 并上传至“策略研究”根目录。
- 打开该文件，设置参数：QUANT_NAME = 'ricequant'
- 查看其它参数并根据需要进行修改。
- 点击工具栏中的右箭头运行该文件，并检查窗口中打印的日志。
- 修改策略代码，可参考如下示例：

  - examples/ricequant/simple\_strategy.py - 基本用法
  - examples/ricequant/advanced\_strategy.py - 高级同步用法（非侵入式设计，推荐）
  - examples/ricequant/new\_stocks\_purchase.py - 新股申购
  - examples/ricequant/convertible\_bonds\_purchase.py - 转债申购
  - examples/ricequant/repo.py - 逆回购

二. 抓取方式
~~~~~~~~~~~~

采用定时轮询的方式。

准备工作
^^^^^^^^

- 部署策略易。
- 测试通过。

步骤
^^^^

见 `定时任务调度 <#定时任务调度>`__

优矿（Uqer）集成
---------------------

一. 推送方式
~~~~~~~~~~~~

| 适用于云服务器环境，例如阿里云；特点是稳定、高效，集成简单。
| 开发中，暂不支持。

二. 抓取方式
~~~~~~~~~~~~

采用定时轮询的方式。

准备工作
^^^^^^^^

- 部署策略易。
- 测试通过。

步骤
^^^^

见 `定时任务调度 <#定时任务调度>`__

果仁（Guorn）集成
---------------------

一. 推送方式
~~~~~~~~~~~~

| 不支持。

二. 抓取方式
~~~~~~~~~~~~

采用定时轮询的方式。

准备工作
^^^^^^^^

- 部署策略易。
- 测试通过。

步骤
^^^^

见 `定时任务调度 <#定时任务调度>`__

字段要求
^^^^^^^^

见策略易《用户手册.txt》的“查询投资组合”章节，可通过策略易菜单“帮助>查看帮助”访问。

其他语言 SDK
------------

C# SDK
~~~~~~

| 由网友 @YBO（QQ：259219140）开发。
| 见 `ShiPanETradingSDK <http://git.oschina.net/ybo1990/ShiPanETradingSDK>`_

.. |策略交流| image:: http://pub.idqqimg.com/wpa/images/group.png
   :target: http://shang.qq.com/wpa/qunwpa?idkey=1ce867356702f5f7c56d07d5c694e37a3b9a523efce199bb0f6ff30410c6185d%22

.. _米筐（RiceQuant）: http://www.ricequant.com

.. _scripts/strategyease_sdk_installer.ipynb: https://raw.githubusercontent.com/sinall/StrategyEase-Python-SDK/master/scripts/strategyease_sdk_installer.ipynb
