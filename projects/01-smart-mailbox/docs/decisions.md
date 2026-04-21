# 技术决策记录 - Smart Mailbox

## ADR-001: 为什么从 Session 迁移到 JWT?

**状态**: 已接受 ✅  
**日期**: 2026-03-27

### 背景

v0.1 版本使用服务端 Session 存储用户状态，在扩展时遇到问题。

### 考虑选项

| 选项 | 优点 | 缺点 |
|:---|:---|:---|
| Session (Redis) | 服务端可控，可主动失效 | 需要额外存储，跨域复杂 |
| JWT | 无状态，天然支持跨域 | Token 无法提前失效 |
| Session + JWT 混合 | 兼顾两者优点 | 实现复杂 |

### 决定

选择 **JWT**，使用短有效期 Access Token + Refresh Token 模式。

```python
# 实现要点
ACCESS_TOKEN_EXPIRE = 15  # 分钟
REFRESH_TOKEN_EXPIRE = 7  # 天
```

### 后果

- 服务无状态，易于水平扩展
- 需要前端实现 Token 刷新逻辑

---

## ADR-002: 限流算法选择

**状态**: 已接受 ✅  
**日期**: 2026-03-27

### 考虑选项

1. **固定窗口**：实现简单，但可能有突发流量
2. **滑动窗口**：平滑，但实现复杂
3. **令牌桶**：允许突发，平滑限流
4. **漏桶**：严格限速，不适合突发

### 决定

选择 **令牌桶算法**，基于 Redis 实现。

```python
# 核心逻辑
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity      # 桶容量
        self.refill_rate = refill_rate  # 每秒填充速率
```

### 配置

| 接口 | 限流 | 理由 |
|:---|:---|:---|
| POST /login | 5/分钟 | 防暴力破解 |
| POST /register | 3/小时 | 防批量注册 |
| API 通用 | 100/分钟 | 正常访问 |

---

## ADR-003: 为什么不用现成的 Celery?

**状态**: 已接受 ✅  
**日期**: 2026-03-27

### 背景

需要实现邮件群发队列功能。

### 考虑选项

1. **Celery + Redis**：功能全面，监控完善
2. **RQ**：轻量，但监控能力弱
3. **自研基于 Redis 的队列**：代码 <200 行，完全可控

### 决定

选择 **自研轻量队列**，代码在 `core/queue.py`。

理由：
- 需求简单，Celery 太重
- 学习目的，理解队列原理
- 代码可控，易于调试

```python
# 简化版实现
class SimpleQueue:
    def push(self, task: dict) -> str:
        task_id = generate_id()
        self.redis.lpush(self.queue_key, json.dumps(task))
        return task_id
    
    def pop(self, timeout: int = 5) -> Optional[dict]:
        result = self.redis.brpop(self.queue_key, timeout)
        return json.loads(result[1]) if result else None
```

### 压测结果

- 1000 任务/秒无丢失
- 内存占用 < 50MB

---

## ADR-004: 端到端加密方案

**状态**: 已接受 ✅  
**日期**: 2026-03-27

### 需求

- 邮件内容加密存储
- 只有收发双方可解密
- 服务端无法读取明文

### 方案

使用 **AES-256-GCM** 对称加密：

```
加密流程：
1. 客户端生成随机密钥 (per-message key)
2. 用收件人公钥加密密钥
3. 用密钥加密邮件内容
4. 存储：加密内容 + 加密密钥 + IV + Tag
```

### 代码示例

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_email(content: str, recipient_public_key: bytes) -> EncryptedEmail:
    # 生成随机密钥
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    
    # 加密内容
    iv = os.urandom(12)
    ciphertext = aesgcm.encrypt(iv, content.encode(), None)
    
    # 用 RSA 加密密钥
    encrypted_key = rsa_encrypt(key, recipient_public_key)
    
    return EncryptedEmail(
        ciphertext=ciphertext,
        encrypted_key=encrypted_key,
        iv=iv,
    )
```

### 限制

- 当前仅支持文本内容加密
- TODO: 附件加密
