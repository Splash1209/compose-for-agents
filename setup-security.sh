#!/bin/bash
# Security setup script for compose-for-agents repository
# Run this after cloning to set up security measures

set -e

echo "🔒 Setting up security measures for compose-for-agents..."

# Install pre-commit hook (optional)
read -p "📋 Install pre-commit hook to prevent committing secrets? [y/N]: " install_hook
if [[ $install_hook =~ ^[Yy]$ ]]; then
    if [ -f ".github/hooks/pre-commit" ]; then
        cp .github/hooks/pre-commit .git/hooks/pre-commit
        chmod +x .git/hooks/pre-commit
        echo "✅ Pre-commit hook installed"
    else
        echo "❌ Pre-commit hook file not found"
    fi
fi

# Check for demo directories and create .env files
echo "🔍 Checking for demo directories that need environment setup..."

demos_with_env_template=(
    "adk-sock-shop"
)

for demo in "${demos_with_env_template[@]}"; do
    if [ -d "$demo" ] && [ -f "$demo/.env.template" ]; then
        if [ ! -f "$demo/.env" ]; then
            echo "📁 Setting up $demo..."
            cp "$demo/.env.template" "$demo/.env"
            echo "✅ Created $demo/.env from template"
            echo "⚠️  Please edit $demo/.env and set secure passwords!"
        else
            echo "ℹ️  $demo/.env already exists"
        fi
    fi
done

echo ""
echo "🚨 IMPORTANT SECURITY REMINDERS:"
echo "1. 🔑 Set strong passwords in any .env files created"
echo "2. 📖 Read SECURITY.md for complete security guidelines"
echo "3. 🚫 Never commit .env files or API keys to git"
echo "4. 🔒 Change ALL default passwords before running demos"
echo ""
echo "✅ Security setup complete!"
echo "📚 For more information, see: SECURITY.md"