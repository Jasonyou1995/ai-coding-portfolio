# 🤖 AI Coding Portfolio

> 系统化的 AI 编程学习之旅，包含 20-30+ 实战项目，展示从基础工具到分布式系统的完整技术栈。

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📚 项目概览

本作品集采用 **分级递进** 设计，分为四个阶段：

| 阶段 | 数量 | 类型 | 技术重点 | 状态 |
|:---|:---:|:---|:---|:---:|
| **基础工具** | 1-5 | CLI 工具、爬虫、数据处理 | Python 基础、文件 IO、正则 | 🔵 计划中 |
| **网络服务** | 6-15 | Web 服务、API 网关、即时通讯 | FastAPI、WebSocket、并发 | 🟡 进行中 |
| **AI 应用** | 16-25 | RAG 系统、Agent 框架、MCP | LLM 集成、向量数据库、Prompt 工程 | ⚪ 待开始 |
| **系统架构** | 26-30 | 分布式锁、消息队列、监控系统 | Redis 集群、Kafka、K8s 部署 | ⚪ 待开始 |

---

## 📁 仓库结构

```
ai-coding-portfolio/
├── templates/                    # 🔥 项目模板（Master 指令）
│   ├── base-python/             # Python 项目脚手架
│   │   ├── src/                 # 源码模板
│   │   ├── tests/               # 测试模板
│   │   ├── docs/decisions.md    # ADR 模板
│   │   ├── pyproject.toml       # 项目配置
│   │   ├── Dockerfile           # 容器化
│   │   └── README.template.md   # README 模板
│   ├── base-node/               # Node.js 模板 (TODO)
│   └── prompts/                 # AI Prompt 记录模板
│
├── projects/                     # 🔥 实战项目（每个独立可运行）
│   ├── 01-smart-mailbox/        # 智能邮箱系统（蚂蚁笔试题扩展）
│   ├── 02-code-reviewer-ai/     # AI 代码审查工具 (TODO)
│   ├── 03-mcp-server-demo/      # MCP 协议实现 (TODO)
│   └── ... (共 20-30 个)
│
├── docs/                         # 📚 架构决策记录（ADR）
│   ├── adr/
│   │   ├── 001-why-fastapi.md   # 为什么选择 FastAPI
│   │   └── 002-security-patterns.md  # 安全与隐私策略
│   └── learning-path.md         # 学习路线图
│
└── .github/                      # CI/CD 配置
    └── workflows/
```

---

## 🚀 快速开始

### 创建新项目

```bash
# 1. 使用模板创建新项目
NEW_PROJECT="02-my-project"
cp -r templates/base-python projects/${NEW_PROJECT}

# 2. 进入项目并初始化
cd projects/${NEW_PROJECT}
cp .env.example .env

# 3. 安装依赖
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. 运行测试
pytest --cov=src --cov-report=html

# 5. 启动服务
python src/main.py
```

---

## 📊 项目索引

### Phase 1: 基础工具 (1-5)

| # | 项目名称 | 描述 | 技术栈 | 状态 |
|:---:|:---|:---|:---|:---:|
| 01 | [Smart Mailbox](./projects/01-smart-mailbox/) | 智能邮箱系统（蚂蚁笔试题扩展） | FastAPI, MongoDB, JWT, AI 分类 | ✅ 已完成 |
| 02 | Code Reviewer AI | AI 代码审查工具（Git Hook 集成） | Python, Git, OpenAI API | 🔵 计划中 |
| 03 | Config Manager | 多环境配置管理 CLI | Python, YAML, Click | 🔵 计划中 |
| 04 | Log Analyzer | 日志分析工具 | Python, Regex, Pandas | 🔵 计划中 |
| 05 | API Tester | API 自动化测试工具 | Python, HTTPX, Jinja2 | 🔵 计划中 |

### Phase 2: 网络服务 (6-15)

| # | 项目名称 | 描述 | 技术栈 | 状态 |
|:---:|:---|:---|:---|:---:|
| 06 | URL Shortener | 高并发短链生成器 | FastAPI, Redis, Bloom Filter | 🔵 计划中 |
| 07 | Chat Server | 实时聊天服务 | FastAPI, WebSocket, Redis Pub/Sub | 🔵 计划中 |
| 08 | API Gateway | 轻量级 API 网关 | Python, Rate Limit, Auth | 🔵 计划中 |
| 09 | File Service | 分布式文件存储 | FastAPI, MinIO, 分片上传 | 🔵 计划中 |
| 10 | Task Queue | 分布式任务队列 | Redis, Celery, 监控 | 🔵 计划中 |
| 11 | ... | ... | ... | ⚪ 待规划 |

### Phase 3: AI 应用 (16-25)

