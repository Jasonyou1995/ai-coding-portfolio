# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-21

### Added

- Expand threat model with full STRIDE analysis (S001–E002) covering attack scenarios, mitigations, and residual risks.
- Document security and design decisions: custom JSON-over-TLS protocol, per-server SQLite storage, Argon2id password hashing, session token + HMAC refresh rotation, keyed deduplication, and AES-256-GCM attachment encryption.

### Changed

- Update and replace initial ADRs with concrete security/design decision records.
- Normalize file permissions across the repository (644 → 755) for executable scripts and templates.

## [0.1.0-alpha] - 2026-04-20

### Added

- Add project templates and initial project scaffolding for Smart Mailbox.
- Establish repository structure with `server/`, `client/`, `common/`, `tests/`, `scripts/`, and `docs/` directories.
- Introduce wire protocol V0.1 with NDJSON message format (`HELLO`, `RELAY_MAIL`, `ACK`) in `common/protocol.py`.
- Add pytest suite with round-trip encoding/decoding and validation tests in `tests/test_protocol.py`.

## [0.0.1] - 2026-03-27

### Added

- Initial repository setup and base templates.
