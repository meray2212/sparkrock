# Configuration file for managing environment-specific settings
# This file centralizes all environment configurations and API endpoints
# for the Pemo application across different deployment environments

import os

# Environment Configuration
# ========================
# The ENVIRONMENT variable determines which deployment environment to use
# Defaults to "dev" if no environment variable is set
# Valid values: "dev", "staging", "prod"
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

# API Endpoints
# =============
# Constructs the base API URL based on the current environment
# Format: https://api.{environment}.pemo.io
# Example: https://api.dev.pemo.io for development environment
API_URL = f"https://api.{ENVIRONMENT}.pemo.io"

# Application URLs
# ================
# Constructs the main application URL based on the current environment
# Format: https://app.{environment}.pemo.io
# Example: https://app.dev.pemo.io for development environment
HOME_URL = f"https://app.{ENVIRONMENT}.pemo.io"
