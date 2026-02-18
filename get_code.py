import requests
import time
import os
import re
import json
from urllib.parse import unquote

# === 配置区 ===
USER_ID = "Your uid"  # 重要! # ---------------------------------------------------------
URL_BASE = "https://www.luogu.com.cn/record/"
INPUT_FILE = f"{USER_ID}.json"  # 你的上一步产物
COOKIES = {
    "__client_id": "Your cookie", # 重要! # ---------------------------------------------
    "_uid": USER_ID
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.luogu.com.cn/"
}

# 路径配置
RECORDS_DIR = 'records'
CODE_DIR = 'code'

os.makedirs(RECORDS_DIR, exist_ok=True)
os.makedirs(CODE_DIR, exist_ok=True)

def get_extension_by_lang(lang_id):
    """根据洛谷语言 ID 返回后缀名"""
    # 常见映射，可以根据需要扩充
    mapping = {
        0: ".cpp", 1: ".py", 2: ".c", 3: ".cpp", 4: ".cpp", 
        7: ".py", 8: ".py", 11: ".cpp", 12: ".cpp", 13: ".java",
        14: ".pas", 16: ".cpp", 20: ".php", 22: ".py", 25: ".cpp",
        26: ".cpp", 27: ".cpp", 28: ".cpp", 34: ".cpp" # 34 通常是 C++17
    }
    return mapping.get(lang_id, ".txt")

def process_record(rid, html_content):
    """解析详情页 HTML 并提取源代码"""
    pattern = re.compile(r'window\._feInjection = JSON\.parse\(decodeURIComponent\("(.+?)"\)\);')
    match = pattern.search(html_content)
    if not match:
        return False
    
    try:
        data = json.loads(unquote(match.group(1)))
        # 注意：详情页的 JSON 结构与列表页不同
        record = data.get('currentData', {}).get('record', {})
        source_code = record.get('sourceCode')
        lang_id = record.get('language')
        
        if source_code:
            ext = get_extension_by_lang(lang_id)
            # 文件名：R提交号_题目名.cpp
            pid = record.get('problem', {}).get('pid', 'Unknown')
            code_filename = f"R{rid}_{pid}{ext}"
            code_path = os.path.join(CODE_DIR, code_filename)
            
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(source_code)
            return True
    except Exception as e:
        print(f"\n[Error] 解析 R{rid} 失败: {e}")
    return False

# 1. 从你的 JSON 文件读取 ID
if not os.path.exists(INPUT_FILE):
    print(f"找不到文件 {INPUT_FILE}，请先运行 get_record。")
    exit()

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    history_data = json.load(f)

# 提取所有提交 ID
ids = [item['id'] for item in history_data]
print(f"同步到本地记录: {len(ids)} 条")

# 2. 循环爬取详情
for i, rid in enumerate(ids):
    html_path = os.path.join(RECORDS_DIR, f"R{rid}.html")
    
    print(f"进度 [{i+1}/{len(ids)}] - 正在处理 R{rid}...", end='\r')

    # A: 本地缓存处理
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            process_record(rid, f.read())
        continue

    # B: 发起网络请求
    try:
        response = requests.get(f"{URL_BASE}{rid}", headers=HEADERS, cookies=COOKIES, timeout=10)
        
        if response.status_code == 200:
            html_text = response.text
            # 保存 HTML 备份
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_text)
            
            if process_record(rid, html_text):
                time.sleep(3)
            else:
                print(f"\n[Error] R{rid} 无法提取代码")
        elif response.status_code == 404:
             print(f"\n[Error] R{rid} 不存在 (404)")
        else:
            print(f"\n[Error] R{rid} 状态码: {response.status_code}")
            time.sleep(5)
            
    except Exception as e:
        print(f"\n[Error] R{rid}: {e}")
        time.sleep(5)

print("\n\n所有源代码已同步至 /code 文件夹！")
