# Design Decisions (ADRs)

## ADR-001: Language Choice
- **Context**: Need for rapid development with strong standard libraries and modern security features.
- **Decision**: Python 3.11+.
- **Consequences**: Easy access to modern crypto primitives and type hinting for safety.

## ADR-002: Transport Layer
- **Context**: The specification forbids mature email libraries.
- **Decision**: Raw TCP sockets wrapped in TLS.
- **Consequences**: Requires custom protocol implementation but ensures full control over security handshake.

## ADR-003: Storage Strategy
- **Context**: Requirement for logical isolation between server instances.
- **Decision**: SQLite (one separate file per server instance).
- **Consequences**: High performance for single-user scenarios and easy backup/isolation via file system.

## ADR-004: Cryptography Library
- **Context**: Need to implement security protocols from scratch using vetted primitives.
- **Decision**: `cryptography` library (primitives only).
- **Consequences**: Prevents "reinventing the wheel" for basic ciphers while allowing custom higher-level protocol design.

## ADR-005: User Interface
- **Context**: Priority is on the security skeleton rather than web presentation.
- **Decision**: Command Line Interface (CLI) client.
- **Consequences**: Faster development of core functionality and easier testing/automation.
