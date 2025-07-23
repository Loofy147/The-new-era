#!/bin/bash

# AI Operating System Framework Deployment Script
# Usage: ./scripts/deploy.sh [environment]

set -e

ENVIRONMENT=${1:-development}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Deploying AI Operating System Framework to $ENVIRONMENT environment"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check Node.js for CLI and Dashboard
    if ! command -v node &> /dev/null; then
        log_warning "Node.js not found - CLI and Dashboard won't be available"
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_warning "Docker not found - containerized deployment not available"
    fi
    
    log_success "Prerequisites check completed"
}

# Setup Python environment
setup_python_env() {
    log_info "Setting up Python environment..."
    
    cd "$PROJECT_ROOT"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Python dependencies installed"
    fi
}

# Setup CLI
setup_cli() {
    log_info "Setting up CLI..."
    
    if [ -d "$PROJECT_ROOT/cli" ]; then
        cd "$PROJECT_ROOT/cli"
        
        if command -v npm &> /dev/null; then
            npm install
            log_success "CLI dependencies installed"
        else
            log_warning "npm not available - skipping CLI setup"
        fi
    fi
}

# Setup Dashboard
setup_dashboard() {
    log_info "Setting up Dashboard..."
    
    if [ -d "$PROJECT_ROOT/dashboard" ]; then
        cd "$PROJECT_ROOT/dashboard"
        
        if command -v npm &> /dev/null; then
            npm install
            log_success "Dashboard dependencies installed"
        else
            log_warning "npm not available - skipping Dashboard setup"
        fi
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."
    
    cd "$PROJECT_ROOT"
    
    mkdir -p reports
    mkdir -p logs
    mkdir -p config
    mkdir -p data
    
    log_success "Directories created"
}

# Initialize configuration
init_config() {
    log_info "Initializing configuration..."
    
    cd "$PROJECT_ROOT"
    
    # Create basic config if it doesn't exist
    if [ ! -f "config/system.json" ]; then
        cat > config/system.json << EOF
{
  "environment": "$ENVIRONMENT",
  "system": {
    "name": "AI Operating System Framework",
    "version": "1.0.0",
    "log_level": "INFO"
  },
  "agents": {
    "enabled": true,
    "parallel_execution": false,
    "timeout_seconds": 300
  },
  "services": {
    "prompt_memory": {
      "enabled": true,
      "port": 5000
    }
  },
  "reports": {
    "enabled": true,
    "format": "json",
    "retention_days": 30
  }
}
EOF
        log_success "Configuration initialized"
    else
        log_info "Configuration already exists"
    fi
}

# Run system tests
run_tests() {
    log_info "Running system tests..."
    
    cd "$PROJECT_ROOT"
    
    # Activate Python environment
    source venv/bin/activate
    
    # Run verification script
    if [ -f "verify_agents.py" ]; then
        python verify_agents.py
        log_success "System verification completed"
    fi
    
    # Run agent tests if available
    if [ -f "run_tests.py" ]; then
        python run_tests.py
        log_success "Agent tests completed"
    fi
}

# Start services
start_services() {
    log_info "Starting services..."
    
    cd "$PROJECT_ROOT"
    
    # Start prompt memory service in background
    if [ "$ENVIRONMENT" = "development" ]; then
        source venv/bin/activate
        cd services/prompt_memory
        python app.py &
        PROMPT_SERVICE_PID=$!
        echo $PROMPT_SERVICE_PID > "$PROJECT_ROOT/data/prompt_service.pid"
        log_success "Prompt memory service started (PID: $PROMPT_SERVICE_PID)"
        cd "$PROJECT_ROOT"
    fi
}

# Main deployment function
deploy() {
    log_info "Starting deployment process..."
    
    check_prerequisites
    create_directories
    setup_python_env
    setup_cli
    setup_dashboard
    init_config
    
    if [ "$ENVIRONMENT" != "production" ]; then
        run_tests
    fi
    
    start_services
    
    log_success "Deployment completed successfully!"
    
    # Print summary
    echo ""
    echo "📊 Deployment Summary:"
    echo "  Environment: $ENVIRONMENT"
    echo "  Python Environment: ✅"
    echo "  CLI: $([ -d "$PROJECT_ROOT/cli/node_modules" ] && echo "✅" || echo "⚠️")"
    echo "  Dashboard: $([ -d "$PROJECT_ROOT/dashboard/node_modules" ] && echo "✅" || echo "⚠️")"
    echo "  Services: ✅"
    echo ""
    echo "🎯 Next Steps:"
    echo "  1. Run agents: python main.py"
    echo "  2. Use CLI: cd cli && npm start"
    echo "  3. Start Dashboard: cd dashboard && npm start"
    echo "  4. View reports: ls reports/"
}

# Execute deployment
deploy
