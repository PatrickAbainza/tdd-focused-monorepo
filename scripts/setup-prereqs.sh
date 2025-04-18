#!/bin/bash
set -e
set -o pipefail

# --- Cross-Platform Development Environment Setup ---

# This script installs necessary development tools across different OS platforms.

echo "Starting prerequisites setup..."

# Function to check if a command exists
command_exists() {
    command -v "$1" &>/dev/null
}

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        # Linux
        . /etc/os-release
        OS_TYPE="linux"
        OS_NAME="$NAME"
    elif [ "$(uname)" == "Darwin" ]; then
        # macOS
        OS_TYPE="macos"
        OS_NAME="macOS"
    else
        echo "Unsupported operating system"
        exit 1
    fi
}

# Function to detect package manager
detect_package_manager() {
    if command_exists apt; then
        PKG_MANAGER="apt"
        PKG_INSTALL="sudo apt install -y"
        # Update package list for apt
        sudo apt update
        # Fix potential GPG ownership issues
        if [ -d "$HOME/.gnupg" ]; then
            echo "Fixing GPG directory ownership..."
            sudo chown -R $(whoami) "$HOME/.gnupg/"
        fi
    elif command_exists dnf; then
        PKG_MANAGER="dnf"
        PKG_INSTALL="sudo dnf install -y"
    elif command_exists pacman; then
        PKG_MANAGER="pacman"
        PKG_INSTALL="sudo pacman -S --noconfirm"
        # Update package list for pacman
        sudo pacman -Sy
    elif command_exists brew; then
        PKG_MANAGER="brew"
        PKG_INSTALL="brew install"
        # Update brew
        brew update
    else
        echo "No supported package manager found"
        exit 1
    fi
}

# Function to install system package
install_package() {
    local package_name="$1"
    local command_name="${2:-$1}"

    echo "Checking for $package_name..."
    if ! command_exists "$command_name"; then
        echo "Installing $package_name..."
        if sudo $PKG_INSTALL "$package_name"; then
            echo "$package_name installed successfully."
        else
            echo "ERROR: Failed to install $package_name. Please check package manager output."
            exit 1
        fi
    fi

    verify_command "$command_name"
}

# Function to verify command installation
verify_command() {
    local command_name="$1"
    echo "Verifying $command_name installation..."
    if command_exists "$command_name"; then
        echo "$command_name found: $(command -v "$command_name")"
    else
        echo "ERROR: $command_name verification failed after installation attempt."
        exit 1
    fi
    echo "---"
}

# Function to install Python packages using uv
install_python_packages() {
    echo "Setting up Python development tools..."

    # Create virtual environment
    if ! command_exists uv; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
        source .venv/bin/activate
        echo "Virtual environment activated."
    fi

    # Install Python packages using uv
    echo "Installing Python development tools..."
    uv pip install \
        pytest \
        pytest-cov \
        ruff \
        radon \
        copydetect \
        pydeps \
        pip-audit \
        pre-commit

    # Verify key tool installations
    for tool in pytest ruff pip-audit pre-commit; do
        verify_command "$tool"
    done
}

# Function to install Node.js packages
install_node_packages() {
    echo "Setting up Node.js development tools..."

    # Install global npm packages
    echo "Installing Node.js development tools..."
    sudo npm install -g \
        vitest \
        eslint \
        prettier \
        husky \
        lint-staged \
        jscpd \
        dependency-cruiser

    # Verify key tool installations
    for tool in vitest eslint prettier; do
        verify_command "$tool"
    done
}

# Main installation process
echo "Detecting system configuration..."
detect_os
echo "Detected OS: $OS_NAME"

detect_package_manager
echo "Using package manager: $PKG_MANAGER"
echo "---"

# Install base development tools
echo "Installing base development tools..."
install_package "git"
install_package "python3" "python3"
install_package "curl"

# Install Node.js based on OS
if [ "$OS_TYPE" = "linux" ]; then
    if [ "$PKG_MANAGER" = "apt" ]; then
        # For Debian/Ubuntu, use NodeSource
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        install_package "nodejs" "node"
    elif [ "$PKG_MANAGER" = "dnf" ]; then
        # For Fedora, use NodeSource
        curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
        install_package "nodejs" "node"
    elif [ "$PKG_MANAGER" = "pacman" ]; then
        # For Arch Linux
        install_package "nodejs" "node"
    fi
else
    # For macOS
    install_package "node"
fi

# Install development tools
install_python_packages
install_node_packages

echo "Prerequisites setup completed successfully."

# Optional: Clean up unused packages (Applies only if using apt)
if [ "$PKG_MANAGER" = "apt" ]; then
    read -p "System detected unused packages. Run 'sudo apt autoremove' to clean them up? (y/N): " cleanup_choice
    if [[ "$cleanup_choice" =~ ^[Yy]$ ]]; then
        echo "Running package cleanup..."
        sudo apt autoremove -y
    fi
fi
echo "Next steps:"
echo "1. Run 'make setup' to install project dependencies"
echo "2. Run 'uv run pre-commit install' to set up Git hooks"
echo "3. For Node.js template, run 'cd templates/nodejs-vitest && npx husky install'"

# Optional: Upgrade packages (Applies only if using apt)
if [ "$PKG_MANAGER" = "apt" ]; then
    read -p "System detected upgradable packages. Run 'sudo apt upgrade' now? (y/N): " upgrade_choice
    if [[ "$upgrade_choice" =~ ^[Yy]$ ]]; then
        echo "Running system upgrade..."
        sudo apt upgrade -y
    fi
fi
