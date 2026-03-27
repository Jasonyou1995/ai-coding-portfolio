# 01 - Smart Mailbox (智能邮箱系统)

> 基于蚂蚁集团笔试题扩展的智能邮箱系统，增加 AI 自动分类和端到端加密功能。

## 📋 项目信息

| 属性 | 内容 |
|:---|:---|
| **项目编号** | 01 |
| **类型** | 网络服务 |
| **技术栈** | FastAPI, MongoDB, Redis, JWT, bcrypt |
| **难度** | ⭐⭐⭐ 中等 |
| **预计工期** | 5-7 天 |

---

## 🎯 项目目标

复刻并扩展蚂蚁笔试题中的邮箱系统，增加以下增强：

1. **AI 自动分类**：邮件自动分类（工作/社交/广告）
2. **端到端加密**：敏感邮件内容加密存储
3. **限流保护**：登录接口防暴力破解
4. **附件分片上传**：大文件断点续传

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        客户端 (Client)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/WebSocket
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI API 层                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ 用户认证模块  │  │ 邮件管理模块  │  │ AI 分类模块       │  │
│  │ - JWT Auth   │  │ - CRUD       │  │ - OpenAI API     │  │
│  │ - Rate Limit │  │ - Encryption │  │ - Caching        │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────────┐ ┌─────────┐ ┌──────────────┐
│   MongoDB    │ │  Redis  │ │    MinIO     │
│  (邮件数据)   │ │(缓存/限流)│ │  (附件存储)   │
└──────────────┘ └─────────┘ └──────────────┘
```

---

## 📁 项目结构

```
01-smart-mailbox/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 配置管理
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT/密码加密
│   │   ├── encryption.py       # 端到端加密
│   │   └── rate_limit.py       # 限流实现
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # 用户模型
│   │   └── email.py            # 邮件模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # 认证服务
│   │   ├── email_service.py    # 邮件服务
│   │   └── ai_classifier.py    # AI 分类器
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── auth.py         # 认证路由
│           └── emails.py       # 邮件路由
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_emails.py
├── docs/
│   ├── decisions.md            # ADR
│   └── benchmark.png           # 压测结果
├── .env.example
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Docker & Docker Compose

### 本地开发

```bash
# 1. 进入项目目录
cd projects/01-smart-mailbox

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 OpenAI API Key

# 3. 启动依赖服务
docker-compose up -d mongo redis minio

# 4. 安装依赖并运行
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

### Docker 一键启动

```bash
docker-compose up --build
```

---

## 🧪 测试

```bash
# 运行测试
pytest --cov=src --cov-report=html

# 压测
wrk -t12 -c400 -d30s http://localhost:8000/api/v1/health
```

---

## 📝 迭代记录

### v0.1 (Day 1-2) - 基础框架
- ✅ 搭建 FastAPI 项目结构
- ✅ 实现用户注册/登录（session 版）
- ❌ **错误**：直接把密码明文存 MongoDB
- ✅ **修正**：朋友 code review 后改用 bcrypt 加密

### v0.2 (Day 3) - 邮件核心功能
- ✅ 邮件 CRUD 接口
- ✅ 附件上传（本地磁盘版）
- ❌ **问题**：测试大文件上传时发现磁盘 IO 瓶颈
- ✅ **解决**：引入 MinIO 对象存储，实现分片上传

### v0.3 (Day 4) - 安全增强
- ✅ 迁移 session 认证到 JWT
- ✅ 增加 Redis 令牌桶限流
- ✅ 实现邮件内容 AES 加密存储
- 📊 压测：1000 QPS 下 P99 延迟 < 50ms

### v0.4 (Day 5-6) - AI 功能
- ✅ 集成 OpenAI API 自动分类
- ✅ 增加分类结果缓存（Redis）
- 📝 TODO: 考虑用本地小模型替代，降低延迟

---

## 📊 性能测试

```bash
# 登录接口压测
wrk -t12 -c400 -d30s \
  -s scripts/login.lua \
  http://localhost:8000/api/v1/auth/login
```

| 指标 | 优化前 | 优化后 |
|:---|:---|:---|
| QPS | 450 | 1200 |
| 平均延迟 | 89ms | 32ms |
| P99 延迟 | 210ms | 48ms |
| 错误率 | 0.5% | 0% |

**优化措施**：
- 增加 Redis 连接池
- JWT 签名使用缓存
- MongoDB 索引优化

---

## 🔧 技术决策 (ADR)

见 [docs/decisions.md](./docs/decisions.md)

### 关键决策摘要

| 决策 | 选择 | 理由 |
|:---|:---|:---|
| 认证方式 | JWT | 无状态，支持跨域 |
| 限流算法 | 令牌桶 | 允许突发流量，平滑限流 |
| 文件存储 | MinIO | 兼容 S3 API，易于扩展 |
| 加密方案 | AES-256-GCM | 标准算法，支持认证加密 |

---

## ⚠️ 隐私声明

本项目所有数据均为 **Mock 数据**，不含任何真实个人信息。

- 用户数据：使用 Faker 生成假数据
- API Keys：使用 `.env` 管理，不提交到 Git
- 邮件内容：全部为随机生成的测试文本

---

## 📚 参考资料

- 原始需求：蚂蚁集团 2027 届校招笔试题（邮箱系统）
- FastAPI 文档: https://fastapi.tiangolo.com/
- OWASP 认证最佳实践: https://cheatsheetseries.owasp.org/

---

## 🎓 学习心得

通过本项目学习到：

1. **密码安全**：永远不要用明文存储密码
2. **限流设计**：生产环境必须有限流保护
3. **加密选择**：对称加密用 AES-GCM，非对称用 RSA/OAEP
4. **AI 集成**：LLM API 需要缓存和降级策略
