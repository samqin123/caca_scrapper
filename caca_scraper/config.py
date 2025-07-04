# -*- coding: utf-8 -*-

"""
配置模块
"""

# 基础URL
BASE_URL = 'https://ask.cacakp.com'

# 搜索页面URL模板
# disease_id: 疾病ID, 8代表胰腺癌
# page_number: 页面数
SEARCH_URL_TEMPLATE = '/question/search?disease_id={disease_id}&order=post_time&page={page_number}'

# 请求头，模拟浏览器
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

import json
import os

def get_disease_list():
    """
    从 cancer_code.json 文件中加载病种列表。

    Returns:
        list: 包含 (病种名称, 病种ID) 元组的列表。
    """
    disease_list = []
    # JSON 文件位于项目根目录的上一级
    file_path = '/Users/qinxiaoqiang/Downloads/肿瘤QA CACA科普/cancer_code.json'
    if not os.path.exists(file_path):
        print(f"错误：病种列表文件不存在于路径 {file_path}")
        return disease_list

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            disease_data = json.load(f)
            # 将 {id: name} 格式转换为 [(name, id)] 格式
            for disease_id, disease_name in disease_data.items():
                disease_list.append((disease_name, disease_id))
    except json.JSONDecodeError:
        print(f"错误：无法解析JSON文件 {file_path}")
    except Exception as e:
        print(f"加载病种列表文件时出错: {e}")
    return disease_list