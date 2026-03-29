import sys
import os

# Allow importing from the project root (so `bot.orders` resolves correctly)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from binance.exceptions import BinanceAPIException
from binance.client import Client
from bot.orders import place_market_order, place_limit_order

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Binance Futures Trading Bot",
    page_icon="📈",
    layout="centered",
)

st.title("📈 Binance Futures Trading Bot")
st.caption("Connected to **Testnet** — no real funds at risk.")
st.divider()

# ─── Input Form ───────────────────────────────────────────────────────────────

with st.form("order_form"):
    col1, col2 = st.columns(2)

    with col1:
        symbol = st.text_input(
            "Symbol",
            value="BTCUSDT",
            help="e.g. BTCUSDT, ETHUSDT",
        ).upper().strip()

        side = st.selectbox("Side", ["BUY", "SELL"])

    with col2:
        order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])

        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            value=0.001,
            format="%.4f",
            step=0.001,
            help="Amount of the base asset to trade.",
        )

    # Price field — always rendered, but only relevant for LIMIT
    price = st.number_input(
        "Price (LIMIT only)",
        min_value=0.0,
        value=30000.0,
        format="%.2f",
        step=0.1,
        help="Ignored for MARKET orders.",
        disabled=(order_type == "MARKET"),
    )

    submitted = st.form_submit_button("🚀 Place Order", use_container_width=True)

# ─── Order Logic ──────────────────────────────────────────────────────────────

if submitted:
    try:
        # ── Notional Validation ──────────────────────────────────────────────
        if order_type == "LIMIT":
            notional = quantity * price
            if notional <= 100:
                st.error(
                    f"❌ Limit order value must be greater than $100.  \n"
                    f"Current value = **${notional:.2f}**"
                )
                st.stop()
        else:  # MARKET order
            client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"), testnet=True)
            ticker = client.futures_symbol_ticker(symbol=symbol)
            effective_price = float(ticker["price"])
            notional = quantity * effective_price
            if notional <= 100:
                st.error(
                    f"❌ Market order value must be greater than $100.  \n"
                    f"Current value = **${notional:.2f}**"
                )
                st.stop()

        # ── Place Order ─────────────────────────────────────────────────────
        with st.spinner("Sending order to Binance Testnet…"):
            if order_type == "MARKET":
                response = place_market_order(symbol, side, quantity)
            else:
                response = place_limit_order(symbol, side, quantity, price)

            # ── Success ─────────────────────────────────────────────────────
            st.success("✅ Order placed successfully!")
            st.divider()

            # Readable summary
            st.subheader("📋 Order Summary")
            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:
                st.metric("Order ID", response.get("orderId", "—"))
                st.metric("Status", response.get("status", "—"))

            with summary_col2:
                st.metric("Symbol", response.get("symbol", "—"))
                st.metric("Side", response.get("side", "—"))

            with summary_col3:
                st.metric("Quantity", response.get("origQty", "—"))
                avg_price = response.get("avgPrice") or response.get("price") or "—"
                st.metric("Price", avg_price)

            # Raw JSON
            st.divider()
            with st.expander("🔍 Raw JSON Response", expanded=False):
                st.json(response)

    except BinanceAPIException as e:
        st.error(
            f"❌ Binance API Error `{e.code}`:  \n"
            f"{e.message}"
        )
    except ValueError as e:
        st.error(f"❌ Configuration Error:  \n{e}")
    except Exception as e:
        st.error(f"❌ Unexpected error:  \n{e}")