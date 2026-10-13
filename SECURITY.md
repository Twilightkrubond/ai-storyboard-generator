# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.9.x   | yes       |
| < 0.9   | no        |

## Reporting a vulnerability

Open a private security advisory on GitHub, or email
`security@fridgecut.dev`. Do not open a public issue for anything that
involves arbitrary code execution, path traversal through project files,
or credential leakage from `config/local.toml`.

Expect a first reply within 72 hours. We are a small team; we ship fixes
as patch releases on the 0.9.x line.

## Threat model notes

- `.sbproj` project files are untrusted input. The loader validates paths
  against the project root and refuses absolute paths outside it.
- Remote image backends are user-configured. We never ship default API
  keys and never log request bodies above `DEBUG`.
- The native extension (`storyboard/native/`) does no I/O; it is pure
  image math. Review it as such.