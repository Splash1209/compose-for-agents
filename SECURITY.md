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