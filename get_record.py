import requests
import json
import time
import os
import re
from urllib.parse import unquote

# 配置保持不变
USER_ID = "Your uid"  # 重要! # ---------------------------------------------------------
URL_BASE = f"https://www.luogu.com.cn/record/list?user={USER_ID}&page="
FILE_NAME = f"{USER_ID}.json"
COOKIES = {
    "__client_id": "Your cookie", # 重要! # ---------------------------------------------
    "_uid": USER_ID
}
HEADERS = {
    "User-Agent": "Chtholly Nota Senioriou",# 彩蛋喵
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.luogu.com.cn/"
}

def extract_json_from_html(html_text):
    """从 HTML 中提取 window._feInjection 里的 JSON 数据"""
    # 正则定位：匹配 window._feInjection = JSON.parse(decodeURIComponent("...")) 内部的内容
    pattern = r'window\._feInjection = JSON\.parse\(decodeURIComponent\("(.+?)"\)\);'
    match = re.search(pattern, html_text)
    if match:
        encoded_json = match.group(1)
        # 解码 URL 编码并转为 Python 字典
        return json.loads(unquote(encoded_json))
    return None

def crawl():
    # 读取本地已有的提交 ID (逻辑同前)
    local_data = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            local_data = json.load(f)
    
    latest_id = local_data[0]['id'] if local_data else None
    new_records = []
    page = 1

    while True:
        print(f"正在抓取第 {page} 页...")
        try:
            response = requests.get(f"{URL_BASE}{page}", headers=HEADERS, cookies=COOKIES, timeout=10)
            res_data = extract_json_from_html(response.text)
            
            if not res_data:
                print("解析 HTML 数据失败，可能是模板已更改或被反爬拦截。")
                break

            records = res_data.get("currentData", {}).get("records", {}).get("result", [])
            
            if not records:
                print("抓取完毕或当前页无数据。")
                break

            stop_found = False
            for item in records:
                if latest_id and item['id'] == latest_id:
                    print(f"到达本地存量数据位置 (ID: {latest_id})，停止抓取。")
                    stop_found = True
                    break
                
                # 按照你的本地 {uid}.json 格式精简字段
                new_records.append({
                    "time": item.get("time"),
                    "memory": item.get("memory"),
                    "problem": item.get("problem"),
                    "contest": item.get("contest"),
                    "sourceCodeLength": item.get("sourceCodeLength"),
                    "submitTime": item.get("submitTime"),
                    "language": item.get("language"),
                    "id": item.get("id"),
                    "status": item.get("status"),
                    "enableO2": item.get("enableO2"),
                    "score": item.get("score")
                })

            if stop_found:
                break
                
            page += 1
            time.sleep(3)

        except Exception as e:
            print(f"发生异常: {e}")
            break

    # 合并并保存
    if new_records:
        final_data = new_records + local_data
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"更新成功！新增 {len(new_records)} 条，总计 {len(final_data)} 条。")
    else:
        print("没有新记录需要更新。")

if __name__ == "__main__":
    crawl()