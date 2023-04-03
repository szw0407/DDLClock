# DDL闹钟项目

项目概述：https://docs.propranolol.cn/docs/ddl_clock.html

启动项目：

1. 获得项目源代码
2. 双击`start.bat`
3. 第一次使用的时候，你需要扫描命令行中展示的二维码完成QQ登录；除此以外，你都不需要再次手动登录QQ。登录会自动完成。如果你需要退出QQ登录状态，建议你使用手机QQ的设备管理删除那个“安卓手表”。
4. 第一次登录微软账户，可能会不能立刻更新状态。怀疑是token需要一小会才能有用。稍等几秒钟刷新一下前端页面就正常了。
5. 如果出现异常，可以手动通过Python安装`requirements.txt`构建。在对应的路径运行：
`python -m pip install -r requirements.txt`