| # | 项目名称 | 描述 | 技术栈 | 状态 |
|:---:|:---|:---|:---|:---:|
| 16 | RAG System | 检索增强生成系统 | LangChain, Vector DB, OpenAI | ⚪ 待规划 |
| 17 | Agent Framework | 简单 Agent 框架 | Python, ReAct, Tools | ⚪ 待规划 |
| 18 | MCP Server | Model Context Protocol 实现 | Python, MCP Spec | ⚪ 待规划 |
| 19 | AI Translator | 智能翻译服务 | FastAPI, LLM, 缓存 | ⚪ 待规划 |
| 20 | ... | ... | ... | ⚪ 待规划 |

### Phase 4: 系统架构 (26-30)

| # | 项目名称 | 描述 | 技术栈 | 状态 |
|:---:|:---|:---|:---|:---:|
| 26 | Distributed Lock | 分布式锁实现 | Redis Redlock, Python | ⚪ 待规划 |
| 27 | Message Queue | 消息队列系统 | Kafka/Redis Streams | ⚪ 待规划 |
| 28 | Rate Limiter | 集群限流器 | Redis, Sliding Window | ⚪ 待规划 |
| 29 | Monitor System | 简单监控系统 | Prometheus, Grafana | ⚪ 待规划 |
| 30 | K8s Deployment | Kubernetes 部署示例 | K8s, Helm, CI/CD | ⚪ 待规划 |

---

## 🔒 隐私与安全

本仓库严格遵循隐私保护原则：

### 🔴 绝对不提交

- ✅ `.env` 文件已加入 `.gitignore`
- ✅ 所有 API Keys 使用环境变量管理
- ✅ 个人敏感信息完全脱敏

### 🟡 脱敏处理

| 内容 | 处理方式 |
|:---|:---|
| 邮箱 | `user@example.com` |
| 手机号 | `138****8888` |
| 姓名 | GitHub 昵称 `@yourname` |
| 公司数据 | Faker 生成 Mock 数据 |

### 🟢 安全最佳实践

- 密码 bcrypt 加密存储
- JWT Token 短有效期 + Refresh 机制
- API 速率限制保护
- SQL 注入防护（参数化查询）
- XSS/CSRF 防护

---

## 📝 设计原则

### 1. 刻意保留思考痕迹

每个项目的 README 都包含：
- **迭代记录**：v0.1 → v0.2 → v0.3 的演进过程
- **错误记录**：遇到的问题和解决方案
- **性能数据**：压测前后的对比

### 2. 技术决策记录 (ADR)

每个项目包含 `docs/decisions.md`，记录：
- 为什么选择技术 A 而非 B
- 考虑的备选方案
- 决策的后果和权衡

### 3. 代码"不完美"的艺术

```python
# 留一个 TODO 展示思考过程
# TODO: 这里可以考虑用布隆过滤器优化，暂时用 set 实现
```

### 4. 可运行证据

每个项目包含：
- ✅ 完整测试套件
- ✅ Docker 部署配置
- ✅ 压测结果截图
- ✅ 覆盖率报告

---

## 🛠️ 技术栈

### 主要技术

| 类别 | 技术 |
|:---|:---|
| **后端框架** | FastAPI, Flask (少量) |
| **数据库** | PostgreSQL, MongoDB, Redis |
| **消息队列** | Redis, RabbitMQ, Kafka |
| **AI/LLM** | OpenAI API, LangChain, Anthropic |
| **部署** | Docker, Docker Compose, Kubernetes |
| **监控** | Prometheus, Grafana |

### 开发工具

- **代码质量**: Black, Ruff, MyPy, pre-commit
- **测试**: pytest, pytest-cov, pytest-asyncio
- **压测**: wrk, locust
- **文档**: Markdown, Mermaid

---

## 🤝 贡献指南

### 提交信息规范

```bash
# 格式: <type>: <subject>
git commit -m "feat: 基础登录实现（session 版）"
git commit -m "fix: 解决附件上传大文件内存溢出"
git commit -m "refactor: 登录鉴权从 session 迁移到 JWT"
```

### 类型说明

| 类型 | 说明 |
|:---|:---|
| `feat` | 新功能 |
| `fix` | 修复 |
| `refactor` | 重构 |
| `docs` | 文档 |
| `test` | 测试 |
| `chore` | 构建/工具 |

---

## 📖 学习资源

### 推荐书籍

- 《设计数据密集型应用》- Martin Kleppmann
- 《流畅的 Python》- Luciano Ramalho
- 《构建高性能 Web 站点》- 郭欣

### 在线资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/)

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🙏 致谢

- 蚂蚁集团笔试题（作为 01 项目的基础需求）
- FastAPI 社区
- 开源社区的各位贡献者

---

> 💡 **提示**: 每个项目都是独立可运行的，可以 `cd` 进入任意项目目录执行 `docker-compose up` 快速体验。
