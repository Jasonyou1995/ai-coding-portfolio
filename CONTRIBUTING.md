# 贡献指南

感谢您对 AI Coding Portfolio 的关注！本指南帮助您了解如何参与项目。

---

## 🎯 项目目标

这是一个**个人学习作品集**，主要目的是：

1. **系统化学习** AI 辅助编程
2. **展示工程能力** 给潜在雇主
3. **记录成长轨迹** 从基础到架构

---

## 📋 贡献类型

### 1. Bug 报告

如果发现代码问题或安全漏洞，请提交 Issue：

```markdown
**问题描述**
清晰描述问题

**复现步骤**
1. 进入项目 XXX
2. 执行命令 ...
3. 看到错误 ...

**期望行为**
应该发生什么

**环境信息**
- Python 版本:
- OS:
```

### 2. 改进建议

欢迎提出架构、性能或文档改进建议。

### 3. 代码贡献

⚠️ **注意**: 由于是个人作品集，代码贡献可能不会被合并，但您的建议仍然有价值！

---

## 🔒 安全报告

如果发现敏感信息泄露或安全漏洞，请：

1. **不要** 在公开 Issue 中披露
2. 发送邮件至: security@example.com
3. 等待修复后再公开

---

## 📝 代码规范

### Python 代码风格

```python
# ✅ 推荐
from typing import Optional

def get_user(user_id: str) -> Optional[User]:
    """Get user by ID.
    
    Args:
        user_id: The unique user identifier.
        
    Returns:
        User object if found, None otherwise.
    """
    return db.query(User).filter(User.id == user_id).first()

# ❌ 不推荐
def get_user(id):
    return db.query(User).filter(User.id==id).first()
```

### 提交信息规范

```bash
# 格式
<type>(<scope>): <subject>

<body>

<footer>

# 示例
feat(auth): 实现 JWT 认证

- 添加 access token 和 refresh token
- 实现 token 刷新机制
- 增加 token 黑名单

Closes #123
```

#### 类型说明

| 类型 | 说明 | 示例 |
|:---|:---|:---|
| `feat` | 新功能 | `feat: 添加用户注册` |
| `fix` | 修复 | `fix: 修复登录接口 500 错误` |
| `docs` | 文档 | `docs: 更新 API 文档` |
| `style` | 格式 | `style: 格式化代码` |
| `refactor` | 重构 | `refactor: 优化查询性能` |
| `test` | 测试 | `test: 添加用户服务测试` |
| `chore` | 构建 | `chore: 更新依赖` |

---

## 🧪 开发流程

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/yourname/ai-coding-portfolio.git
cd ai-coding-portfolio

# 安装 pre-commit
pip install pre-commit
pre-commit install
```

### 2. 创建新功能分支

```bash
git checkout -b feat/new-feature
```

### 3. 开发和测试

```bash
# 运行测试
cd projects/01-smart-mailbox
pytest --cov=src

# 代码检查
ruff check .
black --check .
mypy src/
```

### 4. 提交代码

```bash
git add .
git commit -m "feat: 添加新功能"
git push origin feat/new-feature
```

---

## 📊 项目标准

每个项目必须满足：

- [ ] **可运行**: `docker-compose up` 能启动
- [ ] **有测试**: 单元测试覆盖率 > 80%
- [ ] **有文档**: README 包含架构、API、迭代记录
- [ ] **有 ADR**: 技术决策记录
- [ ] **无敏感信息**: 通过安全扫描
- [ ] **符合规范**: 通过 Black、Ruff、MyPy

---

## 🎓 学习建议

如果您也想创建类似的作品集：

1. **Fork 本仓库** 作为起点
2. **阅读 `docs/learning-path.md`** 了解学习路线
3. **参考 `templates/`** 使用项目模板
4. **记录迭代过程** 展示思考轨迹

---

## 📞 联系方式

- GitHub Issues: [新建 Issue](../../issues/new)
- Email: your.email@example.com

---

## 🙏 致谢

感谢所有提供建议和反馈的朋友！
