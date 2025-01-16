# 🚀 Boltrade DarpServer

A server implementation for Boltrade  analytics using MCP (Model Control Protocol) , focusing on Solana token analysis.

## ✨ Features

### API Endpoints
- 🔍 `get-sol-top-score-list`: Get top scoring Solana tokens with detailed metrics
  - Token address (CA)
  - Price
  - Symbol
  - 24h Volume
  - Market Cap
  - Liquidity (USD)
  - Score
  - Token Age

- 💰 `get-sol-smart-money-listing`: Track smart money movements in new Solana token listings
  - Token address (CA)
  - Price
  - Symbol
  - 24h Volume
  - Market Cap
  - Liquidity (USD)
  - Score
  - Token Age

## 🛠️ Environment Setup

### Proxy Configuration
Create a `.env` file in the project root:
```env
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
PROXY_HOST=your_proxy_host
PROXY_PORT=your_proxy_port
```

## 🚀 Quick Start

We use UV as our Python package installer and runner. UV is much faster than pip and provides better dependency resolution.

### Prerequisites
- Python 3.8+
- UV package manager

### Install UV

**Unix-like systems (Linux/macOS):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Server Startup

Navigate to the project directory and run:
```bash
cd mcpserver
uv init 
uv run ./server.py
```

The server will start on `0.0.0.0:3002` by default.

## 📊 Logging

All API requests and responses are automatically logged to the `logs` directory with timestamp-based filenames (format: `boltrade_api_YYYYMMDD_HHMMSS.log`).

## 🔨 Development

### Built With
- Starlette
- Uvicorn

---



