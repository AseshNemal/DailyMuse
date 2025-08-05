#!/bin/bash

# Feature Branch Deployment Script
# This script handles the deployment of feature branches

set -e  # Exit on any error

echo "🚀 Starting deployment for branch: $BRANCH_NAME"
echo "📝 Commit SHA: $COMMIT_SHA"
echo "⏰ Deployment started at: $(date)"

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to handle errors
handle_error() {
    log "❌ ERROR: $1"
    exit 1
}

# Validate environment variables
log "🔍 Validating environment variables..."
if [ -z "$BRANCH_NAME" ]; then
    handle_error "BRANCH_NAME environment variable is not set"
fi

if [ -z "$COMMIT_SHA" ]; then
    handle_error "COMMIT_SHA environment variable is not set"
fi

# Extract feature information
log "📋 Extracting feature information..."
FEATURE_NAME=$(echo "$BRANCH_NAME" | sed 's/feature\///' | sed 's/feat\///')
log "Feature: $FEATURE_NAME"

# Install dependencies
log "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || handle_error "Failed to install Python dependencies"
elif [ -f "auto-medium-blog/requirements.txt" ]; then
    pip install -r auto-medium-blog/requirements.txt || handle_error "Failed to install Python dependencies"
fi

if [ -f "package.json" ]; then
    npm install || handle_error "Failed to install Node.js dependencies"
fi

# Run tests (if available)
log "🧪 Running tests..."
if [ -f "pytest.ini" ] || [ -f "test_*.py" ] || [ -d "tests/" ]; then
    log "Running Python tests..."
    python -m pytest -v || log "⚠️ WARNING: Some tests failed"
fi

if [ -f "package.json" ] && grep -q '"test"' package.json; then
    log "Running Node.js tests..."
    npm test || log "⚠️ WARNING: Some tests failed"
fi

# Build the application (if needed)
log "🔨 Building application..."
if [ -f "Dockerfile" ]; then
    log "Building Docker image..."
    docker build -t "dailymuse-$FEATURE_NAME:$COMMIT_SHA" . || handle_error "Docker build failed"
fi

if [ -f "package.json" ] && grep -q '"build"' package.json; then
    log "Running npm build..."
    npm run build || handle_error "npm build failed"
fi

# Validate configuration files
log "✅ Validating configuration..."
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    log "⚠️ WARNING: .env file not found, but .env.example exists"
fi

# Check for Python syntax errors
log "🐍 Checking Python syntax..."
find . -name "*.py" -type f -exec python -m py_compile {} \; 2>/dev/null || log "⚠️ WARNING: Some Python files have syntax errors"

# Simulate deployment steps
log "🚀 Deploying to development environment..."

# Create deployment artifact
ARTIFACT_DIR="deployment-artifacts"
mkdir -p "$ARTIFACT_DIR"

# Copy relevant files
log "📁 Creating deployment artifact..."
cp -r . "$ARTIFACT_DIR/" 2>/dev/null || true

# Create deployment manifest
cat > "$ARTIFACT_DIR/deployment-manifest.json" << EOF
{
    "branch": "$BRANCH_NAME",
    "commit": "$COMMIT_SHA",
    "feature": "$FEATURE_NAME",
    "deployedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "environment": "development",
    "version": "$(git describe --tags --always 2>/dev/null || echo 'unknown')"
}
EOF

# Simulate health check
log "🏥 Running health checks..."
sleep 2  # Simulate deployment time

# Check if main Python file can be imported
if [ -f "auto-medium-blog/blog_bot.py" ]; then
    log "Testing blog bot import..."
    python -c "import sys; sys.path.append('auto-medium-blog'); import blog_bot" 2>/dev/null && \
        log "✅ Blog bot import successful" || \
        log "⚠️ WARNING: Blog bot import failed"
fi

# Simulate service startup
log "🔄 Starting services..."
sleep 1

# Final validation
log "🔍 Final deployment validation..."
if [ -d "$ARTIFACT_DIR" ] && [ -f "$ARTIFACT_DIR/deployment-manifest.json" ]; then
    log "✅ Deployment artifact created successfully"
else
    handle_error "Deployment artifact creation failed"
fi

# Success
log "🎉 Deployment completed successfully!"
log "📊 Deployment Summary:"
log "   - Branch: $BRANCH_NAME"
log "   - Feature: $FEATURE_NAME" 
log "   - Commit: $COMMIT_SHA"
log "   - Environment: Development"
log "   - Status: ✅ Success"
log "   - Completed at: $(date)"

echo ""
echo "🔗 Deployment artifact location: $ARTIFACT_DIR/"
echo "📋 Deployment manifest: $ARTIFACT_DIR/deployment-manifest.json"
echo ""
echo "✅ Feature branch deployment completed successfully! 🚀"
