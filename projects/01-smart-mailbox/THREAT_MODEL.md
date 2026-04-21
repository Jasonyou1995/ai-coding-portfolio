# Threat Model

This document maps concrete threats to the Smart Mailbox system requirements using the STRIDE framework. Each threat is specific to our custom JSON-over-TLS email architecture, attachment-dedup storage, and CLI client stack.

---

## Spoofing

### S001 — Cross-Domain Sender Address Forgery
- **Attack Scenario**: An attacker operating a peer server (e.g., `domain-b.com`) constructs a JSON envelope with `From: admin@domain-a.com` and relays it to `domain-a.com`. Because the custom protocol does not inherit SMTP’s SPF/DKIM/DMARC chain, the receiving server accepts the forged origin and the victim client displays the message as genuinely from the domain administrator.
- **Affected Asset**: User trust / Inbox integrity (spec: 初级钓鱼/垃圾邮件识别).
- **Mitigation**: The originating server MUST sign every outbound JSON envelope with an Ed25519 domain key. The receiving server validates the signature against a pinned public-key whitelist before acceptance. The client renders a verified-domain badge and flags any message lacking a valid signature as **Unverified**.
- **Residual Risk**: If a legitimate peer server is compromised and its signing key exfiltrated, the attacker can still spoof senders within that compromised domain.

### S002 — Session Token Replay on Stolen Client Device
- **Attack Scenario**: Malware or physical theft extracts the CLI client’s session token from its local config file (`~/.smartmail/session.json`). The attacker replays the token in a handcrafted JSON request to the server API, impersonating the victim to send emails or read the inbox without knowing the password.
- **Affected Asset**: User account / Session integrity (spec: 用户在进行密码登录后，保障其和服务器之间进行的无需验证的交互的安全性).
- **Mitigation**: Bind every access token to a device fingerprint (hash of OS username + hostname + client ephemeral salt) at issuance. The server rejects requests where the presented token does not match the stored fingerprint. Access tokens expire after 15 minutes and are refreshed with a single-use rotation policy.
- **Residual Risk**: An attacker with live memory access on the victim’s machine can intercept tokens from RAM or hijack the active TLS connection directly.

---

## Tampering

### T001 — Inter-Server JSON Payload Modification in Transit
- **Attack Scenario**: An attacker positioned on the network path between Server A and Server B performs a TLS downgrade or compromises a certificate, then modifies the relayed JSON body to inject a malicious attachment reference or alter the `Subject` field before the message reaches the destination server.
- **Affected Asset**: Email content integrity / Cross-domain message authenticity (spec: 两个域名服务器互发邮件成功).
- **Mitigation**: Enforce TLS 1.3 with certificate pinning for all inter-server sockets. Wrap the JSON payload in an authenticated envelope that includes an HMAC-SHA256 tag computed with a pre-shared inter-server symmetric key and a monotonic nonce to prevent replay and bit-flipping.
- **Residual Risk**: If the server’s private TLS key or the pre-shared symmetric key is exfiltrated, the attacker can forge valid authenticated envelopes.

### T002 — Unauthorized Recall of Another User’s Message
- **Attack Scenario**: After Alice sends an email to Bob, attacker Eve intercepts or fabricates a `RECALL` JSON request and changes the `message_id` parameter to target a message that Bob previously sent to Alice. If the server only checks authentication but not ownership, Bob’s message is silently deleted.
- **Affected Asset**: Email availability / Ownership integrity (spec: 撤回邮件的核验，防止指令错误执行).
- **Mitigation**: The recall endpoint MUST verify that the `message_id` exists in the authenticated sender’s **Outbox** table and that the `sender` field in the stored record matches the session user. A server-side HMAC over the recall command (including message_id and timestamp) is validated before execution, and the action is logged immutably.
- **Residual Risk**: If the victim’s session is hijacked (token stolen), the attacker can legitimately recall the victim’s own emails, which is indistinguishable from a valid user action.

---

## Repudiation

### R001 — Sender Denies Authorship of a Sent Email
- **Attack Scenario**: A user sends a harassing or fraudulent email, then claims the server database was tampered with or that their account was compromised, denying responsibility and preventing disciplinary or legal action.
- **Affected Asset**: Audit trail / Legal accountability (spec: 威胁模型与防护说明).
- **Mitigation**: The server appends every delivered message to an append-only log backed by a sequential HMAC chain: each entry contains the previous entry’s HMAC, timestamp, sender ID, recipient ID, and SHA-256 content hash, all signed with a server audit key. Clients receive a signed delivery receipt containing the log sequence number.
- **Residual Risk**: If the server audit signing key is compromised, an attacker can forge backdated log entries or fabricated receipts.

### R002 — Operator Repudiates a Recall Action by Purging Logs
- **Attack Scenario**: A privileged user or compromised server operator executes a sensitive recall action and subsequently deletes or truncates the corresponding audit rows in the SQLite database to hide the evidence.
- **Affected Asset**: Recall audit log (spec: 撤回邮件的核验).
- **Mitigation**: Implement an append-only SQLite audit table with a write-once trigger (`ON DELETE RESTRICT`) and mirror critical events (send, recall, login failures) to client-side offline receipts that users can export and compare against server claims.
- **Residual Risk**: A root-level compromise on the host can bypass filesystem permissions, delete the SQLite file entirely, or disable write-once triggers.

---

## Information Disclosure

