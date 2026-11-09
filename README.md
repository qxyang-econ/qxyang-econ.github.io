# Qingxu Yang — 学术个人主页

这是当前网站第 3 版的完整可维护源码，已整理为可直接上传到 GitHub 的结构。内容包含 Home、Research、Teaching、CV 四页、样式和图标；CV 下载暂为停用的占位链接，不包含 PDF 文件。网站使用静态 HTML/CSS；Abstract 采用浏览器原生展开功能，没有服务器、数据库或运行时依赖。Python 3 只用于修改内容后重新生成页面，不需要安装第三方包。

## 第一次发布到 GitHub Pages

1. 登录 GitHub，创建名为 `你的用户名.github.io` 的仓库。这里必须使用你实际的 GitHub 用户名。例如用户名为 `example`，仓库名就是 `example.github.io`。建议选择 Public；GitHub Free 可以用公开仓库启用 Pages。如果已有同名仓库，应先查看其现有内容，避免覆盖已有网站。
2. 解压本压缩包。进入 `Qingxu_Yang_website_source` 文件夹，将其中的文件和 `docs` 文件夹上传到仓库根目录，保留文件夹结构。仓库顶层应能直接看到 `generate.py`、`content.json`、`site_config.json`、`README.md` 和 `docs`。不要仅上传 ZIP，也不要多套一层外部文件夹。
3. 网页上传可使用仓库中的 `Add file → Upload files`，拖入文件及文件夹后点击 `Commit changes`。也可以用 GitHub Desktop 上传整个项目。这里已包含生成好的页面，第一次上线无须先运行 Python。
4. 打开仓库 `Settings → Pages`。
5. 在 `Build and deployment` 中，把 `Source` 设为 `Deploy from a branch`，`Branch` 选 `main`，文件夹选 `/docs`，点击 `Save`。
6. 等待发布完成，再通过 Pages 页面里的 `Visit site` 打开网站。默认地址为 `https://你的用户名.github.io/`。GitHub 官方说明更新可能需要最多约 10 分钟。

GitHub 仓库保存源码和版本历史，GitHub Pages 负责对外提供网页。按上述 Public 仓库方式发布后，网站和源码均可公开访问，访问者不需要 ChatGPT 登录。原来的 ChatGPT Site 与 GitHub Pages 是两个独立部署，修改一个不会自动同步另一个。

## 平时修改什么文件

| 要修改的内容 | 文件及位置 |
| --- | --- |
| 论文标题、作者、顺序、Abstract、论文链接 | `content.json`；分别位于 `working_papers`、`publications`、`work_in_progress` 数组 |
| 首页个人介绍 | `generate.py` 的 `bio` 变量 |
| Teaching 页面 | `generate.py` 的 `teaching` 变量 |
| CV 页的下载链接 | `generate.py` 的 `cv` 变量 |
| 侧栏、邮箱、导航等共用内容 | `generate.py` 的 `render()` 函数 |
| 页面配色、字体、间距、布局 | `docs/style.css` |
| 今后启用 CV 下载 | 将 PDF 放入 `docs/files/Qingxu_Yang_CV.pdf`，并在 `generate.py` 中恢复 CV 页和侧栏的下载链接，再重新生成页面 |
| 页脚的更新时间 | `content.json` 的 `updated` 字段 |
| 正式网站地址 | `site_config.json` 的 `site_url` 字段 |

`content.json` 中每组论文的排列顺序就是网页上的顺序。期刊文章可用 `language: "in Chinese"` 标注语言。直接修改 JSON 时保持英文双引号和逗号格式正确。

在项目文件夹打开终端，修改内容后运行：

```bash
python3 generate.py
```

Windows 如果 `python3` 不可用，可使用 `py generate.py` 或 `python generate.py`。请使用 UTF-8 编码保存文件。

该命令生成 `docs` 内的四个 HTML 页面。不要只修改 `docs` 内生成的 HTML 后再运行脚本，因为重新生成会覆盖这些 HTML；日常维护应修改上表对应的源文件。

将修改的源文件和重新生成的 `docs` 文件一起提交到 GitHub，Pages 会自动更新。仅在 GitHub 网页上修改 `content.json` 不会自动运行 Python；当前配置需要在本地生成并提交 HTML。修改 CSS 时无需重新运行生成脚本。

## 本地预览

直接双击 `docs/index.html` 即可查看。也可在项目文件夹运行：

```bash
python3 -m http.server 8000 --directory docs
```

然后访问 `http://localhost:8000/`。按 Ctrl+C 停止预览。

## 正式地址与自定义域名

确定 GitHub Pages 地址后，把 `site_config.json` 改为：

```json
{
  "site_url": "https://qxyang-econ.github.io"
}
```

再运行生成命令并提交更新。这会设置搜索引擎使用的 canonical 地址和个人结构化数据中的网址。此版本已填写 `https://qxyang-econ.github.io`，页面已按该正式地址生成。

如果以后使用自定义域名，先按 GitHub 文档配置 Pages 的域名及 DNS，再把 `site_url` 更新为实际正式地址并重新生成网页。

## 此导出版本的范围

基于 2026 年 11 月 4 日网站第 3 版导出，包含两条研究主线介绍、仅一行下载链接的 CV 页，以及仅显示标题与合作者的在研论文列表；工作论文与已发表论文保留 Abstract。为方便 GitHub Pages 的分支发布，原来 `dist` 中的文件改放到 `docs`；页面内容、布局和论文链接均保留。按最新要求，CV 文件不发布，所有 Download CV 链接暂时停用。此包没有包含原托管平台的内部配置或 Git 历史。

当前包没有 GitHub Actions 自动生成脚本。以上分支发布流程适用于简单维护，无需配置 Actions 权限。如果以后希望只改 JSON 就自动上线，可以另行添加自动构建流程。

## 官方参考

- GitHub Pages 入门：https://docs.github.com/en/pages/quickstart
- 配置发布分支与目录：https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub 网页上传文件：https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

