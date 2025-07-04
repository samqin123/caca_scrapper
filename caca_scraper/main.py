# -*- coding: utf-8 -*-

"""
主程序入口
"""

import logging
import os
import re
from crawler import get_detail_urls, get_qa_content
from file_handler import save_to_markdown, save_links_to_markdown
from config import get_disease_list

def get_crawled_list(directory="."):
    """获取已爬取的病种列表"""
    crawled_list = set()
    if not os.path.isdir(directory):
        logging.error(f"指定的目录不存在: {directory}")
        return crawled_list

    for filename in os.listdir(directory):
        if filename.startswith('caca_') and filename.endswith('_qa.md'):
            match = re.search(r'caca_(.*?)_qa\.md', filename)
            if match:
                crawled_list.add(match.group(1))
    return crawled_list

def main():
    """
    爬虫主函数
    """
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("开始分类爬取CACA科普网所有问答...")

    # 1. 获取病种列表
    disease_list = get_disease_list()
    if not disease_list:
        logging.error("未能获取到病种列表，程序退出。")
        return

    crawled_diseases = get_crawled_list("caca_scraper")
    logging.info(f"检测到已爬取 {len(crawled_diseases)} 个病种: {crawled_diseases}")

    total_articles_crawled = 0
    newly_crawled_count = 0

    # 2. 遍历所有病种进行爬取
    for disease_name, disease_id in disease_list:
        safe_disease_name = re.sub(r'[\/:]', '_', disease_name)
        if safe_disease_name in crawled_diseases:
            logging.info(f"【{disease_name}】已存在，跳过。")
            continue

        logging.info(f"========== 开始处理病种: {disease_name} (ID: {disease_id}) ==========")
        newly_crawled_count += 1

        # 3. 为当前病种获取所有详情页的标题和链接
        detail_info = get_detail_urls(disease_id, disease_name)

        if not detail_info:
            logging.warning(f"【{disease_name}】未能获取到任何详情页链接，跳过此病种。")
            continue

        # 4. 遍历链接，获取Q&A内容
        qa_data = []
        for _, url in detail_info: # 标题在这里暂时不用
            qa = get_qa_content(url)
            if qa:
                qa_data.append(qa)
        
        if not qa_data:
            logging.warning(f"【{disease_name}】未能获取到任何问答数据，跳过此病种。")
            continue

        # 5. 根据病种名称生成文件名 (例如: caca_肺癌_qa.md)
        # 使用正则表达式移除或替换不适合做文件名的字符
        safe_disease_name = re.sub(r'[\/:]', '_', disease_name)
        output_filename_qa = f"caca_{safe_disease_name}_qa.md"

        # 6. 保存Q&A到Markdown文件
        save_to_markdown(qa_data, output_filename_qa)

        # 7. 保存链接到Markdown文件 (文件名将由 save_links_to_markdown 内部生成)
        save_links_to_markdown(detail_info, output_filename_qa, disease_name)

        articles_count = len(qa_data)
        total_articles_crawled += articles_count
        logging.info(f"【{disease_name}】处理完成！共抓取并保存了 {articles_count} 篇文章。")

    logging.info(f"\n========== 所有任务完成！总共抓取了 {newly_crawled_count} 个新病种，合计 {total_articles_crawled} 篇文章。 ==========")

if __name__ == '__main__':
    main()