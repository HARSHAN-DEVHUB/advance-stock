#!/bin/bash

# Stock Prediction API Deployment Script

set -e

echo "🚀 Stock Prediction API Deployment Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Function to install dependencies
install_dependencies() {
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully!"
}

# Function to setup environment
setup_environment() {
    echo "🔧 Setting up environment..."
    
    if [ ! -f .env ]; then
        echo "📝 Creating .env file..."
        cp env_example.txt .env
        echo "⚠️ Please edit .env file and add your Alpha Vantage API key"
    else
        echo "✅ .env file already exists"
    fi
}

# Function to run locally
run_local() {
    echo "🏃 Running application locally..."
    python start.py
}

# Function to run with Docker
run_docker() {
    echo "🐳 Running with Docker..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    echo "🔨 Building Docker image..."
    docker-compose build
    
    echo "🚀 Starting application with Docker Compose..."
    docker-compose up -d
    
    echo "✅ Application is running!"
    echo "📊 API available at: http://localhost:8000"
    echo "📋 Health check: http://localhost:8000/health"
    echo "📖 API docs: http://localhost:8000/docs"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  local     Run the application locally"
    echo "  docker    Run the application with Docker"
    echo "  install   Install dependencies only"
    echo "  setup     Setup environment only"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local    # Run locally"
    echo "  $0 docker   # Run with Docker"
    echo "  $0 install  # Install dependencies"
}

# Main script logic
case "${1:-help}" in
    "local")
        install_dependencies
        setup_environment
        run_local
        ;;
    "docker")
        setup_environment
        run_docker
        ;;
    "install")
        install_dependencies
        ;;
    "setup")
        setup_environment
        ;;
    "help"|*)
        show_help
        ;;
esac 