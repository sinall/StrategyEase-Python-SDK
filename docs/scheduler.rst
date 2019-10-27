定时任务调度
=======================

.. contents:: **目录**

功能列表
--------------

- 多账号自动申购新股（自动打新）
- 多账号自动申购转债
- 多账号自动逆回购
- 定时批量下单
- 聚宽（JoinQuant）

  - 自动跟单模拟交易（抓取方式）
  - 自动同步擂台策略（抓取方式）

- 米筐（RiceQuant）自动跟单（抓取方式）
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
