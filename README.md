# Yanqi Dai's Homepage

根目录的 `index.html` 是已经生成好的静态主页，可以直接双击打开，也可以由 GitHub Pages 原样发布。姓名、邮箱、简介、论文、实习经历、获奖信息和博客入口等可编辑内容集中在 `_source/homepage.liquid` 文件最前面的变量区中。

## 修改主页内容

打开 `_source/homepage.liquid`，找到文件顶部由两行 `---` 包围的 `EDITABLE CONTENT` 区域：

```yaml
---
# EDITABLE CONTENT

profile:
  name: "Yanqi Dai"
  email: "yanqidai@ruc.edu.cn"

papers:
  # ...

experience:
  # ...

awards:
  # ...

blogs:
  # ...
---
```

通常只需修改这个区域，不需要修改后面的 HTML、CSS 或 JavaScript。根目录 `index.html` 是生成文件，不要直接编辑，否则下次生成时会被覆盖。

## 生成并本地预览

修改模板后，在仓库根目录运行：

```bash
ruby scripts/build_homepage.rb
```

脚本只使用 macOS 自带的 Ruby 标准库，不需要安装 Jekyll、Liquid 或其他依赖。生成完成后可以直接双击 `index.html`，也可以运行：

```bash
open index.html
```

### 个人信息

在 `profile` 分区中修改：

- `site_url`：主页网址，不要在结尾添加 `/`
- `name`、`name_zh`：英文名和中文名
- `initials`：导航栏中的姓名缩写
- `email`：联系邮箱
- `description`：搜索引擎和分享卡片使用的简介
- `image`：头像路径
- `background_image`：页面背景图片路径
- `background_image_mobile`：移动端背景图片路径
- `footer_year`：页脚年份
- `hero_intro`：首页顶部简介
- `role`、`affiliation`：当前身份和单位
- `research_chips`：头像周围展示的研究方向
- `about`：详细自我介绍和研究方向图
- `social_links`：Google Scholar、GitHub 等外部链接

`research_chips` 和 `about.map_nodes` 都支持可变数量。前者会自动分布在头像左右两侧，后者会围绕中央研究主题排列；增加条目时，间距和卡片大小会自动调整，使布局逐渐变得更密集。

`hero_intro` 和 `about.paragraphs` 中可以使用简单 HTML，例如：

```yaml
hero_intro: >-
  I am interested in <strong>large multimodal models</strong>.
```

### 论文

在 `papers.items` 中增加、删除或调整论文顺序。每篇论文的格式如下：

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

不需要强调信息时，可以省略 `highlight`。不需要的链接也可以直接删除。

### 实习或工作经历

在 `experience.items` 中填写：

```yaml
- period: "May 2026 — Present"
  location: "Beijing"
  role: "Algorithm Intern"
  team: "VLM Pretraining Team"
  organization: "Company Name"
```

页面会按照文件中的顺序展示经历。

论文、经历、奖项、博客和社交链接同样支持任意数量。增加条目后，页面会自动增加卡片、行或网格，不需要修改 HTML 模板。

### 荣誉与奖项

在 `awards.items` 中填写：

```yaml
- title: "Award Name"
  organization: "University or Organization"
  year: "2026"
```

如果奖项没有颁发单位，可以省略 `organization`。

### 博客

在 `blogs.items` 中增加、删除或调整博客顺序。每张卡片的格式如下：

```yaml
- title: "Blog title"
  date: "2026-08-16"
  description: "A short introduction shown on the homepage."
  url: "blogs/leetcode-hot100/index.html"
  cta: "Read the blog"
```

`date` 是博客发布日期，使用并保留引号包裹的 `YYYY-MM-DD` 格式；该日期会显示在主页博客卡片中。博客仍按照 `blogs.items` 中的顺序展示，不会根据日期自动排序。

`url` 填写相对于主页的文件路径，例如 `blogs/leetcode-hot100/index.html`。每篇博客放在 `blogs/` 下独立的文件夹中，便于后续继续添加和管理；博客卡片整张都可以点击。显式写出 `index.html` 可以同时兼容本地双击打开和 GitHub Pages。

### 更换头像

当前头像位于 `images/yanqidai.jpg`。有两种更换方式：

1. 用新图片覆盖该文件，并保持文件名不变。
2. 将新图片放入 `images` 目录，然后修改 `profile.image`，例如：

```yaml
image: "images/new-profile.jpg"
```

### 更换背景图

桌面背景位于 `images/mountain-background.jpg`，移动端背景位于 `images/mountain-background-mobile.jpg`。建议分别准备横向和竖向 JPEG 图片并进行压缩。更换文件后修改：

```yaml
background_image: "images/your-background.jpg"
background_image_mobile: "images/your-background-mobile.jpg"
```

页面会自动添加深色或浅色遮罩，以保证文字可读性。桌面端照片会随鼠标产生轻微视差；触摸设备或开启“减少动态效果”的设备会自动使用静态背景。

首次打开主页时默认使用深色模式。用户通过页面右上角按钮切换主题后，选择会保存在浏览器中，后续访问将继续使用该主题。

## 编辑时的注意事项

- 使用空格缩进，不要使用 Tab。
- 同一层级保持相同缩进；本项目使用两个空格。
- 列表中的每一项以 `-` 开头。
- 建议用双引号包裹文本，尤其是包含 `:`、`#` 或特殊符号的内容。
- 不要删除变量区开头和结尾的 `---`。
- 修改 `_source/homepage.liquid` 后必须重新运行生成脚本，并同时提交模板与生成后的 `index.html`。
- 根目录 `index.html` 不再包含 Front Matter 或 Liquid 标记，直接双击即可正常打开。

## 发布到 GitHub Pages

修改完成后提交并推送到 GitHub：

```bash
git add index.html README.md _source/homepage.liquid scripts/build_homepage.rb images/ blogs/
git commit -m "Update homepage content"
git push
```

推送后，GitHub Pages 会直接发布生成好的静态 `index.html`。通常等待一到几分钟即可看到更新。
