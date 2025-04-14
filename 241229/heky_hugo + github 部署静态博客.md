### 安装 hugo

#### windows

> 记得开管理员模式如果用 cmd 或者 powershell，推荐用 git bash

Chocolatey
```bash
choco install hugo-extended
```

Scoop
```bash
scoop install hugo-extended
```
![choco 安装 hugo2](https://pan.heky.top/d/博客图片/choco安装hugo2.png)

Winget
```
winget install Hugo.Hugo.Extended
```
#### Debian/Ubuntu

```bash
sudo apt install hugo
```

### 创建一个站点

```bash
hugo new site path/to/site
```

推荐在要想要放博客文件的文件夹下面使用下面这行命令：
```bash
hugo new site .
```

创建好之后的文件目录：
![文件目录](https://pan.heky.top/d/博客图片/文件目录.png)

```bash
.
├── archetypes: default.md是生成博文的模版
├── assets # 存放被 Hugo Pipes 处理的文件
├── content # 存放markdown文件作为博文内容
├── data # 存放 Hugo 处理的数据
├── layouts # 存放布局文件
├── static # 存放静态文件 图片 CSS JS文件
├── themes: 存放不同的主题
└── config.toml: 博客配置文件支持 JSON YAML TOML 三种格式配置文件

```

### 创建文章内容

#### 创建一个文章内容页面

```bash
hugo new about.md
```

内容如下：

```bash
+++ 
date = "2015-01-08T08:36:54-07:00" 
draft = true 
title = "about" 
+++
```

只要将 draft 后面的参数改为 false 就是表示发布的意思
#### 创建一篇文章

```bash
hugo new post/first.md
```

### 添加主题

官方主题仓库：[https://themes.gohugo.io/](https://themes.gohugo.io/)

#### 下载文件到本地

文件下载之后放入 themes 文件夹中，注意，假如有一个主题叫做 heky，github 上直接下载后解压得到的文件夹可能叫做 heky-master，需要将后缀-master 删除

#### git clone

在 themes 文件夹目录下，使用 git clone 克隆仓库到本地

#### git submodule

关联主题仓库

> 要用这种方法，需要先在根目录用 git init 创建一个仓库

```bash
git submodule add https://github.com/example/library.git libs/library
```

好处：可以使用以下命令更新主题
进行初始化：

```bash
git submodule update --init --recursive
```

> 克隆了别人的仓库进行修改之后，希望还原

需要同步主题仓库的最新修改：

```bash
git submodule update --remote
```

坏处是想删干净很麻烦：
假设你有一个子模块在路径 `libs/library`，你想移除它：
完整的操作是：
```bash
git submodule deinit -f libs/library
git rm --cached libs/library
rm -rf libs/library
rm -rf .git/modules/libs/library
git commit -m "Remove submodule libs/library"
```

三种方法都要在根目录下的 `hugo.toml` 文件中添加新的一行：

```sh
theme = "xxx"
```

#### 运行 Hugo

```bash
hugo server --theme=hyde --buildDrafts
```

> 参数说明：
> --theme 后面跟想要的主题
> --buildDrafts 表示草稿也一并显示

hugo 默认开的端口是 1313
所以可以通过浏览器打开 http://localhost:1313 来访问博客

hugo 因为使用 go 语言来实现，所以运行速度很快，支持"热编写"，即，在打开服务的情况下可以创建，或者修改内容，而不用重新启动服务。

同时如果是部署在服务器上，此时就可以通过配置反向代理，来完成博客搭建的收尾工作。

不过如果没有服务器的话要如何？下面来介绍如何利用 github page 来部署我们的 hugo。

### 部署 Hugo 作为一个 Github Pages

第一步： **创建一个 Github 仓库**

1. 登录后，点击右上角，出现下拉菜单，点击 Your repositories 进入页面
2. 点击 New
3. 进入 Creat a new repository 页面
4. `Repository name` 这里一定要填 `[你的github账号].github.io`.

第二步：创建新文章

```text
hugo new posts/my-first-post.md
```


第三步：**修改配置文件 config.toml**

站点目录`config.toml`中`baseURL`要换成自己建立的仓库，如 baseURL = “https://xxx.github.io/"

第四步：进入**站点根目录**下，执行：

```fallback
hugo
```

执行后，站点根目录下会生成一个 `public` 文件夹，该文件下的内容即 Hugo 生成的整个静态网站。每次更新内容后，将 pubilc 目录里所有文件 push 到 GitHub 即可。

第五步：上传代码至 master

首次使用的时候要执行以下命令：

```bash
cd public
git init
git remote add origin git@xxx.git #仓库地址
git add .
git commit -m "[介绍，随便写点什么，比如日期]"
git branch -M main
git push -u origin main
```

> -u 表示将本地分支和远程分支关联，下次 push 时就可以不用显式的使用远程仓库名，而是可以直接用 git push

之后就可以通过 https://xxx.github.io/ 来访问我们的博客了。

以后每次**站点目录**下执行 `hugo` 命令后，再到`public`下执行推送命令：

```bash
git add .
git commit -m "[介绍，随便写点什么，比如日期]"
git push
```

### 自动化部署

通过上述命令我们可以手动发布我们的静态文件，但还是有以下弊端：

1. 发布步骤还是比较繁琐，本地调试后还需要切换到 `public/` 目录进行上传
2. 无法对博客 `.md` 源文件进行备份与版本管理

因此，我们需要简单顺滑的方式来进行博客发布，首先我们初始化博客源文件的仓库，

因为我们的博客基于 GitHub 与 GitHub Pages，可以通过官方提供的 GitHub Action 进行 CI 自动发布，下面我会进行详细讲解。GitHub Action 是一个持续集成和持续交付 (CI/CD) 平台，可用于自动执行构建、测试和部署管道，目前已经有很多开发好的工作流，可以通过简单的配置即可直接使用。

配置在仓库目录 `.github/workflows` 下，以 `.yml` 为后缀。
自动发布示例配置如下：

```yml
name: deploy

on:
    push:
    workflow_dispatch:
    schedule:
        # Runs everyday at 8:00 AM
        - cron: "0 0 * * *"

jobs:
    build:
        runs-on: ubuntu-latest
        steps:
            - name: Checkout
              uses: actions/checkout@v2
              with:
                  submodules: false
                  fetch-depth: 0

            - name: Setup Hugo
              uses: peaceiris/actions-hugo@v2
              with:
                  hugo-version: "latest"

            - name: Build Web
              run: hugo

            - name: Deploy Web
              uses: peaceiris/actions-gh-pages@v3
              with:
                  PERSONAL_TOKEN: ${{ secrets.PERSONAL_TOKEN }}
                  EXTERNAL_REPOSITORY: pseudoyu/pseudoyu.github.io
                  PUBLISH_BRANCH: main
                  PUBLISH_DIR: ./public
                  commit_message: ${{ github.event.head_commit.message }}
```

`on` 表示 GitHub Action 触发条件，我设置了 `push`、`workflow_dispatch` 和 `schedule` 三个条件：

- `push`，当这个项目仓库发生推送动作后，执行 GitHub Action
- `workflow_dispatch`，可以在 GitHub 项目仓库的 Action 工具栏进行手动调用
- `schedule`，定时执行 GitHub Action，如我的设置为北京时间每天早上执行，主要是使用一些自动化统计 CI 来自动更新我博客的关于页面，如本周编码时间，影音记录等，如果你不需要定时功能，可以删除这个条件

`jobs` 表示 GitHub Action 中的任务，我们设置了一个 `build` 任务，`runs-on` 表示 GitHub Action 运行环境，我们选择了 `ubuntu-latest`。我们的 `build` 任务包含了 `Checkout`、`Setup Hugo`、`Build Web` 和 `Deploy Web` 四个主要步骤，其中 `run` 是执行的命令，`uses` 是 GitHub Action 中的一个插件，我们使用了 `peaceiris/actions-hugo@v2` 和 `peaceiris/actions-gh-pages@v3` 这两个插件。其中 `Checkout` 步骤中 `with` 中配置 `submodules` 值为 `true` 可以同步博客源仓库的子模块，即我们的主题模块。

首先需要将上述 `deploy.yml` 中的 `EXTERNAL_REPOSITORY` 改为自己的 GitHub Pages 仓库。

因为我们需要从博客仓库推送到外部 GitHub Pages 仓库，需要特定权限，要在 GitHub 账户下 `Setting - Developer setting - Personal access tokens` 下创建一个 Token。