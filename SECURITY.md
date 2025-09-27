# Security Policy

## ⚠️ IMPORTANT SECURITY NOTICE

This repository contains demo applications for educational purposes. **DO NOT use default configurations in production environments.**

## Security Guidelines

### 🔒 Before Running Any Demo

1. **Change ALL default passwords** before running any compose configuration
2. **Never commit secrets** to version control
3. **Use environment variables** for all sensitive configuration
4. **Review network exposure** of all services

### 🛡️ Required Security Steps

#### 1. Database Security
- **MongoDB**: Set strong `MONGO_ROOT_PASSWORD` environment variable
- **MySQL**: Set strong `MYSQL_ROOT_PASSWORD` environment variable
- **Never use default passwords** like "password" or empty passwords

#### 2. API Keys and Tokens
- Copy `.env.template` files to `.env` in each demo directory
- Set your actual API keys in `.env` files
- Ensure `.env` files are in `.gitignore` (they are by default)

#### 3. Network Security
- Database ports are exposed for demo purposes
- In production: Use internal networks, no exposed ports
- Consider using Docker secrets for production deployments

#### 4. File Permissions
- Ensure secret files have restricted permissions (600)
- Review volume mounts for sensitive data exposure

### 🚨 Never Commit These Files

- `.env` files with real credentials
- `secret.*` files
- API key files
- Database dumps or backups
- Private keys or certificates

### 🔍 Security Checklist

Before sharing or deploying:

- [ ] All default passwords changed
- [ ] No hardcoded secrets in files
- [ ] Environment variables used for sensitive config
- [ ] .env files excluded from git
- [ ] Database credentials are strong (16+ chars, mixed case, numbers, symbols)
- [ ] Network access reviewed and restricted as needed

### 📊 Demo vs Production

| Aspect | Demo Configuration | Production Configuration |
|--------|-------------------|------------------------|
| Passwords | Environment variables | Strong, rotated regularly |
| Network | Exposed ports for testing | Internal networks only |
| Secrets | Local .env files | Container orchestration secrets |
| TLS | Often disabled | Always enabled |
| Monitoring | Basic logs | Full security monitoring |

### 🐛 Reporting Security Issues

If you find security vulnerabilities:

1. **DO NOT** open a public issue
2. Contact the repository maintainers privately
3. Provide detailed description of the vulnerability
4. Allow time for fixes before disclosure

### 📚 Additional Resources

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Compose Security Guidelines](https://docs.docker.com/compose/security/)
- [OWASP Container Security](https://owasp.org/www-project-container-security/)

---

**Remember: These are demo applications. Always implement proper security measures for production use.**
## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |


## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a
reported vulnerability, what to expect if the vulnerability is accepted or
declined, etc.


## Security Considerations for Agents

When developing and deploying agent-based applications, several security considerations must be taken into account:

### Input Validation

All input to agents should be properly validated and sanitized:

- Validate all user inputs before processing
- Sanitize data received from external sources
- Implement rate limiting to prevent abuse
- Use allowlists for acceptable input formats where possible

### Authentication and Authorization

Proper authentication and authorization mechanisms should be implemented:

- Use strong authentication methods
- Implement role-based access control (RBAC)
- Regularly rotate API keys and secrets
- Monitor for unauthorized access attempts

### Data Protection

Sensitive data must be properly protected:

- Encrypt data in transit and at rest
- Implement proper key management
- Use secure communication protocols
- Regularly backup sensitive data

### Network Security

Network communications should be secured:

- Use HTTPS/TLS for all communications
- Implement proper firewall rules
- Use VPNs for sensitive communications
- Monitor network traffic for anomalies

### Container Security

When using containerized deployments:

- Use minimal base images
- Regularly update container images
- Scan images for vulnerabilities
- Implement proper container isolation
- Use read-only filesystems where possible

### Monitoring and Logging

Implement comprehensive monitoring and logging:

- Log all security-relevant events
- Monitor for suspicious activities
- Set up alerting for security incidents
- Regularly review security logs
- Implement centralized logging

### Third-party Dependencies

Manage third-party dependencies securely:

- Regularly update dependencies
- Scan dependencies for known vulnerabilities
- Use dependency pinning
- Monitor for security advisories
- Implement software composition analysis

**Remember: These are demo applications. Always implement proper security measures for production use.**

## Supported Versions

The following table shows which versions of this project are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :x:                |
| 1.4.x   | :white_check_mark: |
| < 1.4   | :x:                |

For more information about security updates, please refer to our release notes and changelog.