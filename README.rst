ShiPanE-Python-SDK
==================

实盘易（ShiPanE）Python SDK，通达信自动化交易 API。

| 实盘易是\ `爱股网 <http://www.iguuu.com>`__\ 旗下的股票自动化解决方案；提供基于HTTP协议的RESTFul service，进而可管理通达信等交易终端。
| 详情见：http://www.iguuu.com/e
| 交流QQ群：11527956 |实盘易-股票自动交易|


原理概述
--------
- 在PC或者云服务上运行\ `实盘易 <http://www.iguuu.com/download/e/installers/ShiPanE.exe>`__\ 客户端，同时运行通达信，实盘易识别通达信以后调用windows api（极个别功能模拟键盘鼠标），对通达信进行操作，进而实现自动登录、自动交易、自动打新、查询等功能
- 客户端提供基于HTTP协议的RESTFul service（HTTP API 封装，由shipane_sdk/client.py的Client类实现）
- 有了这些API，可以运行本地策略的时候直接调用，或者借用量化交易平台（目前支持聚宽、米筐）的模拟交易框架，实现自动下单。

功能介绍
--------

- 简单的实盘易 HTTP API 封装（源码见 shipane_sdk/client.py，示例见\ `爱股网 <http://www.iguuu.com/e#settings>`__\ ）
- 多账号自动新股申购（自动打新）
- 聚宽（JoinQuant）自动跟单
- 米筐（RiceQuant）自动跟单


安装方法
---------

Windows
~~~~~~~

安装
^^^^

- 安装 Python 3.5（建议安装 `Anaconda3 <https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/>`_）
- cmd 中运行：pip install --no-binary shipane_sdk shipane_sdk
- cmd 中运行：cd %UserProfile%\\.shipane_sdk\\config
- cmd 中运行：echo No | copy /-Y scheduler-example.ini scheduler.ini

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

升级
^^^^

- terminal 中运行：pip install --upgrade --no-deps --no-binary shipane_sdk shipane_sdk
- 参考 scheduler-example.ini 修改 scheduler.ini




聚宽（JoinQuant）自动跟单
-------------------------

方式一 推送方式
~~~~~~~~~~~~~~~~~~~

| 适用于云服务器环境（例如阿里云，推荐）或有公网IP的PC（不推荐）
| 特点是稳定、高效，集成简单，跟单较快速  

准备工作
^^^^^^^^

-  本地部署实盘易成功
-  本地测试通过（比如浏览器访问 http://localhost:8888/accounts 能返回账户信息）
-  本地开启端口8888（如果被修改，开启对应端口，方法见搜索引擎）
-  远端测试通过（尝试用聚宽或外网电脑访问实盘易，比如访问 http://x.x.x.x:8888/accounts 返回账户信息成功，x.x.x.x为你的ip）。

步骤
^^^^

-  将 shipane\_sdk/client.py 上传至聚宽“投资研究”根目录，并重命名为 shipane\_sdk.py。
-  将 shipane\_sdk/joinquant/executor.py 拷贝粘贴到 shpane\_sdk.py 末尾。
-  参考 examples/joinquant/simple\_strategy.py (注意将其中的 xxx.xxx.xxx.xxx 替换为实际 IP)改写聚宽策略
-  本地保持运行实盘易和通达信，聚宽策略模拟交易时会发回数据，本地处理后即能下单

注意
^^^^
-  如果是使用PC运行，必须要有公网IP，如果使用了路由器，则路由器获取的公网IP即是你的公网IP，但必须开启DMZ转发和DHCP静态地址保留（有些宽带给的是NAT转发的IP，则没有公网IP），不懂的名词可逐一百度。没有公网IP或不会处理请使用方法二，抓取方式
-  不建议家里PC+路由器的环境，因为路由器获取的公网IP不固定的，若路由器重启，IP更变，则策略的下单发不回来（您可能因此遭受损失），则需要修改手动修改策略，失去程序化的意义，实在要家里路由器的，可以用动态域名的方法

方式二 抓取方式
~~~~~~~~~~~~~~~~~~

无需云服务器，采用周期性爬取聚宽模拟交易页面的方式，实时性不如"推送方式"。

准备工作
^^^^^^^^

-  本地部署实盘易成功
-  本地测试通过（比如浏览器访问http://localhost:8888/accounts返回账户信息）

步骤
^^^^

见 `定时任务调度 <#定时任务调度>`__

米筐（RiceQuant）自动跟单
-------------------------

方式一 推送方式
~~~~~~~~~~~~~~~~~~~

见聚宽方式，但是使用文件不同

步骤
^^^^

-  将 shipane\_sdk/client.py 上传米筐“策略研究”根目录，并重命名为 shipane\_sdk.py。
-  将 shipane\_sdk/ricequant/executor.py 拷贝粘贴到 shpane\_sdk.py 末尾。
-  用法请参考 examples/ricequant/simple\_strategy.py (注意将其中的 xxx.xxx.xxx.xxx 替换为实际 IP)改写聚宽策略
-  本地保持运行实盘易和通达信，聚宽策略模拟交易时会发回数据，本地处理后即能下单

方式二 抓取方式
~~~~~~~~~~~~~~~~~~

无需云服务器，采用周期性爬取米筐模拟交易页面的方式，实时性不如"推送方式"。

准备工作
^^^^^^^^

-  本地部署实盘易成功
-  本地测试通过（比如浏览器访问http://localhost:8888/accounts返回账户信息）

步骤
^^^^

见 `定时任务调度 <#定时任务调度>`__

定时任务调度
--------------

- 可实现功能：
- 多账号自动新股申购（自动打新）
- 聚宽（JoinQuant）自动跟单（抓取方式）
- 米筐（RiceQuant）自动跟单（抓取方式）

Windows
~~~~~~~

配置
^^^^

- cmd 中运行：explorer %UserProfile%\\.shipane_sdk\\config(即用资源管理器打开config目录,也可手动打开用户目录下的.shipane_sdk/config)
- 修改其中的 scheduler.ini配置文件（建议使用Notepad++防止编码错误，另外文件scheduler-example.ini为示例和说明）

运行
^^^^

- 找到 python 安装目录，例如：C:\\Program Files\\Anaconda3
- cmd 下执行（具体路径自行修改）：python "C:\\Program Files\\Anaconda3\\Scripts\\shipane-scheduler.py"
- 或者搜索shipane-scheduler.py，用python运行


Mac/Linux
~~~~~~~~~


配置
^^^^

- 修改 ~/.shipane_sdk/config/scheduler.ini（旁边文件scheduler-example.ini为示例和说明）

运行
^^^^

- terminal 中运行：shipane-scheduler.py


其他语言 SDK
------------

C# SDK
~~~~~~

| 由网友 @YBO（QQ：259219140）开发。
| 见 `ShiPanETradingSDK <http://git.oschina.net/ybo1990/ShiPanETradingSDK>`_

.. |实盘易-股票自动交易| image:: http://pub.idqqimg.com/wpa/images/group.png
   :target: http://shang.qq.com/wpa/qunwpa?idkey=1ce867356702f5f7c56d07d5c694e37a3b9a523efce199bb0f6ff30410c6185d%22
