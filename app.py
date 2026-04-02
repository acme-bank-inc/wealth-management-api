"""Acme Bank Inc Wealth Management API.

A minimal Flask REST API serving fake portfolio and market data
for ETM ASMP testing purposes.
"""

from flask import Flask, jsonify, abort

app = Flask(__name__)

PORTFOLIOS = [
    {
        "id": 1,
        "name": "Conservative Growth",
        "owner": "Alice Johnson",
        "total_value": 250000.00,
        "currency": "USD",
        "holdings": [
            {"symbol": "BND", "name": "Vanguard Total Bond", "shares": 500, "value": 125000.00},
            {"symbol": "VTI", "name": "Vanguard Total Stock", "shares": 300, "value": 75000.00},
            {"symbol": "GLD", "name": "SPDR Gold Shares", "shares": 200, "value": 50000.00},
        ],
    },
    {
        "id": 2,
        "name": "Aggressive Tech",
        "owner": "Bob Martinez",
        "total_value": 780000.00,
        "currency": "USD",
        "holdings": [
            {"symbol": "AAPL", "name": "Apple Inc", "shares": 1000, "value": 200000.00},
            {"symbol": "MSFT", "name": "Microsoft Corp", "shares": 800, "value": 320000.00},
            {"symbol": "NVDA", "name": "NVIDIA Corp", "shares": 400, "value": 260000.00},
        ],
    },
    {
        "id": 3,
        "name": "Balanced Income",
        "owner": "Carol Chen",
        "total_value": 450000.00,
        "currency": "USD",
        "holdings": [
            {"symbol": "SCHD", "name": "Schwab US Dividend", "shares": 600, "value": 150000.00},
            {"symbol": "O", "name": "Realty Income Corp", "shares": 1500, "value": 100000.00},
            {"symbol": "VTI", "name": "Vanguard Total Stock", "shares": 800, "value": 200000.00},
        ],
    },
]

MARKET_DATA = [
    {"symbol": "AAPL", "name": "Apple Inc", "price": 200.50, "change": 1.25, "change_pct": 0.63},
    {"symbol": "MSFT", "name": "Microsoft Corp", "price": 400.75, "change": -2.10, "change_pct": -0.52},
    {"symbol": "NVDA", "name": "NVIDIA Corp", "price": 650.00, "change": 12.30, "change_pct": 1.93},
    {"symbol": "VTI", "name": "Vanguard Total Stock", "price": 250.20, "change": 0.80, "change_pct": 0.32},
    {"symbol": "BND", "name": "Vanguard Total Bond", "price": 72.15, "change": -0.05, "change_pct": -0.07},
    {"symbol": "GLD", "name": "SPDR Gold Shares", "price": 185.40, "change": 3.60, "change_pct": 1.98},
]


@app.route("/api/portfolios", methods=["GET"])
def list_portfolios():
    """Return a summary list of all portfolios."""
    summaries = [
        {"id": p["id"], "name": p["name"], "owner": p["owner"], "total_value": p["total_value"]}
        for p in PORTFOLIOS
    ]
    return jsonify({"portfolios": summaries})


@app.route("/api/portfolios/<int:portfolio_id>", methods=["GET"])
def get_portfolio(portfolio_id):
    """Return full details for a single portfolio."""
    for p in PORTFOLIOS:
        if p["id"] == portfolio_id:
            return jsonify(p)
    abort(404, description="Portfolio not found")


@app.route("/api/market-data", methods=["GET"])
def get_market_data():
    """Return current fake market data."""
    return jsonify({"market_data": MARKET_DATA})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
