"""
==========================================================
                APPLICATION CONFIGURATION
==========================================================

This file loads all application settings from the .env file.

Instead of reading environment variables throughout the
project, every file imports values from this file.

Example:
    from core.config import DATABASE_URL, APP_NAME
"""

# ==========================================================
# Import Required Modules
# ==========================================================

import os

# from dotenv import load_dotenv

# # ==========================================================
# # Load Environment Variables
# # ==========================================================

# load_dotenv()

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

# ==========================================================
# Application Configuration
# ==========================================================

APP_NAME = os.getenv("APP_NAME", "Student Management System")

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

APP_DESCRIPTION = os.getenv(
    "APP_DESCRIPTION",
    "Production Ready Student Management API",
)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ==========================================================
# Database Configuration
# ==========================================================

DB_HOST = os.getenv("DB_HOST", "localhost")

DB_PORT = int(os.getenv("DB_PORT", 5432))

DB_NAME = os.getenv("DB_NAME", "student_db")

DB_USER = os.getenv("DB_USER", "postgres")

DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# print("DATABASE_URL =", DATABASE_URL)
# print("DB_PASSWORD =", DB_PASSWORD)

# ==========================================================
# Logging Configuration
# ==========================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOG_FILE = os.getenv(
    "LOG_FILE",
    "logs/application.log",
)

# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change_this_secret_key"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

# ==========================================================
# Staff OTP / Email Configuration
# ==========================================================
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER or "no-reply@admitix.local")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
AUTH_OTP_EXPIRE_MINUTES = int(os.getenv("AUTH_OTP_EXPIRE_MINUTES", "10"))
# Keep this enabled for local/demo environments where SMTP is not configured.
# Set it to false in production so OTPs are only delivered by email.
AUTH_OTP_EXPOSE_IN_RESPONSE = os.getenv("AUTH_OTP_EXPOSE_IN_RESPONSE", "true").lower() == "true"

# ==========================================================
# CORS Configuration
# ==========================================================

ALLOW_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOW_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
]

# ==========================================================
# Display Configuration (For Learning)
# ==========================================================

if __name__ == "__main__":

    print("=" * 50)
    print("Application Configuration")
    print("=" * 50)

    print(f"App Name      : {APP_NAME}")
    print(f"Version       : {APP_VERSION}")
    print(f"Debug Mode    : {DEBUG}")

    print("\nDatabase")
    print("-" * 50)
    print(f"Host          : {DB_HOST}")
    print(f"Port          : {DB_PORT}")
    print(f"Database      : {DB_NAME}")
    print(f"Username      : {DB_USER}")

    print("\nLogging")
    print("-" * 50)
    print(f"Level         : {LOG_LEVEL}")
    print(f"Log File      : {LOG_FILE}")

    print("\nDatabase URL")
    print("-" * 50)
    print(DATABASE_URL)
