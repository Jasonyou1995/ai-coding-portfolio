# 项目路线图 (Projects Roadmap)

> 本文件跟踪所有项目的状态和进度。

---

## 📊 总览

| 阶段 | 项目数 | 已完成 | 进行中 | 待开始 |
|:---|:---:|:---:|:---:|:---:|
| Phase 1: 基础工具 | 5 | 1 | 0 | 4 |
| Phase 2: 网络服务 | 10 | 0 | 0 | 10 |
| Phase 3: AI 应用 | 10 | 0 | 0 | 10 |
| Phase 4: 系统架构 | 5 | 0 | 0 | 5 |
| **总计** | **30** | **1** | **0** | **29** |

---

## Phase 1: 基础工具 (第 1-4 周)

### 01. Smart Mailbox ✅

**状态**: 已完成  
**路径**: [projects/01-smart-mailbox](./projects/01-smart-mailbox/)

**核心功能**:
- 用户注册/登录（JWT 认证）
- 邮件 CRUD 操作
- AI 自动分类
- 端到端加密
- 附件分片上传
- 限流保护

**技术栈**: FastAPI, MongoDB, Redis, MinIO, JWT, bcrypt, OpenAI API

**学习要点**:
- REST API 设计
- 密码安全存储
- JWT 认证流程
- 文件上传优化
- AI 服务集成

---

### 02. Code Reviewer AI 🔵

**状态**: 计划中  
**预计开始**: 2024-04-03

**核心功能**:
- Git Pre-commit Hook
- 代码变更分析
- AI 自动 Review
- 自定义规则

**技术栈**: Python, Git, OpenAI API

**学习要点**:
- Git Hooks 机制
- AST 代码分析
- Prompt Engineering

---

### 03. Config Manager 🔵

**状态**: 计划中

**核心功能**:
- 多环境配置管理
- 配置验证
- 敏感信息加密
- 配置继承/覆盖

**技术栈**: Python, Click, YAML

---

### 04. Log Analyzer 🔵

**状态**: 计划中

**核心功能**:
- 日志解析
- 模式识别
- 统计分析
- 可视化报表

**技术栈**: Python, Regex, Pandas, Matplotlib

---

### 05. API Tester 🔵

**状态**: 计划中

**核心功能**:
- API 测试用例管理
- 自动化测试执行
- 性能测试
- 测试报告生成

**技术栈**: Python, HTTPX, Jinja2

---

## Phase 2: 网络服务 (第 5-12 周)

### 06. URL Shortener 🔵

**状态**: 计划中

**核心功能**:
- 短链接生成
- 重定向服务
- 访问统计
- 自定义短码

**技术亮点**:
- Bloom Filter 防重复
- Base62 编码
- 缓存优化

---

### 07. Chat Server 🔵

**状态**: 计划中

**核心功能**:
- WebSocket 实时通信
- 多房间支持
- 消息持久化
- 在线状态

**技术栈**: FastAPI, WebSocket, Redis Pub/Sub

---

### 08. API Gateway 🔵

**状态**: 计划中

**核心功能**:
- 反向代理
- 路由管理
- 认证鉴权
- 限流熔断

---

### 09. File Service 🔵

**状态**: 计划中

**核心功能**:
- 分片上传
- 断点续传
- 秒传功能
- 对象存储对接

---

### 10. Task Queue 🔵

**状态**: 计划中

**核心功能**:
- 任务队列管理
- 优先级调度
- 失败重试
- 监控面板

**技术栈**: Redis, Celery (或自研)

---

### 11-15. (待规划) ⚪

---

## Phase 3: AI 应用 (第 13-22 周)

### 16. RAG System ⚪

**状态**: 待规划

**核心功能**:
- 文档向量化
- 语义检索
- 上下文增强
- 引用溯源

**技术栈**: LangChain, Chroma/Pinecone, OpenAI API

---

### 17. Agent Framework ⚪

**状态**: 待规划

**核心功能**:
- ReAct 模式
- Tool 使用
- 规划与执行
- 记忆管理

---

### 18. MCP Server ⚪

**状态**: 待规划

**核心功能**:
- MCP 协议实现
- Context 管理
- Tool 注册
- 多客户端支持

---

### 19-25. (待规划) ⚪

---

## Phase 4: 系统架构 (第 23-30 周)

### 26. Distributed Lock ⚪

**状态**: 待规划

**核心功能**:
- Redis Redlock 实现
- 锁续期
- 死锁检测

---

### 27. Message Queue ⚪

**状态**: 待规划

**核心功能**:
- 消息发布/订阅
- 消息持久化
- 顺序保证
- 消费确认

---

### 28. Rate Limiter ⚪

**状态**: 待规划

**核心功能**:
- 分布式限流
- 滑动窗口
- 令牌桶
- 动态调整

---

### 29. Monitor System ⚪

**状态**: 待规划

**核心功能**:
- 指标采集
- 告警通知
- 可视化面板

**技术栈**: Prometheus, Grafana

---

### 30. K8s Deployment ⚪

**状态**: 待规划

**核心功能**:
- K8s 部署配置
- Helm Charts
- CI/CD 流水线
- 服务网格

---

## 🎯 里程碑

| 里程碑 | 目标日期 | 完成标准 |
|:---|:---|:---|
| Phase 1 完成 | 2024-04-24 | 5 个项目全部完成 |
| Phase 2 完成 | 2024-06-19 | 15 个项目全部完成 |
| Phase 3 完成 | 2024-08-28 | 25 个项目全部完成 |
| Portfolio 完成 | 2024-10-23 | 30 个项目全部完成 |

---

## 📝 项目创建命令

```bash
# 创建新项目
./scripts/create-project.sh <number> <name>

# 示例
./scripts/create-project.sh 02 code-reviewer-ai
```

---

*最后更新: 2024-03-27*
