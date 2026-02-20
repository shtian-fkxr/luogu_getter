# luogu_getter

获取你的洛谷提交记录，并保存对应代码与网页

###### 有彩蛋哦

## 📌 项目简介

`luogu_getter` 是一个用于抓取并保存你在洛谷（Luogu）上的提交记录与代码的轻量 Python 脚本集合。

运行后将自动：
- 获取指定用户的所有提交记录；
- 保存每次提交的代码和对应 HTML 页面；
- 以增量方式更新（已抓取过的数据不会重复抓取）。

> ⚠️ 本脚本仅用于合理合法的用途，请遵守洛谷平台使用协议，**不要滥用爬虫对服务器造成压力**。

## 🚀 功能

- 获取并保存洛谷用户的提交记录；
- 按提交分别下载代码与界面 HTML；
- 支持增量抓取：已有数据不会重复请求；
- 输出 `{uid}.json` 文件保存原始记录。

## 📥 依赖环境

请确保你已安装以下运行环境：

- Python 3.6+
- `requests`

可使用 pip 安装依赖：

```bash
pip install requests
````

## 🛠️ 使用方法

1. 在两个程序中填入你的 cookie！在两个程序中填入你的 cookie！在两个程序中填入你的 cookie！

2. 获取记录：

   ```bash
   python ./get_record.py
   ```

3. 下载代码：

   ```bash
   python ./get_code.py
   ```

运行后会生成如下内容：

* `{uid}.json` — 保存获取的全部提交记录；
* `code/` — 所有提交代码文件；
* `records/` — 各提交对应的网页 HTML。

## 🧠 工作逻辑

* `get_record.py`：访问 `https://www.luogu.com.cn/record/list?user={your uid}`，按用户 UID 获取所有提交记录；
* `get_code.py`：读取记录 JSON，下载每次提交包含的代码；
* 增量逻辑：只处理未保存过的记录以避免重复抓取。

## ⚙️ 示例输出结构
```
.
├── 123456.json
├── code
│   ├── R12345_Pxxxx.cpp
│   ├── R19345_Uxxxxx.cpp
│   └── R23456_Bxxxx.py
└── records
    ├── R12345.html
    ├── R19345.html
    └── R23456.html
```

## 📌 注意事项

* 洛谷对抓取频率有限制，请控制请求节奏；
* 如果脚本运行失败，检查账号是否需要登录或页面访问限制；
* 本项目 Star 越多越有动力更新 😊

[![Star History Chart](https://api.star-history.com/svg?repos=shtian-fkxr/luogu_getter&type=Date)](https://star-history.com/#shtian-fkxr/luogu_getter&Date)
