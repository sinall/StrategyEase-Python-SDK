策略集成
==================

.. contents:: **目录**

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


.. _scripts/strategyease_sdk_installer.ipynb: https://raw.githubusercontent.com/sinall/StrategyEase-Python-SDK/master/scripts/strategyease_sdk_installer.ipynb
