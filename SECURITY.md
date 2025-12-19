# Security Considerations for MBHB

## Overview

This document outlines security considerations and best practices for the MBHB system.

## Current Security Measures

### 1. Authentication & Authorization
- Admin panel (when implemented) should require authentication
- Consider adding Flask-Login for session management
- Use strong passwords and password hashing (bcrypt/argon2)

### 2. Database Security
- SQLAlchemy ORM prevents SQL injection
- Parameterized queries throughout
- Input validation on all routes

### 3. API Security
- Rate limiting should be added for production
- Input validation on all API endpoints
- CORS configuration if needed for external access

### 4. Secret Key Management
- **Development**: Uses default key (acceptable)
- **Production**: Requires SECRET_KEY environment variable
- Application raises error if SECRET_KEY not set in production mode

### 5. File Upload Security
- Currently accepts JSON files only
- File size limits should be configured
- Path traversal protection in place
- Consider virus scanning for production

## Known Security Considerations

### 1. CDN Dependencies (Low Risk)

**Issue**: Bootstrap and Chart.js loaded from CDN without SRI hashes

**Risk Level**: Low (trusted CDNs, HTTPS)

**Mitigation Options**:
1. Add integrity hashes (recommended for production):
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" 
      rel="stylesheet"
      integrity="sha384-..." 
      crossorigin="anonymous">
```

2. Host assets locally:
```bash
npm install bootstrap chart.js
# Copy to static/ folder
```

3. Use build tool (webpack/vite) to bundle assets

### 2. eval() Usage in Generated Worksheets

**Context**: Worksheet JavaScript uses eval() for mathematical calculations

**Safety**: Only evaluates AI-generated code at generation time, never user input

**Details**: See README.md Security section

### 3. CSRF Protection

**Current**: No CSRF protection implemented

**Recommendation**: Add Flask-WTF for forms:
```python
pip install flask-wtf
app.config['WTF_CSRF_ENABLED'] = True
```

### 4. Rate Limiting

**Current**: No rate limiting

**Recommendation**: Add Flask-Limiter:
```python
pip install Flask-Limiter
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

## Production Deployment Checklist

- [ ] Set SECRET_KEY environment variable (random, secure)
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Configure file upload limits
- [ ] Set up logging and monitoring
- [ ] Regular backups
- [ ] Keep dependencies updated
- [ ] Add integrity hashes to CDN resources
- [ ] Configure firewall rules
- [ ] Use reverse proxy (nginx/Apache)
- [ ] Run security audit (safety, bandit)

## Security Auditing

### Recommended Tools

**Python Dependencies**:
```bash
pip install safety
safety check  # Check for known vulnerabilities
```

**Code Analysis**:
```bash
pip install bandit
bandit -r app/  # Static security analysis
```

**Dependency Updates**:
```bash
pip list --outdated
npm audit
```

## Reporting Security Issues

If you discover a security vulnerability, please email [security contact] instead of creating a public issue.

## Regular Maintenance

1. **Weekly**: Check for dependency updates
2. **Monthly**: Run security scans
3. **Quarterly**: Review access logs
4. **Yearly**: Full security audit

## References

- [Flask Security](https://flask.palletsprojects.com/en/latest/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
