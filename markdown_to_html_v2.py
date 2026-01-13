#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 markdown 库将 Markdown 转换为 HTML，并更新图片路径
"""

import re
import os
import markdown

MARKDOWN_FILE = "resources/声学发展史之——建筑声学_(Architectural_Acoustics)_20260106_184535.md"
OUTPUT_HTML = "docs/index.html"

# 图片路径映射：原始路径 -> 新路径
IMAGE_PATH_MAPPING = {
    "Reverb.png": "images/Reverb.png",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_001.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_001.jpg",
    "Sabine.png": "images/Sabine.png",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_002.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_002.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_003.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_003.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_004.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_004.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_005.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_005.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_006.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_006.jpg",
    "IR.png": "images/IR.png",
    "Clarity_EDT_etc.jpg": "images/Clarity_EDT_etc.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_007.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_007.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_008.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_008.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_009.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_009.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_010.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_010.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_011.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_011.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_012.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_012.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_013.jpg": "images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_013.jpg",
}

# HTML文件链接路径映射：原始路径 -> 新路径
HTML_LINK_MAPPING = {
    "Gemini-%20deep%20Research-声学概念-infographic.html": "Gemini- deep Research-声学概念-infographic.html",
}

# 视频文件路径映射：原始路径 -> 新路径
VIDEO_PATH_MAPPING = {
    "Reverb.mp4": "Reverb.mp4",
}

def update_image_paths(content):
    """更新 Markdown 内容中的图片路径、HTML链接路径和视频路径"""
    # 更新图片路径
    for old_path, new_path in IMAGE_PATH_MAPPING.items():
        # 替换图片引用
        pattern = r'(\!\[.*?\]\()' + re.escape(old_path) + r'(\))'
        content = re.sub(pattern, r'\1' + new_path + r'\2', content)
    
    # 更新HTML文件链接路径
    for old_path, new_path in HTML_LINK_MAPPING.items():
        # 替换链接引用（处理URL编码和普通路径）
        # 匹配 [text](path) 格式
        pattern = r'(\[.*?\]\()' + re.escape(old_path) + r'(\))'
        content = re.sub(pattern, r'\1' + new_path + r'\2', content)
    
    # 更新视频文件链接路径（在 Markdown 链接中）
    for old_path, new_path in VIDEO_PATH_MAPPING.items():
        # 替换链接引用中的视频路径 [text](path) 格式
        pattern = r'(\[.*?\]\()' + re.escape(old_path) + r'(\))'
        content = re.sub(pattern, r'\1' + new_path + r'\2', content)
        # 也处理 <video> 标签中的路径（如果有）
        pattern = r'(<source\s+src=")' + re.escape(old_path) + r'(")'
        content = re.sub(pattern, r'\1' + new_path + r'\2', content)
    
    return content

def create_html_page(content):
    """创建完整的 HTML 页面"""
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>声学发展史之——建筑声学 (Architectural Acoustics)</title>
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
        {content}
    </div>
</body>
</html>"""
    
    return html_template.format(content=content)

def main():
    # 读取 Markdown 文件
    with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 更新图片路径
    markdown_content = update_image_paths(markdown_content)
    
    # 使用 markdown 库转换为 HTML
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables'])
    html_content = md.convert(markdown_content)
    
    # 创建完整 HTML 页面
    full_html = create_html_page(html_content)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    
    # 写入 HTML 文件
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ HTML 文件已生成: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
