# ADR-002: 安全与隐私保护策略

**状态**: 已接受 ✅  
**日期**: 2024-03-27  
**作者**: @yourname

---

## 背景

作为公开的代码作品集，必须确保：

1. **不泄露个人敏感信息**（真实姓名、联系方式、地址等）
2. **不泄露 API Keys 和凭证**
3. **不泄露前公司内部信息**
4. **展示安全意识**

---

## 安全分级清单

### 🔴 绝对保护（禁止提交）

```gitignore
# 凭证与密钥
.env
*.key
*.pem
config/secrets.yaml
**/credentials/

# 个人敏感信息
**/personal_data/
**/real_data/
resume_real.*
cv_real.*

# 日志（可能含敏感信息）
logs/
*.log
```

### 🟡 脱敏处理（提交前检查）

| 内容 | 处理方式 | 示例 |
|:---|:---|:---|
| 真实邮箱 | 替换为占位符 | `user@example.com` |
| 真实手机号 | 部分隐藏 | `138****8888` |
| API Key | 环境变量 + 示例文件 | `.env.example` |
| 真实姓名 | 使用 GitHub 昵称 | `@yourname` |
| 服务器 IP | 泛化处理 | `<your-domain>` |
| 公司数据 | Mock 数据 | Faker 生成 |

### 🟢 刻意展示（证明安全意识）

- 错误处理与日志脱敏
- 输入验证与 SQL 注入防护
- 密码 bcrypt 加密存储
- JWT Token 安全设计
- 速率限制实现

---

## 实施规范

### 1. 环境变量管理

```bash
# .env.example（提交到 Git）
DATABASE_URL=postgresql://user:password@localhost/db
SECRET_KEY=your-secret-key-here

# .env（本地保存，不提交）
DATABASE_URL=postgresql://real_user:real_pass@real-host/db
SECRET_KEY=real-secret-key
```

### 2. 日志脱敏

```python
# ❌ 错误：记录敏感信息
logger.info(f"User login: {email}, password: {password}")

# ✅ 正确：脱敏处理
logger.info(f"User login attempt: {email[:3]}***")
```

### 3. Mock 数据生成

```python
from faker import Faker

fake = Faker()

# 生成假数据用于测试
def generate_mock_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
    }
```

### 4. 预提交检查

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: check-env-files
        name: Check for .env files
        entry: bash -c 'if git diff --cached --name-only | grep -q "\.env$"; then echo "Error: .env file detected!"; exit 1; fi'
        language: system
```

---

## 验证清单

每个项目提交前必须检查：

- [ ] `.env` 文件在 `.gitignore` 中
- [ ] 所有 API Keys 已替换为占位符
- [ ] 真实邮箱/手机号已脱敏
- [ ] 日志中不含敏感信息
- [ ] README 中声明"所有数据均为 Mock"

---

## 相关链接

- [根目录 .gitignore](../.gitignore)
- [GitHub 安全最佳实践](https://docs.github.com/en/code-security)