### I001 — Cross-User File Existence Leak via Deduplication Timing
- **Attack Scenario**: An attacker uploads a sensitive file (e.g., a confidential contract PDF) and observes that the server responds instantly and consumes zero additional storage quota. By correlating upload latency and quota deltas across many files, the attacker infers that another user (or the organization) already possesses the same file.
- **Affected Asset**: User attachment confidentiality / Metadata privacy (spec: 存储空间优化（例如附件去重、同时需要考虑文件安全）).
- **Mitigation**: Use a keyed hash (`HMAC-SHA256` with a server-side secret) for the deduplication lookup instead of a raw content hash. Pad all upload responses to constant time and always report a synthetic storage delta (e.g., average file size) regardless of whether a dedup hit occurs.
- **Residual Risk**: Sophisticated side-channel analysis (network jitter, CPU load, or cache timing) may still reveal deduplication hits under prolonged statistical measurement.

### I002 — Database Theft Exposes Weakly Protected Attachments
- **Attack Scenario**: An attacker gains read access to the server host and copies the SQLite database and the attachment storage directory. Because attachments are stored as plaintext files named by hash, the attacker can reconstruct all email content and exfiltrate every user’s images and documents.
- **Affected Asset**: Email body and attachment data at rest (spec: 账户敏感信息保护).
- **Mitigation**: Encrypt each attachment with AES-256-GCM using a per-user key derived from the user’s password via Argon2id. Only ciphertext is stored on disk; the deduplication index maps the keyed hash to an encrypted blob ID without exposing plaintext content.
- **Residual Risk**: If a user’s password is weak and cracked offline, the derived key can decrypt that user’s attachments; a live server compromise can exfiltrate keys from memory during active sessions.

---

## Denial of Service (DoS)

### D001 — Brute-Force Storm Locks Out Legitimate User
- **Attack Scenario**: An attacker distributes a coordinated dictionary attack against a high-value account (e.g., `ceo@domain-a.com`) from thousands of IPs. The aggressive rate-limiting triggers a hard account lockout, denying access to the real user and forcing them through an unbounded unlock process.
- **Affected Asset**: Account availability / Server compute resources (spec: 登录防爆破（限流、短期封禁、验证码等）).
- **Mitigation**: Implement dual rate-limiting: IP-based leaky bucket (100 req/min) and account-based progressive exponential backoff (5 failures → 1 min → 5 min → 15 min). After the 3rd failure, present a CAPTCHA challenge instead of a hard lock, keeping the account accessible to humans while throttling bots.
- **Residual Risk**: A large botnet rotating IPs and solving CAPTCHAs (via cheap solving services) can still cause intermittent service degradation or force repeated human verification hurdles.

### D002 — Storage Exhaustion via Unique-File Flood
- **Attack Scenario**: An attacker scripts the client to generate millions of unique 1-byte files and uploads them as attachments. Because each file has a unique hash, deduplication provides no savings, and the attacker fills the server’s disk quota or exhausts the inode pool, preventing all other users from sending attachments.
- **Affected Asset**: Server storage availability (spec: 客户端防滥发/DOS 的基础防护 & 附件去重).
- **Mitigation**: Enforce per-user daily upload quotas (100 MB), per-file minimum size (1 KB), and a global storage watermark (alert at 80%, hard stop at 95%). Store attachments in size-tiered sharded directories to limit inode pressure.
- **Residual Risk**: A distributed attack from many sleeper accounts could exhaust aggregate storage faster than the global watermark triggers an administrative response.

---

## Elevation of Privilege

### E001 — Insecure Direct Object Reference in Inbox Lookup
- **Attack Scenario**: Authenticated user Alice manipulates the `GET_INBOX` JSON payload, changing the `user_id` field from `alice` to `bob`. If the server naively trusts the client-provided identifier instead of deriving it from the session token, Bob’s entire inbox is returned to Alice.
- **Affected Asset**: User mailbox data / Authorization boundary (spec: 两个系统存储应逻辑隔离).
- **Mitigation**: Enforce strict server-side authorization on every endpoint: extract `user_id` exclusively from the cryptographically verified session token payload, never from client JSON fields. Use parameterized queries for all mailbox lookups and enforce row-level ownership checks (`WHERE owner = :session_user`).
- **Residual Risk**: A server-side logic bug or SQL injection in a secondary lookup path could still bypass the authorization layer.

### E002 — Malicious Script Injection in Rich-Text Email Body
- **Attack Scenario**: An attacker sends an HTML email containing embedded `<script>` tags, `javascript:` URIs, or malicious ANSI escape sequences. When the CLI client renders the message body in a rich preview pane or pipes it to an external pager/browser, the script executes with the client’s OS user privileges, potentially reading local files or session tokens.
- **Affected Asset**: Client host integrity / User privileges (spec bonus: 思考是否恶意用户有可能在邮件中加入恶意脚本，造成破坏结果).
- **Mitigation**: Sanitize all incoming HTML with a strict allowlist (plain text, `<p>`, `<br>`, `<a>` with `href` validation only). Escape ANSI sequences before terminal rendering. Run the client in a minimal sandbox without shell execution privileges; store session tokens with `0600` permissions and refuse to render remote resources.
- **Residual Risk**: Zero-day vulnerabilities in the terminal emulator or image-rendering libraries used by the CLI client could still allow code execution even after sanitization.

---

## Threat Summary Table

| Threat ID | Category | Phase |
|-----------|----------|-------|
| S001 | Spoofing | Protocol Security |
| S002 | Spoofing | Session / Access Control |
| T001 | Tampering | Protocol Security |
| T002 | Tampering | Application Logic |
| R001 | Repudiation | Audit / Storage |
| R002 | Repudiation | Audit / Storage |
| I001 | Information Disclosure | Storage Security |
| I002 | Information Disclosure | Storage Security |
| D001 | Denial of Service | Application Logic |
| D002 | Denial of Service | Application Logic |
| E001 | Elevation of Privilege | Access Control |
| E002 | Elevation of Privilege | Client Security |
