# 声学发展史之——建筑声学

这是一个从 Markdown 转换为静态网页的项目，可直接部署到 GitHub Pages。

## 项目结构

```
.
├── docs/                    # GitHub Pages 部署目录
│   ├── index.html          # 主页面
│   └── images/             # 图片资源目录
│       └── ...            # 所有文章图片
├── resources/              # 原始资源文件
│   └── 声学发展史之——建筑声学_(Architectural_Acoustics)_20260106_184535.md
└── README.md              # 本文件
```

## GitHub Pages 部署步骤

### 方法 1: 使用 docs 目录（推荐）

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: 声学发展史文章"
   git push origin main
   ```

2. **配置 GitHub Pages**
   - 进入仓库的 Settings
   - 找到 Pages 设置
   - Source 选择 "Deploy from a branch"
   - Branch 选择 `main`，文件夹选择 `/docs`
   - 点击 Save

3. **访问网站**
   - 几分钟后，网站将在 `https://[你的用户名].github.io/WechatArticleReGenerate.github.io/` 可用

### 方法 2: 使用根目录

如果你想使用根目录部署，可以：

1. 将 `docs` 目录下的所有文件移动到根目录
2. 在 Settings > Pages 中选择 "Deploy from a branch"，文件夹选择 `/ (root)`

## 本地预览

你可以使用 Python 的简单 HTTP 服务器预览：

```bash
cd docs
python3 -m http.server 8000
```

然后在浏览器中访问 `http://localhost:8000`

## 更新内容

如果需要更新文章内容：

1. 修改 `resources/` 目录下的 Markdown 文件
2. 运行处理脚本：
   ```bash
   python3 process_images.py      # 复制图片
   source venv/bin/activate
   python3 markdown_to_html_v2.py  # 生成 HTML
   ```
3. 提交并推送更改

## 技术说明

- **Markdown 转换**: 使用 Python `markdown` 库进行转换
- **图片处理**: 自动从源目录复制被引用的图片
- **样式**: 内置响应式 CSS，适配移动端和桌面端
- **静态部署**: 纯静态 HTML/CSS/图片，无需后端服务

## 注意事项

- 确保所有图片路径在 HTML 中都是相对路径
- 图片文件名包含中文字符，确保 Git 配置正确处理 UTF-8
- GitHub Pages 支持中文文件名，无需特殊配置
