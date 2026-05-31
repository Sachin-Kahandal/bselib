# Security Policy

## Supported versions

bselib is a small, educational library. Security fixes are applied to the latest released
version only.

| Version | Supported |
|---------|-----------|
| latest  | ✅        |
| older   | ❌        |

## Reporting a vulnerability

Please report security issues privately rather than opening a public issue:

- Use GitHub's [private vulnerability reporting](https://github.com/Sachin-Kahandal/bselib/security/advisories/new), or
- email the maintainer at sachinkahandal142@gmail.com.

Please include reproduction steps and the affected version. You can expect an initial
response within a couple of weeks.

## Scope and caveats

bselib scrapes third-party websites and returns their data largely unmodified. Treat any
fetched content as untrusted input in your own application. The library performs no
authentication and stores no secrets; do not commit credentials when contributing.
