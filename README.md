# 声学科普文章集

这是一个多文章静态网站，使用 GitHub Pages 部署。

## 项目结构

```
docs/
├── index.html                    # Landing Page（首页）
├── .nojekyll                    # GitHub Pages 配置
├── articles/                     # 文章页面目录
│   ├── architectural-acoustics.html
│   └── what-is-acoustics.html
├── images/                       # 所有图片资源（共享）
│   └── ...
├── Gemini- deep Research-声学概念-infographic.html  # 信息图表页面
└── Reverb.mp4                    # 视频文件
```

## 添加新文章

### 方法 1: 使用脚本自动处理（推荐）

1. **编辑 `process_multiple_articles.py`**，在 `ARTICLES` 列表中添加新文章配置：

```python
ARTICLES = [
    # ... 现有文章 ...
    {
        "id": "new-article-id",           # 唯一标识符（英文）
        "title": "新文章标题",             # 显示标题
        "markdown_file": "path/to/article.md",  # Markdown 文件路径
        "html_file": "articles/new-article-id.html",  # 输出 HTML 路径
        "date": "2026-01-13",            # 发布日期
    },
]
```

2. **运行处理脚本**：

```bash
source venv/bin/activate
python3 process_multiple_articles.py
```

脚本会自动：
- 提取文章引用的所有图片
- 从源目录复制图片到 `docs/images/`
- 更新图片路径为相对路径
- 生成 HTML 页面
- 更新 Landing Page

### 方法 2: 手动处理

1. 将 Markdown 文件复制到 `resources/` 目录
2. 手动提取图片并复制到 `docs/images/`
3. 使用 `markdown_to_html_v2.py` 转换单个文件
4. 手动更新 `docs/index.html` 添加文章链接

## 部署到 GitHub Pages

1. **提交更改**：

```bash
git add docs/
git commit -m "Add: 新文章"
git push origin main
```

2. **配置 GitHub Pages**：
   - 进入仓库 Settings > Pages
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/docs`
   - 保存设置

3. **访问网站**：
   - 几分钟后访问：`https://[你的用户名].github.io/WechatArticleReGenerate.github.io/`

## 本地预览

```bash
cd docs
python3 -m http.server 8000
# 访问 http://localhost:8000
```

## 文章配置说明

每篇文章需要以下配置：

- **id**: 唯一标识符，用于文件名和 URL（建议使用英文和连字符）
- **title**: 文章标题，显示在 Landing Page 和页面标题中
- **markdown_file**: Markdown 文件的路径（可以是绝对路径或相对路径）
- **html_file**: 生成的 HTML 文件路径（相对于 `docs/` 目录）
- **date**: 发布日期（格式：YYYY-MM-DD）

## 图片处理

- 所有文章的图片统一存放在 `docs/images/` 目录
- 图片文件名保持原样（可能包含中文字符）
- 文章页面使用相对路径 `../images/文件名` 引用图片
- 脚本会自动去重，相同文件名的图片只复制一次

## 注意事项

1. **图片路径**: 确保 Markdown 中的图片路径能被脚本正确识别
2. **文件编码**: 所有文件使用 UTF-8 编码
3. **文件名**: 支持中文文件名，GitHub Pages 可以正常处理
4. **资源文件**: HTML 文件、视频文件等需要手动复制到 `docs/` 目录

## 技术栈

- **Markdown 转换**: Python `markdown` 库
- **样式**: 纯 CSS，响应式设计
- **部署**: GitHub Pages（纯静态）

## 更新日志

- 2026-01-13: 初始版本，支持多文章结构
- 2026-01-13: 添加"什么是声学？"文章
