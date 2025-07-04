# -*- coding: utf-8 -*-

"""
文件处理模块
"""

import logging
import os

def save_to_markdown(qa_list, filename):
    """
    将问答列表保存到Markdown文件中。

    Args:
        qa_list (list): 包含问答字典的列表。
        filename (str): 要保存的文件名。
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for qa in qa_list:
                question = qa.get('question', '无问题')
                answer = qa.get('answer', '无答案')

                # 写入Markdown格式的Q&A
                f.write(f"## Q: {question}\n\n")
                f.write(f"**A:**\n{answer}\n\n")
                f.write("---\n\n")
        logging.info(f"数据已成功保存到 {filename}")
    except IOError as e:
        logging.error(f"保存文件 {filename} 失败: {e}")


def save_links_to_markdown(detail_info, filename, disease_name):
    """
    将标题和链接列表保存到Markdown文件中。

    Args:
        detail_info (list): 包含 (标题, 链接) 元组的列表。
        filename (str): 要保存的文件名。
        disease_name (str): 病种名称。
    """
    try:
        # 从主输出文件名派生出链接文件名
        base, ext = os.path.splitext(filename)
        links_filename = f"{base}_url{ext}"

        with open(links_filename, 'w', encoding='utf-8') as f:
            f.write(f"# CACA科普网【{disease_name}】问答链接列表\n\n")
            for title, url in detail_info:
                f.write(f"- [{title}]({url})\n")
        logging.info(f"链接列表已成功保存到 {links_filename}")
    except IOError as e:
        logging.error(f"保存链接文件 {links_filename} 失败: {e}")