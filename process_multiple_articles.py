#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理多篇 Markdown 文章，生成多文章网站结构
"""

import re
import os
import shutil
import markdown
from pathlib import Path
from datetime import datetime

# 配置路径
SOURCE_IMAGE_DIR = "/Users/fanyumeng/Documents/公众号/公众号文章导出/WeChat-Articles-Batch-Downloader/output/images"
OUTPUT_DIR = "docs"
ARTICLES_DIR = os.path.join(OUTPUT_DIR, "articles")
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

# 文章配置列表
ARTICLES = [
    {
        "id": "architectural-acoustics",
        "title": "声学发展史之——建筑声学 (Architectural Acoustics)",
        "markdown_file": "resources/声学发展史之——建筑声学_(Architectural_Acoustics)_20260106_184535.md",
        "html_file": "articles/architectural-acoustics.html",
        "date": "2026-01-06",
    },
    {
        "id": "what-is-acoustics",
        "title": "什么是声学？",
        "markdown_file": "/Users/fanyumeng/Documents/公众号/公众号文章导出/WeChat-Articles-Batch-Downloader/output/markdown/什么是声学？_20260106_181628.md",
        "html_file": "articles/what-is-acoustics.html",
        "date": "2026-01-06",
    },
]

def extract_image_paths(markdown_content):
    """提取 Markdown 中的所有图片路径"""
    pattern = r'!\[[^\]]*\]\(([^\)]+)\)'
    matches = re.findall(pattern, markdown_content)
    
    image_paths = []
    for match in matches:
        path = match.split('?')[0].split('#')[0].strip().replace('\n', '').replace('\r', '')
        if path and not path.startswith('http'):
            image_paths.append(path)
    
    return list(set(image_paths))

def normalize_image_path(image_path, markdown_dir):
    """标准化图片路径，返回绝对路径和文件名"""
    if image_path.startswith('../'):
        base_dir = os.path.dirname(os.path.dirname(markdown_dir))
        normalized = os.path.normpath(os.path.join(base_dir, image_path[3:]))
    elif image_path.startswith('./'):
        normalized = os.path.normpath(os.path.join(markdown_dir, image_path[2:]))
    else:
        normalized = os.path.normpath(os.path.join(markdown_dir, image_path))
    
    return normalized, os.path.basename(normalized)

def find_image_in_source(image_filename, source_dir):
    """在源图片目录中查找图片文件"""
    exact_path = os.path.join(source_dir, image_filename)
    if os.path.exists(exact_path):
        return exact_path
    
    if os.path.exists(source_dir):
        for file in os.listdir(source_dir):
            if image_filename in file or file in image_filename:
                return os.path.join(source_dir, file)
    
    return None

def copy_article_images(markdown_file, source_image_dir, target_image_dir):
    """复制文章引用的图片到目标目录"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    image_paths = extract_image_paths(content)
    markdown_dir = os.path.dirname(markdown_file)
    copied_images = {}
    
    for img_path in image_paths:
        abs_path, filename = normalize_image_path(img_path, markdown_dir)
        
        if os.path.exists(abs_path):
            target_path = os.path.join(target_image_dir, filename)
            shutil.copy2(abs_path, target_path)
            copied_images[img_path] = filename
        else:
            found_path = find_image_in_source(filename, source_image_dir)
            if found_path:
                target_path = os.path.join(target_image_dir, filename)
                shutil.copy2(found_path, target_path)
                copied_images[img_path] = filename
    
    return copied_images

def update_image_paths_in_content(content, image_mapping):
    """更新内容中的图片路径（文章在 articles/ 目录，图片在 images/ 目录）"""
    for old_path, new_path in image_mapping.items():
        pattern = r'(\!\[.*?\]\()' + re.escape(old_path) + r'(\))'
        content = re.sub(pattern, r'\1../images/' + new_path + r'\2', content)
    return content

