# Security Policy

## Supported Versions

This repository contains demonstrations and examples for multi-agent systems using
various agent frameworks. Security updates are provided for the current `main`
branch and the most recent stable releases of each demo.

| Component | Supported          |
| --------- | ------------------ |
| main branch | :white_check_mark: |
| Latest demos | :white_check_mark: |
| Docker configurations | :white_check_mark: |
| Archived/legacy demos | :x: |

## Reporting a Vulnerability

If you discover a security vulnerability in any of the agent demos or
configurations, please help us maintain the security of the project by reporting
it responsibly.

### Where to Report

**For security vulnerabilities, please use GitHub Security Advisories:**

1. Go to the [Security tab](https://github.com/Splash1209/compose-for-agents/security)
   of this repository
2. Click "Report a vulnerability"
3. Fill out the security advisory form with details about the vulnerability

**For less critical security concerns, you can:**

- Open a regular issue on GitHub (for configuration recommendations, best practices, etc.)
- Contact the maintainers directly through GitHub

### What to Include

When reporting a vulnerability, please include:

- **Description**: A clear description of the vulnerability
- **Location**: Which demo/component is affected
- **Impact**: Potential security impact and attack scenarios
- **Reproduction**: Steps to reproduce the issue
- **Suggested Fix**: If you have ideas for how to resolve the issue

### Response Timeline

- **Initial Response**: We aim to acknowledge receipt within **48 hours**
- **Assessment**: Initial assessment and triage within **5 business days**
- **Updates**: Regular updates every **7 days** until resolution
- **Resolution**: We strive to resolve critical vulnerabilities within **30 days**

### What to Expect

**If the vulnerability is accepted:**

- We'll work with you to understand and reproduce the issue
- We'll develop and test a fix
- We'll coordinate disclosure timing with you
- We'll credit you in the security advisory (if desired)
- We'll update affected demos and documentation

**If the vulnerability is declined:**

- We'll provide a detailed explanation of why it doesn't qualify as a security issue
- We may suggest alternative channels (like feature requests) if appropriate
- We'll still thank you for your security research efforts

### Security Best Practices

Since these are demo applications, please remember:

- **Never use demo configurations in production** without proper security hardening
- **Review all Docker configurations** before deploying in your environment
- **Use secure API keys and secrets management** in production deployments
- **Keep your Docker installation and dependencies up to date**
