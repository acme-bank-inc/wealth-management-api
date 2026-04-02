# Wealth Management API

A minimal Flask REST API for Acme Bank Inc. This service provides fake portfolio and market data endpoints, built for ETM ASMP testing purposes.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/portfolios` | List all portfolio summaries |
| GET | `/api/portfolios/{id}` | Get full portfolio details by ID |
| GET | `/api/market-data` | Get current market data quotes |

## Prerequisites

Python 3.11 or later.

## Setup and Run

```bash
make install   # Create venv and install dependencies
make run       # Start the Flask dev server on port 5000
```

## Other Targets

```bash
make clean     # Remove venv and cached files
```

## Example

```bash
curl http://localhost:5000/api/portfolios
curl http://localhost:5000/api/portfolios/1
curl http://localhost:5000/api/market-data
```
