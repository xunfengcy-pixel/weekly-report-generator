# 🚀 GitHub Actions 自动打包快速开始

## 什么是 GitHub Actions？

GitHub Actions 是 GitHub 提供的免费自动化服务。你把代码推送到 GitHub，它会自动在云端（Windows/Mac/Linux）打包你的应用，生成可执行文件。

**优点：**
- ✅ 完全免费
- ✅ 真正的 macOS 环境打包
- ✅ 无需自己准备 Mac
- ✅ 自动发布到 Releases 页面

---

## 第一步：创建 GitHub 仓库

### 1. 注册/登录 GitHub
访问 https://github.com

### 2. 创建新仓库
1. 点击右上角 **+** → **New repository**
2. 仓库名称：`weekly-report-generator`
3. 选择 **Public**（公开，免费）
4. 勾选 **Add a README file**
5. 点击 **Create repository**

---

## 第二步：上传代码到 GitHub

### 方法 A：使用 Git 命令行

```bash
# 1. 进入你的项目文件夹
cd weekly_report_generator

# 2. 初始化 git（如果还没初始化）
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit"

# 5. 连接远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/weekly-report-generator.git

# 6. 推送代码
git push -u origin main
```

### 方法 B：使用 GitHub Desktop（图形界面）

1. 下载 GitHub Desktop：https://desktop.github.com/
2. 登录你的 GitHub 账号
3. 点击 **File** → **Add local repository**
4. 选择 `weekly_report_generator` 文件夹
5. 点击 **Publish repository**

### 方法 C：直接网页上传

1. 打开你的 GitHub 仓库页面
2. 点击 **Add file** → **Upload files**
3. 拖拽所有文件上传
4. 点击 **Commit changes**

---

## 第三步：触发自动打包

### 方式一：创建标签（推荐，会发布 Release）

```bash
# 创建版本标签
git tag -a v1.0.0 -m "版本 1.0.0"

# 推送标签到 GitHub
git push origin v1.0.0
```

推送标签后，GitHub Actions 会自动：
1. 在 Windows 上打包 `.exe`
2. 在 macOS 上打包 `.app`
3. 在 Linux 上打包可执行文件
4. 创建 Release 并上传文件

### 方式二：推送到 main 分支（只打包，不发布 Release）

```bash
git add .
git commit -m "更新代码"
git push origin main
```

---

## 第四步：下载打包好的应用

### 查看打包进度

1. 打开 GitHub 仓库页面
2. 点击上方的 **Actions** 标签
3. 查看打包进度（绿色 ✓ 表示成功，红色 ✗ 表示失败）

### 下载应用

#### 方式 A：从 Releases 下载（推荐）

1. 点击仓库右侧的 **Releases**
2. 找到最新版本
3. 下载对应系统的文件：
   - Windows: `周报生成器-Windows.zip`
   - macOS: `周报生成器-macOS.zip`
   - Linux: `周报生成器-Linux.zip`

#### 方式 B：从 Artifacts 下载

1. 进入 **Actions** 页面
2. 点击最新的工作流运行记录
3. 页面底部有 **Artifacts** 区域
4. 下载对应系统的文件

---

## 完整操作流程示例

```bash
# 1. 进入项目文件夹
cd weekly_report_generator

# 2. 初始化 git
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit"

# 5. 连接远程仓库（替换你的用户名）
git remote add origin https://github.com/你的用户名/weekly-report-generator.git

# 6. 推送代码
git push -u origin main

# 7. 创建版本标签（触发打包）
git tag -a v1.0.0 -m "版本 1.0.0"
git push origin v1.0.0

# 8. 等待 5-10 分钟，然后去 GitHub Releases 下载
```

---

## 更新代码并重新打包

```bash
# 1. 修改代码...

# 2. 提交并推送
git add .
git commit -m "修复了 xxx 问题"
git push origin main

# 3. 创建新版本标签
git tag -a v1.1.0 -m "版本 1.1.0"
git push origin v1.1.0

# 4. 等待打包完成，下载新版本
```

---

## 常见问题

### Q: 推送代码时提示 "Permission denied"
A: 需要使用 HTTPS 或配置 SSH 密钥。最简单的方法是用 GitHub Desktop。

### Q: Actions 运行失败？
A: 点击 Actions 页面查看详细日志，通常是依赖安装问题。

### Q: Mac 应用打不开？
A: 这是 Apple 安全机制，需要用户右键打开。可以在 README 中说明。

### Q: 打包后的文件太大？
A: PyInstaller 打包的文件约 100-200MB，这是正常的，包含了 Python 环境。

---

## 下一步

1. 创建 GitHub 仓库
2. 上传代码
3. 创建标签 `v1.0.0`
4. 等待 5-10 分钟
5. 下载 Mac 版本测试

遇到问题随时问我！
