#!/bin/bash

# AI Operating System Framework Setup Script
# This script initializes the complete development environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔧 Setting up AI Operating System Framework Development Environment"

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running on macOS, Linux, or Windows (Git Bash)
detect_os() {
    case "$(uname -s)" in
        Darwin*)    OS=macOS;;
        Linux*)     OS=Linux;;
        MINGW*)     OS=Windows;;
        *)          OS=Unknown;;
    esac
    log_info "Detected OS: $OS"
}

# Install system dependencies
install_system_deps() {
    log_info "Checking system dependencies..."
    
    case $OS in
        macOS)
            if ! command -v brew &> /dev/null; then
                log_warning "Homebrew not found. Please install it from https://brew.sh/"
            else
                log_info "Installing Python and Node.js via Homebrew..."
                brew install python node
            fi
            ;;
        Linux)
            if command -v apt-get &> /dev/null; then
                log_info "Installing Python and Node.js via apt..."
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip python3-venv nodejs npm
            elif command -v yum &> /dev/null; then
                log_info "Installing Python and Node.js via yum..."
                sudo yum install -y python3 python3-pip nodejs npm
            fi
            ;;
        Windows)
            log_warning "Please ensure Python 3.8+ and Node.js 16+ are installed"
            log_warning "Download from: https://python.org and https://nodejs.org"
            ;;
    esac
}

# Setup Python environment
setup_python() {
    log_info "Setting up Python environment..."
    
    cd "$PROJECT_ROOT"
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate based on OS
    if [[ "$OS" == "Windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    
    log_success "Python environment setup completed"
}

# Setup CLI
setup_cli() {
    log_info "Setting up CLI tools..."
    
    cd "$PROJECT_ROOT/cli"
    npm install
    
    # Make CLI globally available (optional)
    if [[ "$OS" != "Windows" ]]; then
        chmod +x src/index.js
    fi
    
    log_success "CLI setup completed"
}

# Setup Dashboard
setup_dashboard() {
    log_info "Setting up Dashboard..."
    
    cd "$PROJECT_ROOT/dashboard"
    npm install
    
    log_success "Dashboard setup completed"
}

# Create development configuration
create_dev_config() {
    log_info "Creating development configuration..."
    
    cd "$PROJECT_ROOT"
    
    # Create .env file for development
    cat > .env << EOF
# AI Operating System Framework - Development Environment
ENVIRONMENT=development
LOG_LEVEL=DEBUG
FLASK_ENV=development
FLASK_DEBUG=1
PROMPT_MEMORY_PORT=5000
EOF

    # Create development config
    mkdir -p config
    cat > config/development.json << EOF
{
  "environment": "development",
  "debug": true,
  "system": {
    "name": "AI Operating System Framework",
    "version": "1.0.0",
    "log_level": "DEBUG"
  },
  "agents": {
    "enabled": true,
    "parallel_execution": false,
    "timeout_seconds": 600
  },
  "services": {
    "prompt_memory": {
      "enabled": true,
      "port": 5000,
      "debug": true
    }
  },
  "reports": {
    "enabled": true,
    "format": "json",
    "retention_days": 7
  },
  "development": {
    "auto_reload": true,
    "verbose_logging": true,
    "test_mode": true
  }
}
EOF

    log_success "Development configuration created"
}

# Setup development tools
setup_dev_tools() {
    log_info "Setting up development tools..."
    
    cd "$PROJECT_ROOT"
    
    # Create useful development scripts
    cat > run_dev.sh << 'EOF'
#!/bin/bash
# Development runner script

echo "🚀 Starting AI Operating System in Development Mode"

# Activate Python environment
source venv/bin/activate

# Start prompt memory service in background
cd services/prompt_memory
python app.py &
PROMPT_PID=$!
cd ../..

echo "Prompt Memory Service started (PID: $PROMPT_PID)"
echo "Available at: http://localhost:5000"

# Run main system
echo "Starting main system..."
python main.py

# Cleanup
kill $PROMPT_PID 2>/dev/null || true
EOF

    chmod +x run_dev.sh

    # Create test runner
    cat > run_tests.sh << 'EOF'
#!/bin/bash
# Test runner script

echo "🧪 Running AI Operating System Tests"

# Activate Python environment
source venv/bin/activate

# Run verification
python verify_agents.py

# Run any additional tests
echo "All tests completed!"
EOF

    chmod +x run_tests.sh

    log_success "Development tools setup completed"
}

# Setup IDE configuration
setup_ide_config() {
    log_info "Setting up IDE configuration..."
    
    cd "$PROJECT_ROOT"
    
    # VS Code configuration
    mkdir -p .vscode
    cat > .vscode/settings.json << EOF
{
    "python.pythonPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.associations": {
        "*.md": "markdown"
    },
    "markdown.preview.fontSize": 14
}
EOF

    cat > .vscode/launch.json << EOF
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: AI Operating System",
            "type": "python",
            "request": "launch",
            "program": "main.py",
            "console": "integratedTerminal",
            "cwd": "\${workspaceFolder}",
            "env": {
                "PYTHONPATH": "\${workspaceFolder}"
            }
        },
        {
            "name": "Python: Prompt Memory Service",
            "type": "python",
            "request": "launch",
            "program": "services/prompt_memory/app.py",
            "console": "integratedTerminal",
            "cwd": "\${workspaceFolder}"
        }
    ]
}
EOF

    log_success "IDE configuration completed"
}

# Print final instructions
print_instructions() {
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Development Environment Ready:"
    echo "  ✅ Python virtual environment with all dependencies"
    echo "  ✅ CLI tools ready to use"
    echo "  ✅ Web dashboard ready for development"
    echo "  ✅ Development configuration files"
    echo "  ✅ IDE configuration (VS Code)"
    echo ""
    echo "🚀 Quick Start:"
    echo "  1. Run all agents:     ./run_dev.sh"
    echo "  2. Use CLI:           cd cli && node src/index.js --help"
    echo "  3. Start Dashboard:   cd dashboard && npm start"
    echo "  4. Run tests:         ./run_tests.sh"
    echo ""
    echo "📁 Important directories:"
    echo "  • reports/    - Generated reports from agents"
    echo "  • logs/       - System logs"
    echo "  • config/     - Configuration files"
    echo "  • docs/       - Documentation"
    echo ""
    echo "💡 Tips:"
    echo "  • Check system status: python verify_agents.py"
    echo "  • View agent manifest: cat ai-agents-manifest.json"
    echo "  • Read documentation: ls docs/"
    echo ""
    echo "Happy coding! 🤖"
}

# Main setup function
main() {
    detect_os
    install_system_deps
    setup_python
    setup_cli
    setup_dashboard
    create_dev_config
    setup_dev_tools
    setup_ide_config
    print_instructions
}

# Run main setup
main
