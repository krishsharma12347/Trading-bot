# Binance Futures Trading Bot

A simple trading bot built with **Python** and **Streamlit**, connected to **Binance Futures Testnet**.  
This project demonstrates how to place Market and Limit orders with proper validation and error handling.  
⚠️ Testnet only — no real funds are used.

---

## 🚀 Features
- Connects securely to Binance Futures Testnet using API keys from `.env`.
- Supports **Market** and **Limit** orders.
- Automatically adjusts **precision** (stepSize / tickSize).
- Validates **minimum notional value > $100** before sending orders.
- Streamlit UI with:
  - Order form (symbol, side, type, quantity, price).
  - Order summary (ID, status, symbol, side, quantity, price).
  - Raw JSON response from Binance.
- Error handling for invalid inputs and API errors.

---

## 📦 Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone 
   cd trading-bot