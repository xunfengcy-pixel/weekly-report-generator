# 🐳 Docker 部署方案

## 用户使用方法（超简单）

### 第一步：安装 Docker Desktop

1. 访问 https://www.docker.com/products/docker-desktop/
2. 下载对应系统的版本（Windows/Mac/Linux 都有）
3. 安装并启动 Docker Desktop

### 第二步：获取周报生成器

#### 方式 A：使用打包好的镜像（推荐）

把 `weekly_report_generator` 文件夹发给用户，包含：
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `app.py`
- `config.py`
- `template.html`

#### 方式 B：从 Docker Hub 拉取（如果你上传了镜像）

```bash
docker pull yourname/weekly-report-generator:latest
```

### 第三步：启动应用

#### 方法 1：使用 Docker Compose（推荐）

在文件夹中打开终端，执行：

```bash
# 进入项目目录
cd weekly_report_generator

# 启动服务
docker-compose up -d

# 查看日志（可选）
docker-compose logs -f
```

浏览器访问：`http://localhost:8501`

#### 方法 2：使用 Docker 命令

```bash
# 构建镜像
docker build -t weekly-report-generator .

# 运行容器
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --name weekly-report \
  weekly-report-generator
```

浏览器访问：`http://localhost:8501`

---

## 📦 给用户的极简说明书

```
📊 周报生成器 - Docker 版
==========================

【前提条件】
1. 安装 Docker Desktop（https://www.docker.com/products/docker-desktop/）

【启动步骤】
1. 解压 weekly_report_generator.zip
2. 打开终端，进入文件夹
3. 运行：docker-compose up -d
4. 浏览器访问：http://localhost:8501

【停止服务】
docker-compose down

【查看日志】
docker-compose logs -f

【数据说明】
- 所有数据保存在 ./data 文件夹中
- 重启容器数据不会丢失
```

---

## 🔧 常用命令

| 命令 | 说明 |
|------|------|
| `docker-compose up -d` | 后台启动服务 |
| `docker-compose down` | 停止服务 |
| `docker-compose logs -f` | 查看实时日志 |
| `docker-compose restart` | 重启服务 |
| `docker-compose pull` | 更新镜像 |
| `docker ps` | 查看运行中的容器 |

---

## 💾 数据持久化

数据保存在 `./data` 目录下，包含：
- `weekly_report_autosave.json` - 自动保存的数据

即使删除容器，只要保留 data 文件夹，数据就不会丢失。

---

## 🌐 局域网访问

如果想让局域网内的其他电脑也能访问：

### 修改 docker-compose.yml

```yaml
ports:
  - "0.0.0.0:8501:8501"  # 允许外部访问
```

然后其他电脑通过 `http://你的IP:8501` 访问。

---

## 🚀 构建并推送镜像到 Docker Hub

如果你想让用户直接 `docker pull` 而不用本地构建：

### 1. 注册 Docker Hub 账号

访问 https://hub.docker.com/ 注册

### 2. 登录并推送

```bash
# 登录
docker login

# 构建镜像（替换 yourname 为你的用户名）
docker build -t yourname/weekly-report-generator:latest .

# 推送镜像
docker push yourname/weekly-report-generator:latest
```

### 3. 用户使用方法

```bash
# 直接拉取运行
docker run -d -p 8501:8501 --name weekly-report yourname/weekly-report-generator:latest
```

---

## 🆚 Docker vs 原生打包对比

| 特性 | Docker 方案 | PyInstaller 打包 |
|------|-------------|------------------|
| 安装难度 | 需安装 Docker | 无需额外安装 |
| 启动方式 | 命令行 | 双击运行 |
| 跨平台 | ✅ 完美支持 | 需分别打包 |
| 文件大小 | 较大（含完整环境） | 较小 |
| 更新维护 | 简单（换镜像） | 需重新打包 |
| 适合人群 | 技术人员 | 普通用户 |

---

## ❓ 常见问题

### Q1: 端口被占用怎么办？

修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8502:8501"  # 使用 8502 端口
```

### Q2: 如何更新应用？

```bash
# 拉取最新代码后重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Q3: 容器启动失败？

查看日志排查问题：
```bash
docker-compose logs
```

### Q4: 如何备份数据？

直接复制 `data` 文件夹即可。

---

## 📝 总结

**Docker 方案最适合：**
- 用户有一定技术背景
- 需要同时支持 Windows/Mac/Linux
- 方便远程部署和更新
- 不想处理各种系统兼容性问题

**最简单的用户操作流程：**
1. 安装 Docker Desktop
2. 解压文件夹
3. 运行 `docker-compose up -d`
4. 浏览器访问 `localhost:8501`