def create_article_html(markdown_content, article_info):
    """创建文章 HTML 页面"""
    # 使用 markdown 库转换
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables'])
    html_content = md.convert(markdown_content)
    
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .back-link {{
            margin-bottom: 20px;
        }}
        
        .back-link a {{
            color: #3498db;
            text-decoration: none;
            font-size: 0.9em;
        }}
        
        .back-link a:hover {{
            text-decoration: underline;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 0.5em;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            font-size: 2em;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 0.2em;
        }}
        
        h3 {{
            font-size: 1.5em;
            margin-top: 1.2em;
            margin-bottom: 0.4em;
            color: #34495e;
        }}
        
        h4 {{
            font-size: 1.2em;
            margin-top: 1em;
            margin-bottom: 0.3em;
            color: #34495e;
        }}
        
        p {{
            margin-bottom: 1em;
            text-align: justify;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        video {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 20px 0;
            color: #555;
            font-style: italic;
            background-color: #f8f9fa;
            padding: 15px 20px;
            border-radius: 4px;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 1em;
        }}
        
        li {{
            margin-bottom: 0.5em;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        strong {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        em {{
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            h2 {{
                font-size: 1.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="back-link">
            <a href="../index.html">← 返回首页</a>
        </div>
        {content}
    </div>
</body>
</html>"""
    
    return html_template.format(title=article_info['title'], content=html_content)

def process_article(article_config):
    """处理单篇文章"""
    print(f"\n处理文章: {article_config['title']}")
    print(f"  Markdown: {article_config['markdown_file']}")
    
    # 读取 Markdown 文件
    with open(article_config['markdown_file'], 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 复制图片
    copied_images = copy_article_images(
        article_config['markdown_file'],
        SOURCE_IMAGE_DIR,
        IMAGES_DIR
    )
    print(f"  复制了 {len(copied_images)} 个图片文件")
    
    # 更新图片路径
    markdown_content = update_image_paths_in_content(markdown_content, copied_images)
    
    # 处理HTML文件链接和视频链接
    # 更新HTML文件链接（如 infographic.html）
    html_link_pattern = r'(\[.*?\]\()Gemini-%20deep%20Research-声学概念-infographic\.html(\))'
    markdown_content = re.sub(html_link_pattern, r'\1../Gemini- deep Research-声学概念-infographic.html\2', markdown_content)
    
    # 更新视频链接路径
    video_pattern = r'(\[.*?\]\()Reverb\.mp4(\))'
    markdown_content = re.sub(video_pattern, r'\1../Reverb.mp4\2', markdown_content)
    
    # 生成 HTML
    html_content = create_article_html(markdown_content, article_config)
    
    # 保存 HTML 文件
    html_path = os.path.join(OUTPUT_DIR, article_config['html_file'])
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  生成 HTML: {html_path}")
    
    return article_config

def create_landing_page(articles):
    """创建 Landing Page"""
    articles_html = ""
    for article in articles:
        articles_html += f"""
        <div class="article-card">
            <h2><a href="{article['html_file']}">{article['title']}</a></h2>
            <p class="article-date">发布时间: {article['date']}</p>
        </div>
        """
    
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>声学科普文章集</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 0.5em;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
            text-align: center;
        }}
        
        .intro {{
            text-align: center;
            color: #555;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}
        
        .articles-list {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .article-card {{
            border: 1px solid #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            transition: box-shadow 0.3s;
        }}
        
        .article-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .article-card h2 {{
            margin: 0 0 10px 0;
            border: none;
            padding: 0;
        }}
        
        .article-card h2 a {{
            color: #2c3e50;
            text-decoration: none;
        }}
        
        .article-card h2 a:hover {{
            color: #3498db;
        }}
        
        .article-date {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin: 0;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>声学科普文章集</h1>
        <p class="intro">欢迎来到声学科普文章集，这里收集了关于声学的精彩文章。</p>
        <div class="articles-list">
            {articles_html}
        </div>
    </div>
</body>
</html>"""
    
    html_content = html_template.format(articles_html=articles_html)
    
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ Landing Page 已生成: {index_path}")

def main():
    """主函数"""
    # 创建目录
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # 处理所有文章
    processed_articles = []
    for article_config in ARTICLES:
        try:
            processed_article = process_article(article_config)
            processed_articles.append(processed_article)
        except Exception as e:
            print(f"✗ 处理文章失败: {article_config['title']}")
            print(f"  错误: {e}")
    
    # 创建 Landing Page
    create_landing_page(processed_articles)
    
    print(f"\n✓ 处理完成！共处理 {len(processed_articles)} 篇文章")

if __name__ == "__main__":
    main()
