## Star Shine

直播运营小工具合集

### Captain User

用户管理模块, 通过 xlsx 导入, 也可以直接在页面上添加用户

### Birthday Notice

生日提醒功能, 可以设置提醒时间, 发送微信通知, 发送桌面通知

### Revenue Manage

收益获取功能

模块一: 拉取特定日期范围的收益, 并且保存到 db 中;

模块二: 根据本地数据库中的数据进行保存, 和导出;

### 伴奏管理

- 基于爬虫的伴奏查询

### Road Map

DOING
- 单独的登录页面 + 系统设置
  - 退出登录 / 重新登录
  - 过期时间
  - 系统设置: 每天自动同步收益, 礼物用户自动同步到 Captain
  - 添加命令行来退出登录
  - 支持数据备份
- 用户信息更新功能
    - ~~DOING 提交后, 刷新页面~~
    - ~~支持用户信息修改改能~~
    - ~~支持农历生日的提醒~~
      - ~~农历生日和公历生日一起展示~~
    - ~~支持通过bilibili链接的同步功能;~~
    - ~~生日提醒功能: 点击按钮~~
    - ~~删除用户~~ 
    - ~~新增省市区, 和详细地址 https://ai.baidu.com/ai-doc/NLP/vk6z52h5n~~
    - BUG-FIX
      - ~~用户列表信息需要同时计算农历和阳历, 同时体现最近几天过生日, 超过 15 才显示日期~~
      - ~~地址变化交互优化~~
    - 用户消息面板:
      - ~~支持用户地址, 省市区+详细地址识别接口~~
    - 交互优化 + UI 优化
      - 用户查询
        - ~~查询提示中高亮显示匹配到的用户信息~~
        - 完成 grp view 的上下滑动
        - 修改 query 条的长度
- 收益功能
    - ~~用户登录功能~~
    - ~~收益查询(用户/金额/时间),~~
      - ~~导出表格~~ 
      - ~~分页展示~~
      - ~~搜索功能~~
      - ~~同步收益~~
    - 计算还有几天没有同步, 支持同步本月收益, 支持全部同步, 支持选择时间范围同步; 
    - 支持礼物类型查询, 支持用户名称查询, 去除金额查询, 去除时间查询
    - 支持表格字段排序
    - 支持导出文件的路径选择和导出dialog, 选增本月/本周/最近三个月
    - 交互优化 + UI 优化

FUTURE
    - 支持快捷键的记事本添加, 允许的主体: 用户, 收益, 伴奏
    - 支持数据库的每日备份
    - Center Topic: 的当前聊天室话题分析功能; 




