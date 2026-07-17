# Yanqi Dai's Homepage

这是一个由单个 `index.html` 文件生成的个人主页。除头像外，姓名、邮箱、简介、论文、实习经历和获奖信息等内容都集中在 `index.html` 文件最前面的变量区中。

## 修改主页内容

打开 `index.html`，找到文件顶部由两行 `---` 包围的 `EDITABLE CONTENT` 区域：

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
---
```

通常只需修改这个区域，不需要修改后面的 HTML、CSS 或 JavaScript。

### 个人信息

在 `profile` 分区中修改：

- `site_url`：主页网址，不要在结尾添加 `/`
- `name`、`name_zh`：英文名和中文名
- `initials`：导航栏中的姓名缩写
- `email`：联系邮箱
- `description`：搜索引擎和分享卡片使用的简介
- `image`：头像路径
- `background_image`：页面背景图片路径
- `footer_year`：页脚年份
- `hero_intro`：首页顶部简介
- `role`、`affiliation`：当前身份和单位
- `research_chips`：头像周围展示的研究方向
- `about`：详细自我介绍和研究方向图
- `social_links`：Google Scholar、GitHub 等外部链接

`research_chips` 和 `about.map_nodes` 都支持任意数量，页面会自动换行和扩展，不需要增加 CSS 定位样式。

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

论文、经历、奖项和社交链接同样支持任意数量。增加条目后，页面会自动增加卡片、行或网格，不需要修改 HTML 模板。

### 荣誉与奖项

在 `awards.items` 中填写：

```yaml
- title: "Award Name"
  organization: "University or Organization"
  year: "2026"
```

如果奖项没有颁发单位，可以省略 `organization`。

### 更换头像

当前头像位于 `images/yanqidai.png`。有两种更换方式：

1. 用新图片覆盖该文件，并保持文件名不变。
2. 将新图片放入 `images` 目录，然后修改 `profile.image`，例如：

```yaml
image: "/images/new-profile.jpg"
```

### 更换背景图

当前背景图位于 `images/mountain-background.jpg`。建议使用宽度约 2000 像素的横向 JPEG 图片，并在上传前进行压缩。更换文件后修改：

```yaml
background_image: "/images/your-background.jpg"
```

页面会自动添加深色或浅色遮罩，以保证文字可读性。桌面端照片会随鼠标产生轻微视差；触摸设备或开启“减少动态效果”的设备会自动使用静态背景。

## 编辑时的注意事项

- 使用空格缩进，不要使用 Tab。
- 同一层级保持相同缩进；本项目使用两个空格。
- 列表中的每一项以 `-` 开头。
- 建议用双引号包裹文本，尤其是包含 `:`、`#` 或特殊符号的内容。
- 不要删除变量区开头和结尾的 `---`。
- 页面内容由 GitHub Pages 构建，直接双击本地 `index.html` 不会完成变量渲染。

## 发布到 GitHub Pages

修改完成后提交并推送到 GitHub：

```bash
git add index.html README.md images/
git commit -m "Update homepage content"
git push
```

推送后，GitHub Pages 会自动读取 `index.html` 顶部的变量并重新生成主页。通常等待一到几分钟即可看到更新。
