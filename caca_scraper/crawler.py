# -*- coding: utf-8 -*-

"""
爬虫核心模块
"""

import requests
from bs4 import BeautifulSoup
import time
import logging

# 从配置模块导入配置
from config import BASE_URL, SEARCH_URL_TEMPLATE, HEADERS

def get_detail_urls(disease_id, disease_name):
    """
    获取指定病种的所有问题详情页的标题和URL链接。

    通过循环翻页，从指定病种的搜索结果列表中提取所有问题的标题和链接。

    Args:
        disease_id (str): 病种ID。
        disease_name (str): 病种名称。

    Returns:
        list: 包含 (标题, 链接) 元组的列表。
    """
    detail_info = [] # 用于存储 (标题, 链接) 元组
    page_number = 1
    while True:
        # 拼接搜索URL
        search_url = SEARCH_URL_TEMPLATE.format(disease_id=disease_id, page_number=page_number)
        full_search_url = f"{BASE_URL}{search_url}"
        logging.info(f"正在为【{disease_name}】抓取列表页面: {full_search_url}")

        try:
            response = requests.get(full_search_url, headers=HEADERS)
            response.raise_for_status()  # 如果请求失败则抛出异常

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找当前页面的所有问题链接
            # 根据`检索页面源码.md`，链接在`div.particular`下的`a.headline_link`标签中
            question_links = soup.select('div.particular a.headline_link')

            if not question_links:
                # 如果页面上没有找到任何链接，说明已经到了最后一页
                logging.info(f"【{disease_name}】未找到更多问题链接，列表抓取完成。")
                break

            for link in question_links:
                href = link.get('href')
                title = link.get_text(strip=True)
                if href:
                    full_detail_url = f"{BASE_URL}{href}"
                    # 检查是否已存在，避免重复
                    if not any(info[1] == full_detail_url for info in detail_info):
                        detail_info.append((title, full_detail_url))
            
            # 模拟人类行为，随机暂停一段时间
            time.sleep(1)
            page_number += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"抓取列表页面 {full_search_url} 失败: {e}")
            break # 如果发生网络错误，则停止抓取

    logging.info(f"为【{disease_name}】共找到 {len(detail_info)} 个不重复的问题链接。")
    return detail_info

def get_qa_content(url):
    """
    从问题详情页提取问题标题和答案内容。

    Args:
        url (str): 问题详情页的URL。

    Returns:
        dict: 包含'question'和'answer'的字典，如果提取失败则返回None。
    """
    logging.info(f"正在抓取详情页面: {url}")
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取问题标题
        # 根据`需求.md`，标题在`div.issue h3`中
        question_tag = soup.select_one('div.issue h3')
        question = question_tag.get_text(strip=True) if question_tag else "未找到标题"

        # 提取答案内容
        # 根据`需求.md`，答案在`div.details`中
        answer_tag = soup.select_one('div.details')
        if answer_tag:
            # 提取所有p标签的文本并合并
            paragraphs = answer_tag.find_all('p')
            answer = '\n'.join(p.get_text(strip=True) for p in paragraphs)
        else:
            answer = "未找到答案"
        
        # 模拟人类行为，随机暂停一段时间
        time.sleep(1)

        return {"question": question, "answer": answer}

    except requests.exceptions.RequestException as e:
        logging.error(f"抓取详情页面 {url} 失败: {e}")
    except Exception as e:
        logging.error(f"解析页面 {url} 时发生错误: {e}")
    
    return None