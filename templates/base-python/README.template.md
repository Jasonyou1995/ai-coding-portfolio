# {project_name}

> {project_description}

## 📋 项目信息

| 属性 | 内容 |
|:---|:---|
| **项目编号** | {project_number} |
| **类型** | {project_type} |
| **技术栈** | {tech_stack} |
| **难度** | {difficulty} |
| **预计工期** | {estimated_days} 天 |

---

## 🎯 项目目标

{project_goals}

---

## 🏗️ 系统架构

```
{ascii_architecture_diagram}
```

---

## 📁 项目结构

```
{project_folder}/
├── src/                    # 源代码
│   ├── __init__.py
│   ├── main.py            # 入口文件
│   └── core/              # 核心逻辑
├── tests/                  # 测试代码
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py
├── docs/                   # 文档
│   ├── arch.png           # 架构图
│   └── decisions.md       # 技术决策记录(ADR)
├── scripts/                # 脚本工具
├── .env.example           # 环境变量示例
├── requirements.txt       # Python依赖
├── pyproject.toml         # 项目配置
├── Dockerfile             # 容器配置
├── docker-compose.yml     # 本地开发环境
└── README.md              # 本文件
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Docker (可选)

### 本地开发

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的配置

# 4. 运行测试
pytest --cov=src --cov-report=html

# 5. 启动服务
python src/main.py
```

### Docker 方式

```bash
# 构建并启动
docker-compose up --build

# 运行测试
docker-compose exec app pytest
```

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 带覆盖率报告
pytest --cov=src --cov-report=html

# 运行特定测试
pytest tests/test_main.py -v
```

---

## 📝 迭代记录

### v0.1 (Day 1-2)
- {initial_implementation_notes}
- 遇到的问题：{problems_encountered}
- 解决方案：{solutions_applied}

### v0.2 (Day 3)
- {iteration_notes}

---

## 📊 性能测试

```bash
# 运行压测（示例）
wrk -t12 -c400 -d30s http://localhost:8000/api/endpoint
```

| 指标 | 数值 |
|:---|:---|
| QPS | {qps_value} |
| 平均延迟 | {latency_ms} ms |
| P99 延迟 | {p99_ms} ms |

---

## 🔧 技术决策 (ADR)

见 [docs/decisions.md](./docs/decisions.md)

---

## 📚 参考资料

- {reference_links}

---

## ⚠️ 隐私声明

本项目所有数据均为 Mock 数据，不含任何真实个人信息。
