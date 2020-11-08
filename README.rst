StrategyEase-Python-SDK
=======================

策略易（StrategyEase）Python SDK。

| 策略易是\ `爱股网 <http://www.iguuu.com>`__\ 旗下的策略自动化解决方案；提供基于 HTTP 协议的 RESTFul Service，并管理交易客户端。
| 详情见：http://www.iguuu.com/e
| 交流QQ群：115279569 |策略交流|
|

.. contents:: **目录**

原理概述
--------
- 策略易通过调用 WINDOWS API 对交易客户端进行操作。
- 策略易提供基于 HTTP 协议的 RESTFul Service/API。
- SDK 对 API 进行了封装（由 strategyease_sdk/client.py 中的 Client 类实现）。
- 本地策略或量化交易平台（目前支持聚宽、米筐、优矿）的模拟交易通过调用 SDK 实现自动下单。

功能介绍
--------

- 简单的策略易 HTTP API 封装，见 strategyease_sdk/client.py
- 定时任务

  - 多账号自动新股申购（自动打新）
  - 多账号自动逆回购
  - 定时批量下单

- 策略集成

  - 聚宽（JoinQuant）集成
  - 米筐（RiceQuant）集成
  - 优矿（Uqer）集成
  - 果仁（Guorn）集成

安装
--------------

- 安装 Python 3.5（建议安装 `Anaconda3-4.2.0 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/>`_）
- 命令行中运行

+--------+-------------------------------------------------------------------------+
| 正式版 | :code:`pip install --no-binary strategyease_sdk strategyease_sdk`       |
+--------+-------------------------------------------------------------------------+
| 测试版 | :code:`pip install --pre --no-binary strategyease_sdk strategyease_sdk` |
+--------+-------------------------------------------------------------------------+

升级
--------------

- 命令行中运行

+--------+---------------------------------------------------------------------------------------------+
| 正式版 | :code:`pip install --upgrade --no-deps --no-binary strategyease_sdk strategyease_sdk`       |
+--------+---------------------------------------------------------------------------------------------+
| 测试版 | :code:`pip install --upgrade --pre --no-deps --no-binary strategyease_sdk strategyease_sdk` |
+--------+---------------------------------------------------------------------------------------------+

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
见《`定时任务调度说明 <docs/scheduler.rst>`_》

策略集成
---------------------
见《`策略集成说明 <docs/online-quant-integration.rst>`_》

其他语言 SDK
------------

C# SDK
~~~~~~

| 由网友 @YBO（QQ：259219140）开发。
| 见 `ShiPanETradingSDK <http://git.oschina.net/ybo1990/ShiPanETradingSDK>`_

.. |策略交流| image:: http://pub.idqqimg.com/wpa/images/group.png
   :target: http://shang.qq.com/wpa/qunwpa?idkey=1ce867356702f5f7c56d07d5c694e37a3b9a523efce199bb0f6ff30410c6185d%22
