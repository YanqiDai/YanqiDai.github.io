# Yanqi Dai's Homepage

这是一个由 GitHub Pages / Jekyll 渲染的个人主页。

- **唯一的内容数据文件：** `_data/homepage.yml`
- **页面模板：** `index.html`
- **发布方式：** 推送到 GitHub 后，由 GitHub Pages 自动读取 YAML 并生成网页
- **不再需要：** 手动运行主页生成脚本，也不需要同时维护两份 About Me

## 修改主页内容

日常更新只需编辑 `_data/homepage.yml`。姓名、邮箱、简介、论文、经历、奖项、博客入口和图片路径等信息都集中在这里：

```yaml
profile:
  name: "Yanqi Dai"
  email: "yanqidai@ruc.edu.cn"

papers:
  items:
    # ...

experience:
  items:
    # ...

awards:
  items:
    # ...

blogs:
  items:
    # ...
```

`index.html` 中只保留页面结构、样式、JavaScript 和 Liquid 渲染逻辑。通常无需为了修改内容而编辑它。

### 个人信息

在 `profile` 分区中修改：

- `site_url`：主页网址，不要在结尾添加 `/`
- `name`、`name_zh`：英文名和中文名
- `initials`：导航栏中的姓名缩写
- `email`：联系邮箱
- `description`：搜索引擎和分享卡片使用的简介
- `image`：头像路径
- `background_image`：桌面端背景图片路径
- `background_image_mobile`：移动端背景图片路径
- `footer_year`：页脚年份
- `hero_intro`：首页顶部简介
- `role`、`affiliation`：当前身份和单位
- `research_chips`：头像周围展示的研究方向
- `about`：About Me 文案和研究方向图
- `social_links`：Google Scholar、GitHub 等外部链接

`research_chips`、`about.map_nodes`、论文、经历、奖项、博客和社交链接都支持增删条目，不需要同步修改 HTML。

`hero_intro` 和 `about.paragraphs` 中可以使用简单 HTML，例如：

```yaml
hero_intro: >-
  I am interested in <strong>large multimodal models</strong>.
```

### 论文

在 `papers.items` 中增加、删除或调整顺序：

```yaml
- venue: "ICLR 2026"
  short_name: "Paper Name"
  title: "Full Paper Title"
  authors: "Author A, Author B, Author C*"
  highlight: "Optional highlight text"
  links:
    - label: "Paper"
      url: "https://example.com/paper"
    - label: "Code"
      url: "https://github.com/example/repository"
```

`highlight` 和不需要的链接可以直接省略。

### 实习或工作经历

在 `experience.items` 中填写：

```yaml
- period: "May 2026 — Present"
  location: "Beijing"
  role: "Algorithm Intern"
  team: "VLM Pretraining Team"
  organization: "Company Name"
```

### 荣誉与奖项

在 `awards.items` 中填写：

```yaml
- title: "Award Name"
  organization: "University or Organization"
  year: "2026"
```

没有颁发单位时可以省略 `organization`。

### 博客

在 `blogs.items` 中增加、删除或调整顺序：

```yaml
- title: "Blog title"
  date: "2026-08-16"
  description: "A short introduction shown on the homepage."
  url: "blogs/leetcode-hot100/index.html"
  cta: "Read the blog"
```

`date` 使用带引号的 `YYYY-MM-DD` 格式，并会显示在主页博客卡片中。博客仍按 YAML 中的顺序展示，不会自动按日期排序。

## 更换图片

当前头像和背景图分别位于：

- `images/yanqidai.jpg`
- `images/mountain-background.jpg`
- `images/mountain-background-mobile.jpg`

可以覆盖现有文件，也可以添加新文件后修改 `_data/homepage.yml` 中相应路径。桌面端和移动端建议分别使用横向、竖向且经过压缩的 JPEG 图片。

## 本地预览

因为 `index.html` 包含 Liquid，直接双击文件不会解析 YAML。安装了 Jekyll 时，在仓库根目录运行：

```bash
jekyll serve
```

然后访问：

```text
http://127.0.0.1:4000
```

保存 `_data/homepage.yml` 或 `index.html` 后，Jekyll 会自动重新生成页面。停止预览时按 `Ctrl+C`。

## 发布到 GitHub Pages

修改完成后提交并推送：

```bash
git add _data/homepage.yml index.html README.md images/ blogs/
git commit -m "Update homepage"
git push
```

推送会触发 GitHub Pages 构建。构建时，Jekyll 自动加载 `_data/homepage.yml`，将数据传给 `index.html` 中的 Liquid 模板，再输出最终静态网页；不需要手动运行生成脚本。

## YAML 编辑注意事项

- 使用空格缩进，不要使用 Tab。
- 同一层级保持相同缩进；本项目使用两个空格。
- 列表中的每一项以 `-` 开头。
- 建议用双引号包裹文本，尤其是包含 `:`、`#` 或特殊符号的内容。
- 日期建议保留为带引号的字符串。
