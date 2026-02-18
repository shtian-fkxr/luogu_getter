# luogu_getter
获取你的洛谷提交记录

由 GPT5 辅助完成。

# 使用方式
首先你应该先安装 `pyhton` 和 `requests`。

然后执行：
```
python ./get_record.py
```
等待此程序执行完后执行：
```
python ./get_code.py
```
# 运行结果
此文件运行后会产生：

`{uid}.json`

其中是你的所有提交记录，在运行完 `get_record` 后就会创建，这也是 `get_record` 的全部作用。

`code` 和 `records` 文件夹：里面分别是你所有提交的代码和这个界面的 `html` 代码。

程序采用增量修改，就是说之前获取过的记录不会再次获取。

# 请合理使用本脚本。

$\color{white}\textup{\textmd{有彩蛋哦}}$
