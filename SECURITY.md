# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in `asset-marketplace-client-core`, please report it responsibly.

### How to Report

**Please DO NOT open a public GitHub issue for security vulnerabilities.**

Instead, please use one of these methods:

1. **GitHub Security Advisories** (Preferred)
   - Go to: https://github.com/brentlopez/asset-marketplace-client-core/security/advisories
   - Click "Report a vulnerability"
   - Provide detailed information about the vulnerability

2. **Email** (Alternative)
   - Contact the maintainer directly
   - Include "SECURITY" in the subject line
   - Provide detailed information about the vulnerability

### What to Include

When reporting a vulnerability, please include:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Affected versions**
- **Potential impact** assessment
- **Suggested fix** (if you have one)
- **Your contact information** (for follow-up)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Assessment**: We will assess the vulnerability within 7 days
- **Updates**: We will keep you informed of progress
- **Resolution**: We aim to release a fix within 30 days for critical issues
- **Credit**: We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices for Users

### For Platform Implementers

If you're building a platform-specific client using this library:

1. **Credential Management**
   - Never hardcode API keys, tokens, or credentials
   - Use environment variables or secure credential stores
   - Implement credential rotation where possible

2. **Input Validation**
   - Always validate user inputs before passing to library methods
   - Use the provided `sanitize_filename()` and `validate_url()` utilities
   - Validate asset UIDs match expected formats

3. **Path Security**
   - Validate download output directories
   - Prevent directory traversal attacks
   - Use `Path.resolve()` to normalize paths
   - Example:
     ```python
     from pathlib import Path
     
     def safe_download_path(base_dir: Path, filename: str) -> Path:
         """Ensure download path doesn't escape base directory."""
         # Sanitize the filename
         safe_name = sanitize_filename(filename)
         
         # Resolve the full path
         full_path = (base_dir / safe_name).resolve()
         
         # Verify it's still within base_dir
         if not str(full_path).startswith(str(base_dir.resolve())):
             raise MarketplaceValidationError("Path traversal detected")
         
         return full_path
     ```

4. **Network Security**
   - Always use HTTPS for API endpoints
   - Verify SSL certificates (don't disable verification)
   - Implement proper timeout values
   - Handle rate limiting appropriately

5. **Error Handling**
   - Don't expose sensitive information in error messages
   - Log security events appropriately
   - Never log credentials, tokens, or PII

6. **Dependencies**
   - Keep your HTTP library (requests, httpx, etc.) up to date
   - Run regular security audits with `pip-audit` or `safety`
   - Monitor security advisories for your dependencies

### For End Users

1. **Keep Updated**
   - Use the latest version of the library
   - Subscribe to security advisories via GitHub

2. **Secure Storage**
   - Store credentials securely
   - Don't commit `.env` files or credentials to version control

3. **Network Security**
   - Use secure networks when accessing marketplace APIs
   - Be cautious of man-in-the-middle attacks

## Security Features

This library is designed with security in mind:

- ✅ **Zero runtime dependencies** - Minimal attack surface
- ✅ **Type-safe** - Full mypy strict mode compliance prevents many bugs
- ✅ **Input validation** - Built-in utilities for sanitizing filenames and validating URLs
- ✅ **Secure defaults** - No unsafe operations (eval, exec, pickle, shell commands)
- ✅ **Clear abstractions** - Security-sensitive operations delegated to platform implementations

## Known Security Considerations

### This Library

- This is an **abstract library** providing base classes
- Platform implementations are responsible for:
  - Secure credential management
  - Network security (TLS/SSL)
  - Rate limiting
  - Request signing/authentication
  - Data validation

### Not Provided

This library intentionally does NOT provide:
- Authentication implementations (platform-specific)
- Network request handling (platform-specific)
- Credential storage (platform-specific)

These are delegated to platform implementations to allow flexibility while maintaining security boundaries.

## Acknowledgments

We appreciate the security research community and will acknowledge security researchers who responsibly disclose vulnerabilities.

## Questions?

If you have questions about the security of this library, please open a GitHub Discussion or contact the maintainers.

---

**Last Updated:** 2025-12-23
