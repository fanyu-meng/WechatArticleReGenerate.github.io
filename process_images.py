#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理 Markdown 文件，提取图片引用并复制到目标目录
"""

import os
import shutil
from pathlib import Path

# 配置路径
SOURCE_IMAGE_DIR = "/Users/fanyumeng/Documents/公众号/公众号文章导出/WeChat-Articles-Batch-Downloader/output/images"
MARKDOWN_FILE = "resources/声学发展史之——建筑声学_(Architectural_Acoustics)_20260106_184535.md"
TARGET_IMAGE_DIR = "docs/images"
OUTPUT_DIR = "docs"

# 所有图片路径（从 grep 结果中提取）
IMAGE_PATHS = [
    "Reverb.png",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_001.jpg",
    "Sabine.png",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_002.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_003.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_004.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_005.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_006.jpg",
    "IR.png",
    "Clarity_EDT_etc.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_007.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_008.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_009.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_010.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_011.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_012.jpg",
    "../images/声学发展史之——建筑声学_(Architectural_Acoustics)_037_013.jpg",
]

def normalize_image_path(image_path, markdown_dir):
    """标准化图片路径，返回绝对路径和文件名"""
    # 处理相对路径
    if image_path.startswith('../'):
        # 相对于 markdown 文件的父目录
        base_dir = os.path.dirname(os.path.dirname(markdown_dir))
        normalized = os.path.normpath(os.path.join(base_dir, image_path[3:]))  # 移除 ../
    elif image_path.startswith('./'):
        normalized = os.path.normpath(os.path.join(markdown_dir, image_path[2:]))
    else:
        # 相对于 markdown 文件所在目录
        normalized = os.path.normpath(os.path.join(markdown_dir, image_path))
    
    return normalized, os.path.basename(normalized)

def find_image_in_source(image_filename, source_dir):
    """在源图片目录中查找图片文件"""
    # 尝试精确匹配
    exact_path = os.path.join(source_dir, image_filename)
    if os.path.exists(exact_path):
        return exact_path
    
    # 尝试模糊匹配（文件名包含）
    if os.path.exists(source_dir):
        for file in os.listdir(source_dir):
            if image_filename in file or file in image_filename:
                return os.path.join(source_dir, file)
    
    return None

def copy_images():
    """复制图片到目标目录"""
    # 创建目标目录
    os.makedirs(TARGET_IMAGE_DIR, exist_ok=True)
    
    markdown_dir = os.path.dirname(MARKDOWN_FILE)
    copied_images = {}
    
    print(f"处理 {len(IMAGE_PATHS)} 个图片引用:\n")
    
    for img_path in IMAGE_PATHS:
        # 标准化路径
        abs_path, filename = normalize_image_path(img_path, markdown_dir)
        
        # 检查文件是否存在
        if os.path.exists(abs_path):
            # 文件存在，直接复制
            target_path = os.path.join(TARGET_IMAGE_DIR, filename)
            shutil.copy2(abs_path, target_path)
            copied_images[img_path] = filename
            print(f"✓ 复制: {filename}")
        else:
            # 文件不存在，尝试在源目录中查找
            found_path = find_image_in_source(filename, SOURCE_IMAGE_DIR)
            if found_path:
                target_path = os.path.join(TARGET_IMAGE_DIR, filename)
                shutil.copy2(found_path, target_path)
                copied_images[img_path] = filename
                print(f"✓ 从源目录复制: {filename}")
            else:
                print(f"✗ 未找到图片: {img_path} (查找: {filename})")
    
    # 复制HTML文件
    html_file = "Gemini- deep Research-声学概念-infographic.html"
    html_source = os.path.join(markdown_dir, html_file)
    if os.path.exists(html_source):
        html_target = os.path.join(os.path.dirname(TARGET_IMAGE_DIR), html_file)
        shutil.copy2(html_source, html_target)
        print(f"\n✓ 复制HTML文件: {html_file}")
    
    # 复制视频文件
    video_file = "Reverb.mp4"
    video_source = os.path.join(markdown_dir, video_file)
    if os.path.exists(video_source):
        video_target = os.path.join(os.path.dirname(TARGET_IMAGE_DIR), video_file)
        shutil.copy2(video_source, video_target)
        print(f"✓ 复制视频文件: {video_file}")
    
    return copied_images

if __name__ == "__main__":
    copied = copy_images()
    print(f"\n总共成功复制了 {len(copied)} 个图片文件到 {TARGET_IMAGE_DIR}")
