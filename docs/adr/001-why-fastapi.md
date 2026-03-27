# ADR-001: 为什么选择 FastAPI 作为主力框架

**状态**: 已接受 ✅  
**日期**: 2024-03-27  
**作者**: @yourname

---

## 背景

在构建 AI Coding Portfolio 的多个项目时，需要选择一个统一的主力 Web 框架。主要考虑因素：

1. **性能**：需要支持高并发场景（如实时通信、流式响应）
2. **开发效率**：快速迭代，自动生成文档
3. **AI 生态**：与 LLM SDK 集成友好
4. **类型安全**：减少运行时错误

---

## 考虑选项

### 选项 1: Flask

| 维度 | 评估 |
|:---|:---|
| 优点 | 生态成熟，社区大，学习资源多 |
| 缺点 | 异步支持弱（需配合 gevent/eventlet），需手动配置文档 |
| 适用场景 | 传统同步应用 |

### 选项 2: Django

| 维度 | 评估 |
|:---|:---|
| 优点 | 全功能框架，ORM、Admin 等开箱即用 |
| 缺点 | 太重，不适合微服务/小型服务，异步支持较晚 |
| 适用场景 | 大型单体应用 |

### 选项 3: FastAPI

| 维度 | 评估 |
|:---|:---|
| 优点 | 原生异步、自动生成 OpenAPI 文档、Pydantic 验证、类型提示 |
| 缺点 | 相对较新，部分第三方中间件生态不如 Flask |
| 适用场景 | API 服务、微服务、AI 应用 |

### 选项 4: Go (Gin/Echo)

| 维度 | 评估 |
|:---|:---|
| 优点 | 性能最好，静态类型，编译部署方便 |
| 缺点 | 开发效率不如 Python，AI 生态较弱 |
| 适用场景 | 极致性能要求的场景 |

---

## 决定

选择 **FastAPI** 作为主力框架，Go 作为特定高性能场景的补充。

### 决策矩阵

| 项目类型 | 推荐框架 | 理由 |
|:---|:---|:---|
| AI API 服务 | FastAPI | 与 OpenAI/Anthropic SDK 集成友好 |
| 实时通信 | FastAPI + WebSocket | 原生异步支持 |
| 高并发网关 | Go (Gin) | 极致性能 |
| 数据爬虫/脚本 | Python + httpx | 生态丰富 |

---

## 实施细节

### 统一的 FastAPI 项目模板

见 `templates/base-python/`

```python
# 关键配置
app = FastAPI(
    title="{project_name}",
    description="{project_description}",
    version="0.1.0",
    lifespan=lifespan,  # 优雅的启停管理
)
```

### 开发规范

1. **类型注解**：100% 覆盖
2. **Pydantic Models**：用于所有输入/输出验证
3. **依赖注入**：使用 FastAPI 的 Depends
4. **异步优先**：默认使用 `async def`

---

## 后果

### 正面

- 开发速度提升 30%+（自动生成文档）
- 类型安全减少运行时错误
- 异步支持为未来高并发场景留有余地

### 负面

- 团队需要适应 Python 类型提示
- 部分老旧库可能不支持异步

---

## 相关链接

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [模板代码](../templates/base-python/)
