# 🚀 GitHub Actions 自动打包说明

## 功能介绍

配置 GitHub Actions 后，每次推送代码到 GitHub，系统会自动：
- 在 Windows 上打包 `.exe` 可执行文件
- 在 macOS 上打包 `.app` 应用程序
- 在 Linux 上打包可执行文件
- 自动发布到 GitHub Releases

---

## 配置步骤

### 第一步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库（如 `weekly-report-generator`）
3. 选择 **Public**（免费）或 **Private**（需要付费账号才能使用 Actions）

### 第二步：推送代码到 GitHub

在项目文件夹中执行：

```bash
# 初始化 git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/weekly-report-generator.git

# 推送
git push -u origin main
```

或者直接把文件夹拖到 GitHub Desktop 上传。

### 第三步：触发自动打包

#### 方式 A：推送到 main 分支
每次 `git push` 到 main 分支，会自动打包（但不会发布 Release）

#### 方式 B：创建标签发布（推荐）
```bash
# 创建版本标签
git tag -a v1.0.0 -m "版本 1.0.0"

# 推送标签
git push origin v1.0.0
```

推送标签后，会自动：
1. 打包三个平台的可执行文件
2. 创建 GitHub Release
3. 把可执行文件附加到 Release 中

### 第四步：下载可执行文件

1. 打开 GitHub 仓库页面
2. 点击右侧的 **Releases**
3. 找到最新版本
4. 下载对应系统的文件：
   - Windows: `周报生成器.exe`
   - macOS: `周报生成器.app` (需要解压)
   - Linux: `weekly-report-generator`

---

## 📦 用户使用方法

### Windows 用户

1. 下载 `周报生成器.exe`
2. 双击运行
3. 浏览器自动打开

### Mac 用户

1. 下载 `周报生成器.app.zip`，解压
2. 双击 `周报生成器.app`
3. 如果提示"无法验证开发者"：
   - 按住 `Control` 键，点击应用
   - 选择"打开" → "仍要打开"

### Linux 用户

1. 下载 `weekly-report-generator`
2. 添加执行权限：`chmod +x weekly-report-generator`
3. 运行：`./weekly-report-generator`

---

## 🔧 手动触发打包

如果不想推送代码，也可以手动触发：

1. 打开 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 **Build Executables** 工作流
4. 点击 **Run workflow** → **Run workflow**

---

## 📁 项目结构要求

确保仓库包含以下文件：
```
weekly_report_generator/
├── .github/
│   └── workflows/
│       └── build.yml      # GitHub Actions 配置
├── app.py                 # 主应用
├── config.py              # 配置
├── template.html          # 模板
├── run_app.py             # 打包入口
└── requirements.txt       # 依赖
```

---

## ⚠️ 注意事项

### 关于 macOS 打包

由于 Apple 的安全机制，打包的 Mac 应用：
- 可能需要用户右键打开（Control + 点击）
- 可能需要在系统设置中允许"任何来源"的应用
- 如果要在 Mac 上完全无警告运行，需要购买 Apple 开发者证书（$99/年）

**临时解决方案：**
用户首次运行时，在终端执行：
```bash
xattr -cr /path/to/周报生成器.app
```

### 关于文件大小

PyInstaller 打包的文件较大（约 100-200MB），因为包含了完整的 Python 环境。

---

## 🔄 更新流程

1. 修改代码
2. 提交并推送：
   ```bash
   git add .
   git commit -m "更新内容"
   git push
   ```
3. 创建新版本标签：
   ```bash
   git tag -a v1.1.0 -m "版本 1.1.0"
   git push origin v1.1.0
   ```
4. 等待 Actions 完成
5. 在 Releases 页面下载新版本

---

## 💡 替代方案

如果不想用 GitHub Actions，也可以：

### 方案 1：本地打包
在自己的电脑上安装 PyInstaller，执行打包命令。

### 方案 2：找朋友帮忙
把代码发给有 Mac 的朋友，让他在 Mac 上运行打包脚本。

### 方案 3：使用云 Mac 服务
如 MacStadium、AWS EC2 Mac 实例等（有免费额度）。

---

## ❓ 常见问题

### Q: Actions 运行失败？
A: 点击 Actions 页面查看详细日志，通常是依赖安装问题。

### Q: 打包后的文件无法运行？
A: 检查是否缺少依赖，可以在本地先测试 PyInstaller 打包。

### Q: Mac 应用打不开？
A: 这是 Apple 安全机制，需要用户手动允许，或购买开发者证书签名。

---

## 📞 需要帮助？

GitHub Actions 文档：https://docs.github.com/cn/actions
